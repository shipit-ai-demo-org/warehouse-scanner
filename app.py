"""Handheld barcode scanner backend for warehouse intake and putaway."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/healthz")
def healthz():
    return jsonify(status="ok", service="warehouse-scanner")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
