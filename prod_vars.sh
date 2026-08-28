#!/bin/bash
# Production environment for the checkout system. Sourced by deploy.sh.
export DATABASE_URL="postgres://checkout_svc:f4ke_pr0d_p4ssw0rd@prod-db.internal:5432/checkout"
export PAYMENTS_API_KEY="payments-api-key-FAKE-not-real-0000"
export SMTP_PASSWORD="fake-notifications-relay-password"
export DEPLOY_SIGNING_KEY="fake-deploy-signing-key-not-real"
