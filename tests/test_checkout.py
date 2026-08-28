from unittest import mock

import pytest

from services.checkout import app as checkout_app
from shared.models import Order


def make_order(**overrides):
    defaults = dict(
        order_id="ord_4",
        customer_id="cust_1",
        amount_cents=3000,
        currency="GBP",
        card_token="tok_visa",
    )
    defaults.update(overrides)
    return Order(**defaults)


@mock.patch("services.checkout.app.payments_client.pay")
def test_checkout_succeeds(mock_pay):
    mock_pay.return_value = {
        "payment_id": "pay_ord_4",
        "order_id": "ord_4",
        "status": "charged",
    }
    result = checkout_app.checkout(make_order())
    assert result["status"] == "confirmed"
    assert result["payment_id"] == "pay_ord_4"


@mock.patch("services.checkout.app.payments_client.pay")
def test_checkout_raises_on_payment_failure(mock_pay):
    mock_pay.side_effect = RuntimeError("card declined")
    with pytest.raises(checkout_app.CheckoutError):
        checkout_app.checkout(make_order())
