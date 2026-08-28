# Changelog

## v2.14.0 — Use ISO field naming in payment payload (currency → currency_code)

Renamed the `currency` field to `currency_code` in the payload
`checkout` sends to `payments`, to line up with the ISO 4217 field
naming we use elsewhere.

## v2.13.2

Fixed a retry bug in `payments_client` where a declined card was
retried instead of failing immediately.

## v2.13.1

Added `notifications` as a separate service so a slow SMTP relay can no
longer delay checkout.

## v2.13.0

Initial split of the monolith into `gateway`, `checkout`, `payments`
and `notifications`.
