"""Lightweight evidence collection and source quality ranking."""

from urllib.parse import quote_plus, urlparse
import feedparser
import requests
from bs4 import BeautifulSoup

from config import NEWS_LIMIT, REQUEST_TIMEOUT

TRUSTED_PUBLISHERS = {
    "reuters": 10,
    "associated press": 10,
    "ap news": 10,
    "bbc": 9,
    "financial times": 9,
    "the wall street journal": 9,
    "new york times": 9,
    "bloomberg": 9,
    "the guardian": 8,
    "politico": 8,
    "npr": 8,
}


def _clean(text: str) -> str:
    return BeautifulSoup(text or "", "html.parser").get_text(" ", strip=True)


def source_quality(source: dict[str, str]) -> tuple[int, str]:
    publisher = (source.get("source") or "").lower().strip()
    domain = urlparse(source.get("url") or "").netloc.lower().removeprefix("www.")
    for name, score in TRUSTED_PUBLISHERS.items():
        if name in publisher or name.replace(" ", "") in domain.replace(".", ""):
            return score, "Established publisher"
    if domain.endswith(".gov") or domain.endswith(".gov.uk") or domain.endswith(".eu"):
        return 10, "Government / official domain"
    if domain.endswith(".edu"):
        return 8, "Academic institution"
    if domain:
        return 5, "Other publisher"
    return 1, "Unknown source"


def search_news(query: str, limit: int = NEWS_LIMIT) -> list[dict[str, str]]:
    url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT, headers={"User-Agent": "PolymarketResearchTerminal/1.0"})
        response.raise_for_status()
        feed = feedparser.parse(response.content)
    except requests.RequestException as exc:
        return [{"title": "News search failed", "url": "", "source": "", "summary": str(exc), "quality": "1"}]

    results = []
    for entry in feed.entries[:limit]:
        source_name = _clean(entry.get("source", {}).get("title", "")) if hasattr(entry.get("source", {}), "get") else ""
        result = {
            "title": _clean(entry.get("title", "")),
            "url": entry.get("link", ""),
            "source": source_name,
            "summary": _clean(entry.get("summary", ""))[:600],
            "published": entry.get("published", ""),
        }
        score, label = source_quality(result)
        result["quality"] = str(score)
        result["quality_label"] = label
        results.append(result)
    return sorted(results, key=lambda item: int(item.get("quality", "1")), reverse=True)


def format_sources(sources: list[dict[str, str]]) -> str:
    if not sources:
        return "No external sources found."
    lines = []
    for i, source in enumerate(sources, 1):
        quality = source.get("quality", "?")
        label = source.get("quality_label", "Unknown")
        lines.append(
            f"[{i}] {source.get('source') or 'Unknown publisher'} — {source.get('title', 'Untitled')}\n"
            f"    Quality: {quality}/10 ({label})\n"
            f"    Published: {source.get('published', 'Unknown')}\n"
            f"    {source.get('url', '')}"
        )
    return "\n".join(lines)
