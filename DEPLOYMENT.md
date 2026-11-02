# Run and publish checklist

## Local run

1. Install Ollama and run `ollama pull qwen2.5:0.5b-instruct`.
2. Create a virtual environment and run `pip install -r requirements.txt`.
3. Ensure Ollama is running (`ollama serve`, if needed).
4. Run `python app.py` and open `http://127.0.0.1:5000`.
5. In a second terminal, run `python -m unittest -v`.
6. Test a normal defensive prompt, a prompt that triggers an input rule, and the model-unavailable path (stop Ollama temporarily). Confirm the UI accurately reports each outcome.

## GitHub

Before pushing, review `git status` and confirm `.venv`, model files, credentials and personal data are not included.

```bash
git init
git add .
git status
git commit -m "Add interactive frontend for local AI guardrails"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-cloud-guardrails.git
git push -u origin main
```

If a Git repository or remote already exists, inspect it with `git status` and `git remote -v` instead of repeating `git init` or `git remote add`.

## Public hosting

A public deployment needs a server with sufficient memory/compute for Ollama and the selected model. Do not deploy this development server with Flask debug mode enabled. Use a production WSGI server, HTTPS, authentication, rate limiting and a private network path to Ollama. The current app is intended for local demonstration until those controls are implemented.
