"""Configuration for the local Polymarket research terminal."""

import os

POLYMARKET_GAMMA_URL = os.getenv("POLYMARKET_GAMMA_URL", "https://gamma-api.polymarket.com")
POLYMARKET_CLOB_URL = os.getenv("POLYMARKET_CLOB_URL", "https://clob.polymarket.com")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
NEWS_LIMIT = int(os.getenv("NEWS_LIMIT", "8"))
