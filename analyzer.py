"""Evidence-first market analysis."""

import json
from ollama_client import generate
from news import format_sources


def build_prompt(market: dict, sources: list[dict], history: list[dict] | None = None) -> str:
    evidence = format_sources(sources)
    movement = json.dumps(history or [], indent=2, ensure_ascii=False)
    return f"""You are an evidence-first prediction-market research analyst.

Analyze the Polymarket market below using ONLY the supplied market data, historical price data, and sources.
Do not invent facts, sources, dates, causes, statistics, or URLs.
Clearly separate FACTS from INFERENCES and SPECULATION.
A price movement is NOT proof of causation. When explaining a movement, explicitly distinguish correlation from confirmed cause.
If evidence is insufficient, say so.
Do not give financial advice or claim certainty.

MARKET DATA:
{json.dumps(market, indent=2, ensure_ascii=False)}

HISTORICAL PRICE DATA AND STATS:
{movement}

EXTERNAL SOURCES:
{evidence}

Return concise Markdown with exactly these sections:
1. Assessment
2. Price Movement
3. Key Facts
4. Possible Explanations
5. What Could Change The View
6. Evidence Quality

In Price Movement, report the observed change using the supplied statistics. Do not fabricate a percentage.
In Possible Explanations, rank explanations by evidence strength and label each as CONFIRMED, SUPPORTED, or SPECULATIVE.
For each factual claim based on a source, cite it as [SOURCE n].
Never create a citation number that does not exist above.
"""


def analyze_market(market: dict, sources: list[dict], history: list[dict] | None = None) -> str:
    return generate(build_prompt(market, sources, history))
