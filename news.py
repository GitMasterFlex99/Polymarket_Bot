"""Lightweight evidence collection using Google News RSS."""

from urllib.parse import quote_plus
import feedparser
import requests
from bs4 import BeautifulSoup

from config import NEWS_LIMIT, REQUEST_TIMEOUT


def _clean(text: str) -> str:
    return BeautifulSoup(text or "", "html.parser").get_text(" ", strip=True)


def search_news(query: str, limit: int = NEWS_LIMIT) -> list[dict[str, str]]:
    url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT, headers={"User-Agent": "PolymarketResearchTerminal/1.0"})
        response.raise_for_status()
        feed = feedparser.parse(response.content)
    except requests.RequestException as exc:
        return [{"title": "News search failed", "url": "", "source": "", "summary": str(exc)}]

    results = []
    for entry in feed.entries[:limit]:
        results.append({
            "title": _clean(entry.get("title", "")),
            "url": entry.get("link", ""),
            "source": _clean(entry.get("source", {}).get("title", "")) if hasattr(entry.get("source", {}), "get") else "",
            "summary": _clean(entry.get("summary", ""))[:600],
            "published": entry.get("published", ""),
        })
    return results


def format_sources(sources: list[dict[str, str]]) -> str:
    if not sources:
        return "No external sources found."
    lines = []
    for i, source in enumerate(sources, 1):
        lines.append(f"[{i}] {source.get('source') or 'Unknown publisher'} — {source.get('title', 'Untitled')}\n    {source.get('url', '')}")
    return "\n".join(lines)
