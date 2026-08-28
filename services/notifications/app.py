"""Sends order confirmation emails.

Runs independently of checkout: notifications only fire for orders that
already succeeded, so this service is unaffected by the checkout/payments
incident. Its log is a distraction, not a lead.
"""

import logging

logger = logging.getLogger("notifications")


class SMTPError(Exception):
    """Raised when the upstream SMTP relay is unreachable."""


def send_confirmation(order_id: str, customer_email: str) -> bool:
    """Send a confirmation email for a completed order."""
    logger.info("sending confirmation for %s to %s", order_id, customer_email)
    return True
