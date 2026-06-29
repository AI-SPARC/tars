from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

import jsonschema

SUPPORTED_MESSAGE_TYPES = {
    "order",
    "instantActions",
    "state",
    "visualization",
    "connection",
    "factsheet",
    "zoneSet",
    "responses",
}
SCHEMA_DIR = Path(__file__).parent / "schemas" / "v3_0_0"


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: list[str]


@lru_cache
def _load_schema(message_type: str) -> dict[str, Any]:
    schema_path = SCHEMA_DIR / f"{message_type}.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"VDA 5050 schema not found: {schema_path}")
    import json
    import re

    raw_schema = schema_path.read_text(encoding="utf-8")
    # The upstream VDA 5050 v3.0.0 schema files currently contain a few
    # JSON-with-comments style trailing commas. Keep the files verbatim for
    # traceability and normalize only while loading.
    normalized_schema = re.sub(r",\s*([}\]])", r"\1", raw_schema)
    return cast(dict[str, Any], json.loads(normalized_schema))


@lru_cache
def _validator(message_type: str) -> jsonschema.protocols.Validator:
    schema = _load_schema(message_type)
    cls = jsonschema.validators.validator_for(schema)
    cls.check_schema(schema)
    return cls(schema)


def validate_message(message_type: str, payload: dict[str, Any]) -> ValidationResult:
    if message_type not in SUPPORTED_MESSAGE_TYPES:
        return ValidationResult(False, [f"Unsupported VDA 5050 message type: {message_type}"])

    validator = _validator(message_type)
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    if not errors:
        return ValidationResult(True, [])

    return ValidationResult(False, [_format_error(error) for error in errors])


def _format_error(error: jsonschema.ValidationError) -> str:
    path = ".".join(str(part) for part in error.path)
    prefix = f"{path}: " if path else ""
    return f"{prefix}{error.message}"
