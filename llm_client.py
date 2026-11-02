"""Client for a locally running Ollama model."""
import json
import urllib.error
import urllib.request


MODEL = "qwen2.5:0.5b-instruct"
OLLAMA_URL = "http://localhost:11434/api/generate"


class LLMError(Exception):
    """Raised when the local model cannot respond."""


def generate_response(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result.get("response", "").strip()

        if not answer:
            raise LLMError("The local model returned an empty response.")

        return answer

    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise LLMError(
            "Could not get a response from Ollama. "
            "Check that Ollama is running and the model is installed."
        ) from exc