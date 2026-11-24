"""Output contract for the model, validated again in code."""

from __future__ import annotations

import jsonschema

TRIAGE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["risk", "missing_tests", "rationale"],
    "properties": {
        "risk": {"enum": ["low", "medium", "high"]},
        "missing_tests": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
        "rationale": {"type": "string", "maxLength": 400},
    },
}


def validate(obj: object) -> dict:
    jsonschema.validate(obj, TRIAGE_SCHEMA)
    return obj  # type: ignore[return-value]
