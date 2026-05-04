# warehouse-scanner

Handheld barcode scanner backend for warehouse intake and putaway. Python 3.12
with Flask; deployed per-warehouse on the edge cluster.

## Role at CargoCloud

Floor associates scan inbound parcels with Zebra handhelds. This service parses
GS1-128 labels, validates intake records, and forwards confirmed putaway counts
to [inventory-service](https://github.com/shipit-ai-demo-org/inventory-service)
(`PUT /v1/stock/{sku}`), which keeps the stock ledger that order reservations
draw from.

## API surface

```
GET  /healthz       liveness
POST /v1/scan       parse a raw GS1-128 barcode payload
POST /v1/intake     validate and accept an intake record
```

## Intake schema contract

`scanner/parser.py` declares `SCHEMA_VERSION` — the version of the intake
payload contract emitted downstream. CI runs `scripts/check_schema.py` on every
push and fails if the parser's version drifts from the version CI is certified
against. Bump both, deliberately, in the same change.

## Local development

```bash
pip install -r requirements.txt
flask --app app run --debug
python3 -m unittest discover tests
```
