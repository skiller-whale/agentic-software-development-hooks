from unittest import mock

from services.gateway import app as gateway_app
from shared.models import Order


def make_order():
    return Order(
        order_id="ord_5",
        customer_id="cust_1",
        amount_cents=1500,
        currency="GBP",
        card_token="tok_visa",
    )


@mock.patch("services.gateway.app.checkout_app.checkout")
def test_handle_checkout_request_success(mock_checkout):
    mock_checkout.return_value = {
        "order_id": "ord_5",
        "payment_id": "pay_ord_5",
        "status": "confirmed",
    }
    response = gateway_app.handle_checkout_request(make_order())
    assert response["status"] == 200


@mock.patch("services.gateway.app.checkout_app.checkout")
def test_handle_checkout_request_failure(mock_checkout):
    mock_checkout.side_effect = RuntimeError("boom")
    response = gateway_app.handle_checkout_request(make_order())
    assert response["status"] == 502


@mock.patch("services.gateway.app.checkout_app.checkout")
def test_retries_on_transient_timeout(mock_checkout):
    # Flaky on CI — sometimes times out under load.
    mock_checkout.side_effect = TimeoutError("upstream timed out")
    response = gateway_app.handle_checkout_request(make_order())
    assert response["status"] == 502
