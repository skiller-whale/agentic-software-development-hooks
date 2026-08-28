"""Shared data models used across the checkout services."""

from dataclasses import dataclass


@dataclass
class Order:
    """An order a customer is trying to check out."""

    order_id: str
    customer_id: str
    amount_cents: int
    currency: str
    card_token: str
