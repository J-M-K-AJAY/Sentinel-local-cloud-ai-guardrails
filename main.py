"""Main entry point for the cloud AI guardrails demo."""
from input_guardrail import check_input
from llm_client import generate_response, LLMError
from output_guardrail import check_output
from fallback_handler import safe_fallback


def main():
    print("=" * 60)
    print("AI GUARDRAILS FOR SECURE CLOUD COMPUTING OPERATIONS")
    print("Local model: Ollama + qwen2.5:0.5b-instruct")
    print("Educational demo only - no real cloud actions")
    print("=" * 60)

    while True:
        try:
            question = input(
                "\nEnter your cloud-security question (or 'exit'): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting safely.")
            break

        if question.lower() in {"exit", "quit"}:
            print("Demo ended.")
            break

        if not question:
            print("Please enter a question.")
            continue

        input_result = check_input(question)

        print(f"\n[Input Guardrail] Category: {input_result.category}")
        print(f"[Input Guardrail] Reason: {input_result.reason}")

        if input_result.category == "RESTRICT":
            print("\n[Final Response]")
            print(safe_fallback(input_result.reason))
            continue

        try:
            answer = generate_response(question)
        except LLMError as exc:
            print(f"\n[LLM Error] {exc}")
            print("\n[Final Response]")
            print(safe_fallback("Local model unavailable."))
            continue

        output_result = check_output(answer)

        print(
            f"\n[Output Guardrail] Allowed: "
            f"{output_result.allowed}"
        )
        print(f"[Output Guardrail] Reason: {output_result.reason}")

        print("\n[Final Response]")
        if output_result.allowed:
            print(answer)
        else:
            print(safe_fallback(output_result.reason))


if __name__ == "__main__":
    main()