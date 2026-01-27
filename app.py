"""Handheld barcode scanner backend for warehouse intake and putaway."""

from flask import Flask, jsonify, request

from scanner.parser import BarcodeError, parse_gs1
from scanner.validators import validate_intake

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    return jsonify(status="ok", service="warehouse-scanner")


@app.post("/v1/scan")
def scan():
    payload = (request.get_json(silent=True) or {}).get("barcode", "")
    try:
        record = parse_gs1(payload)
    except BarcodeError as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(record)


@app.post("/v1/intake")
def intake():
    body = request.get_json(silent=True) or {}
    errors = validate_intake(body)
    if errors:
        return jsonify(errors=errors), 422
    # Confirmed counts are forwarded to inventory-service by the putaway
    # worker; the handheld only needs the ack.
    return jsonify(accepted=True, location=body.get("location")), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
