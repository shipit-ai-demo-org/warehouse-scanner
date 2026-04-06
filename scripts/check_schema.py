#!/usr/bin/env python3
"""CI guard for the intake schema contract.

The intake payload schema declared in scanner/parser.py is consumed by
inventory-service's WMS sync. A version bump that lands without consumer
certification silently corrupts stock counts, so CI pins the version it has
been certified against. Bump EXPECTED_SCHEMA_VERSION here in the same change
that updates the parser, after the consumer contract fixtures pass.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

EXPECTED_SCHEMA_VERSION = 2


def main() -> int:
    source = Path(__file__).resolve().parents[1] / "scanner" / "parser.py"
    text = source.read_text(encoding="utf-8")

    match = re.search(r"^SCHEMA_VERSION\s*=\s*(\d+)", text, re.MULTILINE)
    if not match:
        print("check_schema: SCHEMA_VERSION not found in scanner/parser.py")
        return 1

    actual = int(match.group(1))
    if actual != EXPECTED_SCHEMA_VERSION:
        print(
            f"check_schema: schema mismatch — parser.py declares v{actual} "
            f"but CI is certified for v{EXPECTED_SCHEMA_VERSION}. "
            "Update scripts/check_schema.py in the same change once the "
            "inventory-service contract fixtures are green."
        )
        return 1

    print(f"check_schema: OK (intake schema v{actual})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
