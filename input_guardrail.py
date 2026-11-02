
"""Rule-based input guardrails for a local cloud-security assistant."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class InputResult:
    category: str
    reason: str


MAX_INPUT_LENGTH = 1000

SENSITIVE_PATTERNS = [
    r"\b(personal|private|confidential|sensitive)\s+"
    r"(information|data|details|records)\b",

    r"\b(credit card|cardholder|payment)\s+"
    r"(details|data|information|credentials)\b",

    r"\b(passwords?|api keys?|access tokens?|secret keys?)\b",

    r"\b(customer|patient|employee)\s+"
    r"(records|data|details|information)\b",
]

RESTRICT_PATTERNS = [
    r"\b(steal|exfiltrate|dump)\b.{0,100}"
    r"\b(credentials?|passwords?|tokens?|secrets?|private data)\b",
    r"\b(bypass|evade|disable|circumvent)\b.{0,60}"
    r"\b(security|authentication|access controls?|protection)\b",

    r"\b(steal|hack|break into|gain unauthorized access)\b",

    r"\b(retrieve|obtain|access|extract)\b.{0,100}"
    r"\b(credit cards?|payment details|credentials?|passwords?)\b",

    r"\b(credit card credentials?|payment credentials?)\b",

    r"\b(retrieve|obtain|access|extract|download|export|view|read|"
    r"query|collect|copy)\b.{0,200}"
    r"\b(credit card|cardholder|payment information|payment details|"
    r"customer records|customer data|personal details|personal data|"
    r"confidential records|private data|sensitive data)\b"
    r".{0,200}"
    r"\b(without authorization|without authorisation|without permission|"
    r"unauthorized|unauthorised|illegally|illicitly)\b",
]


def check_input(user_input: str) -> InputResult:
    """Classify a request before it reaches the local model."""

    if not isinstance(user_input, str):
        return InputResult("RESTRICT", "Invalid input type.")

    text = user_input.strip()

    if not text:
        return InputResult("RESTRICT", "Empty input is not permitted.")

    if len(text) > MAX_INPUT_LENGTH:
        return InputResult("RESTRICT", "Input exceeds the permitted length.")

    for pattern in RESTRICT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            return InputResult(
                "RESTRICT",
                "Potentially harmful or unauthorised activity detected.",
            )

    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return InputResult(
                "SENSITIVE",
                "Potentially sensitive information detected.",
            )

    return InputResult("ALLOW", "No configured input rule was triggered.")
