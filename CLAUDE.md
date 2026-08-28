# checkout-system

`services/` holds one directory per service (`gateway`, `checkout`,
`payments`, `notifications`), each with an `app.py`; `checkout` also has
`payments_client.py`, which builds the payload it sends to `payments`,
and `payments` also has `validation.py`, which checks that payload.
`shared/models.py` holds the data types used across services.
`migrations/` holds the SQL migrations for the underlying database.
