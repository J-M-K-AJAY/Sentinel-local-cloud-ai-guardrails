"""Safe fallback response for blocked content."""


def safe_fallback(reason: str = "") -> str:
    return (
        "Request stopped by the AI safety guardrails. "
        "I can help with defensive cloud security, "
        "access controls, and data protection instead."
    )