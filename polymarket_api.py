"""Read-only Polymarket API client."""

from typing import Any
import requests

from config import POLYMARKET_CLOB_URL, POLYMARKET_GAMMA_URL, REQUEST_TIMEOUT


class PolymarketError(RuntimeError):
    pass


def _get(url: str, params: dict[str, Any] | None = None) -> Any:
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise PolymarketError(f"Polymarket request failed: {exc}") from exc


def get_markets(limit: int = 20) -> list[dict[str, Any]]:
    data = _get(
        f"{POLYMARKET_GAMMA_URL}/markets",
        {"active": "true", "closed": "false", "limit": limit, "order": "volumeNum", "ascending": "false"},
    )
    return data if isinstance(data, list) else data.get("data", [])


def search_markets(query: str, limit: int = 20) -> list[dict[str, Any]]:
    markets = get_markets(100)
    terms = query.lower().split()
    scored = []
    for market in markets:
        text = f"{market.get('question', '')} {market.get('description', '')}".lower()
        score = sum(term in text for term in terms)
        if score:
            scored.append((score, market))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [market for _, market in scored[:limit]]


def get_price_history(token_id: str, interval: str = "1d", fidelity: int = 60) -> list[dict[str, Any]]:
    data = _get(
        f"{POLYMARKET_CLOB_URL}/prices-history",
        {"market": token_id, "interval": interval, "fidelity": fidelity},
    )
    return data.get("history", []) if isinstance(data, dict) else []


def get_orderbook(token_id: str) -> dict[str, Any]:
    return _get(f"{POLYMARKET_CLOB_URL}/book", {"token_id": token_id})


def extract_token_ids(market: dict[str, Any]) -> list[str]:
    raw = market.get("clobTokenIds", market.get("clob_token_ids", []))
    if isinstance(raw, str):
        try:
            import json
            raw = json.loads(raw)
        except json.JSONDecodeError:
            raw = [raw]
    return [str(x) for x in raw] if isinstance(raw, list) else []


def market_summary(market: dict[str, Any]) -> dict[str, Any]:
    tokens = extract_token_ids(market)
    prices = market.get("outcomePrices", market.get("outcome_prices", []))
    if isinstance(prices, str):
        try:
            import json
            prices = json.loads(prices)
        except json.JSONDecodeError:
            prices = []
    return {
        "id": market.get("id"),
        "question": market.get("question", "Unknown"),
        "description": market.get("description", ""),
        "url": market.get("url") or (f"https://polymarket.com/event/{market.get('slug')}" if market.get("slug") else ""),
        "volume": market.get("volumeNum", market.get("volume", 0)),
        "liquidity": market.get("liquidityNum", market.get("liquidity", 0)),
        "outcomes": market.get("outcomes", []),
        "prices": prices,
        "token_ids": tokens,
    }
