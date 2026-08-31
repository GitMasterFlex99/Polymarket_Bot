# Polymarket Research Terminal

A standalone Windows/Linux terminal application for researching Polymarket markets with a **local Ollama model** and concrete external sources.

## What it does

- Reads public Polymarket market data without a Polymarket API key.
- Finds relevant news through Google News RSS.
- Shows the actual source title, publisher, and URL.
- Sends market data + source evidence to a local Ollama model.
- Instructs the model to separate facts, inferences, and speculation.
- Requires no paid AI API for the analysis layer.
- Does not place trades.
- Does not require a server or database.

Polymarket's public Gamma API exposes market/event data without authentication, while the CLOB provides public read endpoints for market data. Ollama exposes its local API at `http://localhost:11434/api`. 

## Requirements

- Python 3.10+
- Ollama installed and running
- An Ollama model, for example `llama3.2`
- Internet connection for Polymarket and source collection

## Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull llama3.2
python run.py
```

If PowerShell blocks activation, you can run the Python executable directly:

```powershell
.\.venv\Scripts\python.exe run.py
```

## Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2
python run.py
```

## Configuration

Environment variables are optional:

```text
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
REQUEST_TIMEOUT=15
NEWS_LIMIT=8
```

## Evidence philosophy

The model is explicitly told not to invent sources or facts. Source-backed claims should use `[SOURCE n]` references. The application prints the concrete source URLs separately so the user can inspect the evidence themselves.

A source is evidence, not proof of causality. If the available sources do not establish why a market moved, the model should say that the cause is uncertain rather than manufacture an explanation.

## Current scope

This first version is intentionally small. It is a research terminal, not a trading bot. Future versions can add historical price analysis, source deduplication, stronger source ranking, local caching, market movement detection, and configurable research commands.
