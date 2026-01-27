"""Validation for intake and putaway requests submitted by handhelds."""

from __future__ import annotations

import re

# Bin locations look like AA01-B03-07: aisle, bay, shelf.
LOCATION_RE = re.compile(r"^[A-Z]{2}\d{2}-[A-Z]\d{2}-\d{2}$")
GTIN_RE = re.compile(r"^\d{14}$")


def gtin_check_digit_ok(gtin: str) -> bool:
    """Validate the GS1 mod-10 check digit on a 14-digit GTIN."""
    digits = [int(c) for c in gtin]
    body, check = digits[:-1], digits[-1]
    total = sum(d * (3 if idx % 2 == 0 else 1) for idx, d in enumerate(body))
    return (10 - total % 10) % 10 == check


def validate_intake(record: dict) -> list[str]:
    """Return a list of human-readable errors; empty means valid."""
    errors: list[str] = []

    gtin = str(record.get("gtin", ""))
    if not GTIN_RE.match(gtin):
        errors.append("gtin must be exactly 14 digits")
    elif not gtin_check_digit_ok(gtin):
        errors.append("gtin check digit is invalid")

    quantity = record.get("quantity")
    if not isinstance(quantity, int) or quantity <= 0:
        errors.append("quantity must be a positive integer")

    location = str(record.get("location", ""))
    if not LOCATION_RE.match(location):
        errors.append("location must match AA00-A00-00 bin format")

    return errors
