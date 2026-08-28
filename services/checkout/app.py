"""The checkout service: builds an order and takes payment for it."""

from services.checkout import payments_client


class CheckoutError(Exception):
    """Raised when a checkout cannot be completed."""


def checkout(order) -> dict:
    """Complete checkout for an order by taking payment.

    Raises CheckoutError if payment fails for any reason.
    """
    try:
        result = payments_client.pay(order)
    except Exception as exc:
        raise CheckoutError(str(exc)) from exc

    return {
        "order_id": order.order_id,
        "payment_id": result["payment_id"],
        "status": "confirmed",
    }
