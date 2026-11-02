"""Rule-based output validation."""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class OutputResult:
    allowed: bool
    reason: str


BLOCK_PATTERNS = [
    r"\bhere is how to steal\b",
    r"\bsteal (?:passwords|credentials|credit cards)\b",
    r"\bexfiltrate (?:customer|private|sensitive) data\b",
    r"\bbypass (?:security|authentication) controls\b",
]


def check_output(text: str) -> OutputResult:
    if not text or not text.strip():
        return OutputResult(False, "Empty response.")

    for pattern in BLOCK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return OutputResult(
                False, "Potentially unsafe content detected."
            )

    return OutputResult(
        True, "No configured unsafe-output rule was triggered."
    )