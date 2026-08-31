"""Local Ollama client. No cloud AI is required."""

import requests

from config import OLLAMA_MODEL, OLLAMA_URL, REQUEST_TIMEOUT


class OllamaError(RuntimeError):
    pass


def list_models() -> list[str]:
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return [m.get("name", "") for m in response.json().get("models", [])]
    except requests.RequestException as exc:
        raise OllamaError(f"Cannot connect to Ollama at {OLLAMA_URL}: {exc}") from exc


def generate(prompt: str, model: str = OLLAMA_MODEL) -> str:
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.2}},
            timeout=300,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.RequestException as exc:
        raise OllamaError(f"Ollama analysis failed: {exc}") from exc
