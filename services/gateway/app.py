"""The API gateway: the front door for checkout requests."""

from services.checkout import app as checkout_app


def handle_checkout_request(order) -> dict:
    """Route a checkout request to the checkout service.

    Returns a dict with a 'status' key mimicking an HTTP response:
    200 on success, 502 if the checkout service failed for any reason.
    """
    try:
        result = checkout_app.checkout(order)
    except Exception:
        return {"status": 502, "body": "Bad Gateway"}

    return {"status": 200, "body": result}
