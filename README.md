# checkout-system

A small checkout system, split into four services that call each other
in-process (no real network, no real database):

- **gateway** — the front door. Routes a checkout request to `checkout`
  and returns 200 or 502.
- **checkout** — builds the order and asks `payments` to take payment,
  via `payments_client`.
- **payments** — validates and charges a payment request.
- **notifications** — sends confirmation emails. Independent of the
  other three.

`migrations/` holds the SQL migrations for the underlying database.

## Running the tests

```
python3 -m pytest -q
```
