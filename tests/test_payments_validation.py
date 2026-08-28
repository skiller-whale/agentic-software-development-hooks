import pytest

from services.payments import validation


def test_validate_accepts_full_payload():
    payload = {
        "order_id": "ord_1",
        "amount_cents": 1000,
        "currency": "GBP",
        "card_token": "tok_visa",
    }
    validation.validate(payload)  # should not raise


def test_validate_rejects_missing_currency():
    payload = {
        "order_id": "ord_1",
        "amount_cents": 1000,
        "card_token": "tok_visa",
    }
    with pytest.raises(validation.ValidationError, match="currency"):
        validation.validate(payload)


def test_validate_rejects_missing_order_id():
    payload = {
        "amount_cents": 1000,
        "currency": "GBP",
        "card_token": "tok_visa",
    }
    with pytest.raises(validation.ValidationError, match="order_id"):
        validation.validate(payload)
