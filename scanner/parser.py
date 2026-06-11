"""GS1-128 barcode parsing for warehouse intake scans.

SCHEMA_VERSION is the version of the intake payload contract emitted to
inventory-service. Bumps must be deliberate and paired with consumer-side
certification — CI enforces this via scripts/check_schema.py.
"""

from __future__ import annotations

SCHEMA_VERSION = 3

GS = "\x1d"  # FNC1 group separator

# GS1 application identifiers accepted on intake labels.
# AI -> (field name, fixed length or None for variable-length)
SUPPORTED_AIS = {
    "01": ("gtin", 14),
    "10": ("lot", None),  # schema v2: lot/batch tracking for recalls
    "21": ("serial", None),
    "30": ("quantity", None),
    "37": ("tote_count", None),  # schema v3: multi-tote putaway
}


class BarcodeError(ValueError):
    """Raised when a scanned payload cannot be parsed."""


def parse_gs1(payload: str) -> dict:
    """Parse a GS1-128 element string into an intake record.

    Variable-length fields are terminated by the FNC1 group separator or end
    of payload, per the GS1 General Specifications.
    """
    if not payload:
        raise BarcodeError("empty barcode payload")

    fields: dict[str, object] = {"schema_version": SCHEMA_VERSION}
    i = 0
    while i < len(payload):
        ai = payload[i : i + 2]
        if ai not in SUPPORTED_AIS:
            raise BarcodeError(f"unsupported application identifier {ai!r}")
        name, fixed = SUPPORTED_AIS[ai]
        i += 2

        if fixed is not None:
            value = payload[i : i + fixed]
            if len(value) < fixed:
                raise BarcodeError(f"truncated value for AI {ai}")
            i += fixed
        else:
            end = payload.find(GS, i)
            if end == -1:
                end = len(payload)
            value = payload[i:end]
            i = end + 1

        fields[name] = value

    if "quantity" in fields:
        try:
            fields["quantity"] = int(fields["quantity"])
        except ValueError as exc:
            raise BarcodeError("quantity is not numeric") from exc

    return fields
