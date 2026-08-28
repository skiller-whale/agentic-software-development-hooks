"""The payments service: validates and charges a payment request."""

from services.payments import validation

DECLINED_TOKENS = {"tok_declined"}

# Refunds issued so far, in cents, keyed by order id.
REFUNDS_CENTS = {
    "ord_2": [500],
    "ord_5": [200, 300],
}


class PaymentError(Exception):
    """Raised when a validated payment cannot be charged."""


def charge(payload: dict) -> dict:
    """Validate and charge a payment payload.

    Raises ValidationError if the payload is malformed, or PaymentError
    if the card is declined. Returns a dict describing the charge.
    """
    validation.validate(payload)

    if payload["card_token"] in DECLINED_TOKENS:
        raise PaymentError(f"card declined (order={payload['order_id']})")

    return {
        "payment_id": f"pay_{payload['order_id']}",
        "order_id": payload["order_id"],
        "status": "charged",
    }
