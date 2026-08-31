"""Evidence-first market analysis."""

import json
from ollama_client import generate
from news import format_sources


def build_prompt(market: dict, sources: list[dict]) -> str:
    evidence = format_sources(sources)
    return f"""You are an evidence-first prediction-market research analyst.

Analyze the Polymarket market below using ONLY the supplied market data and sources.
Do not invent facts, sources, dates, causes, statistics, or URLs.
Clearly separate FACTS from INFERENCES and SPECULATION.
If the evidence is insufficient, say so.
Do not give financial advice or claim certainty.

MARKET DATA:
{json.dumps(market, indent=2, ensure_ascii=False)}

EXTERNAL SOURCES:
{evidence}

Return concise Markdown with exactly these sections:
1. Assessment
2. Key Facts
3. Possible Explanations
4. What Could Change The View
5. Evidence Quality

For each factual claim based on a source, cite it as [SOURCE n].
Never create a citation number that does not exist above.
"""


def analyze_market(market: dict, sources: list[dict]) -> str:
    return generate(build_prompt(market, sources))
