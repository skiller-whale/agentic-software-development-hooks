import pytest

from services.payments import app as payments_app


def test_charge_succeeds_with_valid_payload():
    payload = {
        "order_id": "ord_2",
        "amount_cents": 2500,
        "currency": "GBP",
        "card_token": "tok_visa",
    }
    result = payments_app.charge(payload)
    assert result["status"] == "charged"
    assert result["order_id"] == "ord_2"


def test_charge_rejects_declined_card():
    payload = {
        "order_id": "ord_3",
        "amount_cents": 2500,
        "currency": "GBP",
        "card_token": "tok_declined",
    }
    with pytest.raises(payments_app.PaymentError):
        payments_app.charge(payload)


def test_charge_propagates_validation_error():
    payload = {
        "order_id": "ord_3b",
        "amount_cents": 2500,
        "card_token": "tok_visa",
    }
    with pytest.raises(payments_app.validation.ValidationError):
        payments_app.charge(payload)
