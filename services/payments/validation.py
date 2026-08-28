"""Validation for incoming payment requests."""

REQUIRED_FIELDS = ["order_id", "amount_cents", "currency", "card_token"]


class ValidationError(Exception):
    """Raised when a payment payload is missing a required field."""


def validate(payload: dict) -> None:
    """Check a payment payload has every required field.

    Raises ValidationError naming the first missing field.
    """
    for field in REQUIRED_FIELDS:
        if field not in payload:
            raise ValidationError(f"missing required field: {field}")
