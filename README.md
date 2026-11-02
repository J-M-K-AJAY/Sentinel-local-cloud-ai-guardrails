# Sentinel — Local AI Guardrails for Cloud Security

An educational, local-first demonstration of input and output guardrails around a locally hosted language model. The project combines the original Python guardrail modules with a Flask API and a responsive, scroll-based web interface.

> **Scope:** Educational prototype only. It performs no real cloud actions and is not production security software. Its pattern-based rules are intentionally limited and do not guarantee detection of all unsafe requests or responses.

## What it demonstrates

- Input classification (`ALLOW`, `SENSITIVE`, `RESTRICT`) before model inference.
- Local text generation using Ollama and `qwen2.5:0.5b-instruct`.
- Output screening before a generated response is delivered.
- Safe fallback responses when an input is restricted, output is blocked, or Ollama is unavailable.
- A browser UI that visualises the actual backend result at each pipeline stage.

## Architecture

```text
Browser (HTML/CSS/JS)
        │ POST /api/chat
        ▼
     Flask API
        │
        ▼
 Input guardrail ── RESTRICT ──► Fallback response
        │ ALLOW / SENSITIVE
        ▼
 Ollama (Qwen 2.5 0.5B Instruct)
        │
        ▼
 Output guardrail ── BLOCK ──► Fallback response
        │ ALLOW
        ▼
 Browser chat response
```

`SENSITIVE` is a classification, not an automatic block in the original implementation: it continues to the model and is displayed in the pipeline as an input-check pass with its category shown. `RESTRICT` stops before inference.

## Project structure

```text
ai-cloud-guardrails-frontend/
├── app.py
├── main.py                    # Original CLI entry point
├── input_guardrail.py         # Original input rules
├── output_guardrail.py        # Original output rules
├── llm_client.py              # Ollama client
├── fallback_handler.py        # Safe fallback text
├── test_guardrails.py         # Original unit tests
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── styles.css
```

## Requirements

- Python 3.9 or newer
- Ollama installed and running locally
- `qwen2.5:0.5b-instruct` pulled in Ollama

## Run locally

1. **Install / start Ollama**, then pull the model:

   ```bash
   ollama pull qwen2.5:0.5b-instruct
   ```

2. **Create and activate a virtual environment** from the project root:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # macOS / Linux
   # .venv\\Scripts\\activate     # Windows PowerShell
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama** (if it is not already running):

   ```bash
   ollama serve
   ```

5. **Start the web app** in another terminal:

   ```bash
   python app.py
   ```

6. Open <http://127.0.0.1:5000> in your browser.

The web app and model are intended to run on the same machine. The browser sends prompts to Flask; Flask calls Ollama at `http://localhost:11434`.

## Run the original tests

```bash
python -m unittest -v
```

The supplied project contained six input-guardrail unit tests. Run them locally after setup to confirm the current environment.

## API

- `GET /api/health` — reports the configured local engine and model name. It does not guarantee Ollama is reachable.
- `POST /api/chat` — JSON body: `{"prompt": "How can I secure cloud storage?"}`. Returns the input classification, whether model inference was attempted, output-check result (when applicable), final status and user-facing response.

## Deployment notes

This application is designed first for **local demonstration**. A conventional static host cannot run Ollama or load the model. To make it publicly accessible, deploy the Flask service on a private server you control with Ollama and the model installed, then serve the frontend through Flask or configure a secure reverse proxy. Do not expose Ollama's port or an unauthenticated prompt endpoint directly to the public internet. Add authentication, rate limiting, request-size limits, HTTPS, logging controls and stronger security review before any public deployment. Do not send confidential or personal data to this educational prototype.

## Limitations and responsible use

- Guardrails use regular-expression pattern matching, so they can miss unsafe content and may flag benign content.
- The output filter checks a small number of configured phrases; it is not a semantic safety classifier.
- The demo does not connect to AWS, Azure, GCP or any real cloud account.
- The local model may produce inaccurate or incomplete information. Verify security advice independently.
- The UI's stage indicators reflect backend responses; animations are presentation only and do not fabricate check results.
