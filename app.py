"""Handheld barcode scanner backend for warehouse intake and putaway."""

from flask import Flask, jsonify, request

from scanner.parser import BarcodeError, parse_gs1

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
