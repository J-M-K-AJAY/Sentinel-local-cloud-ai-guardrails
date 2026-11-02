"""Flask web interface for the local AI cloud guardrails demonstration."""
from flask import Flask, jsonify, render_template, request
from input_guardrail import check_input
from llm_client import generate_response, LLMError, MODEL
from output_guardrail import check_output
from fallback_handler import safe_fallback

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", model=MODEL)


@app.get("/api/health")
def health():
    # The model is checked when a prompt is submitted; this endpoint reports configuration.
    return jsonify({"status": "online", "model": MODEL, "engine": "Ollama", "mode": "local"})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "")
    if not isinstance(prompt, str) or not prompt.strip():
        return jsonify({"error": "Please enter a question first."}), 400

    input_result = check_input(prompt)
    result = {
        "input": {"category": input_result.category, "reason": input_result.reason},
        "model": MODEL,
        "model_attempted": False,
        "output": None,
        "response": None,
        "blocked": False,
        "error": None,
    }

    if input_result.category == "RESTRICT":
        result["blocked"] = True
        result["response"] = safe_fallback(input_result.reason)
        result["final_status"] = "blocked_at_input"
        return jsonify(result)

    result["model_attempted"] = True
    try:
        answer = generate_response(prompt)
    except LLMError as exc:
        result["blocked"] = True
        result["error"] = str(exc)
        result["response"] = safe_fallback("Local model unavailable.")
        result["final_status"] = "model_unavailable"
        return jsonify(result), 503

    output_result = check_output(answer)
    result["output"] = {"allowed": output_result.allowed, "reason": output_result.reason}
    if output_result.allowed:
        result["response"] = answer
        result["final_status"] = "allowed"
    else:
        result["blocked"] = True
        result["response"] = safe_fallback(output_result.reason)
        result["final_status"] = "blocked_at_output"
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
