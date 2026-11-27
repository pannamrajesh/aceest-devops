#!/usr/bin/env sh
# usage: scripts/smoke_test.sh [base_url]
set -eu
BASE="${1:-http://localhost:5000}"

# wait for the app to come up (max ~30s)
i=0
until curl -fs "$BASE/health" >/dev/null 2>&1; do
  i=$((i + 1))
  if [ "$i" -ge 30 ]; then
    echo "app did not start at $BASE" >&2
    exit 1
  fi
  sleep 1
done

curl -fs "$BASE/health" | grep -q '"healthy"'
curl -fs "$BASE/programs" | grep -q 'Fat Loss'
curl -fs -X POST "$BASE/calories" -H 'Content-Type: application/json' \
  -d '{"weight": 70, "program": "Fat Loss (FL)"}' | grep -q '1540'

code=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$BASE/calories" \
  -H 'Content-Type: application/json' -d '{"weight": "abc", "program": "Fat Loss (FL)"}')
[ "$code" = "400" ] || { echo "expected 400 for bad weight, got $code" >&2; exit 1; }

echo "smoke test passed for $BASE"
