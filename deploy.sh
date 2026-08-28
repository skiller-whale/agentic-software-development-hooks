#!/bin/bash
# Deploys the checkout system to production.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$DIR/prod_vars.sh"

echo "Deploying checkout system to production..."
echo "Target database: ${DATABASE_URL}"
echo "(this is a placeholder — wire up the real deploy steps here)"
