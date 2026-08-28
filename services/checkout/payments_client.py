"""Builds payment requests and sends them to the payments service."""

from services.payments import app as payments_app


def build_payment_payload(order) -> dict:
    """Build the payload sent to the payments service for this order."""
    return {
        "order_id": order.order_id,
        "amount_cents": order.amount_cents,
        "currency_code": order.currency,
        "card_token": order.card_token,
    }


def pay(order) -> dict:
    """Send an order's payment to the payments service."""
    payload = build_payment_payload(order)
    return payments_app.charge(payload)
