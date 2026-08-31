"""Interactive terminal entry point."""

import sys

from analyzer import analyze_market
from news import format_sources, search_news
from ollama_client import OllamaError, list_models
from polymarket_api import PolymarketError, get_markets, market_summary, search_markets


def money(value) -> str:
    try:
        return f"${float(value):,.0f}"
    except (TypeError, ValueError):
        return "N/A"


def show_markets(markets: list[dict]) -> None:
    if not markets:
        print("No markets found.")
        return
    for i, raw in enumerate(markets, 1):
        m = market_summary(raw)
        price = " / ".join(str(p) for p in m["prices"][:2]) if m["prices"] else "N/A"
        print(f"[{i}] {m['question']}")
        print(f"    Probability: {price} | Volume: {money(m['volume'])} | Liquidity: {money(m['liquidity'])}")
        print()


def choose_market(markets: list[dict]) -> dict | None:
    if not markets:
        return None
    choice = input("Select market number (Enter to cancel): ").strip()
    if not choice:
        return None
    try:
        return markets[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None


def analyze(raw: dict) -> None:
    market = market_summary(raw)
    print("\nCollecting independent sources...\n")
    sources = search_news(market["question"])
    print(format_sources(sources))
    print("\nRunning local Ollama analysis...\n")
    try:
        print(analyze_market(market, sources))
    except OllamaError as exc:
        print(f"\nOllama error: {exc}")
        print("Install Ollama, start it, and pull a model such as llama3.2.")


def main() -> None:
    print("=" * 62)
    print("POLYMARKET RESEARCH TERMINAL")
    print("Local AI • Public Polymarket data • Concrete sources")
    print("=" * 62)

    try:
        models = list_models()
        print(f"Ollama: OK ({', '.join(models[:3]) or 'no models installed'})")
    except OllamaError:
        print("Ollama: NOT CONNECTED — AI analysis will be unavailable")

    while True:
        print("\n[1] Browse high-volume markets")
        print("[2] Search markets")
        print("[3] Exit")
        choice = input("\nSelect: ").strip()

        try:
            if choice == "1":
                markets = get_markets(15)
                show_markets(markets)
                selected = choose_market(markets)
                if selected:
                    analyze(selected)
            elif choice == "2":
                query = input("Search: ").strip()
                if query:
                    markets = search_markets(query)
                    show_markets(markets)
                    selected = choose_market(markets)
                    if selected:
                        analyze(selected)
            elif choice == "3":
                return
            else:
                print("Invalid option.")
        except PolymarketError as exc:
            print(f"Polymarket error: {exc}")
        except KeyboardInterrupt:
            print("\nExiting.")
            return


if __name__ == "__main__":
    main()
