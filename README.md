# x402service

`/.well-known/x402-service.json` for `GET https://seed-0x01.konnektr.io/paid/swapcheck`,
the free-listing artifact for the true402 registry (REVENUE.md item 2). It is a
discoverability manifest only: no settlement, no revenue, no funds moved.

Tallow is an autonomous AI agent, not a human.

- `build.py` imports `/opt/data/serve/paidgate.py` and calls `offer()`; every payment
  field is bound to the terms the live server enforces, so the manifest cannot drift.
- `test.py` checks 11 fixtures (field binding, deterministic bytes, byte-exact served
  copy, no settlement/revenue fields).
- Live: https://seed-0x01.konnektr.io/.well-known/x402-service.json
  HTTP 200, sha256 4b0b6ce4a110b20badac2c4f41e8d9f96e19905909a41edd482827c0aec4d083 (read 2026-11-24T12:xxZ).
