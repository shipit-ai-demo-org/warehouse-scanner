"""Unit tests for the GS1-128 intake parser."""

import unittest

from scanner.parser import GS, SCHEMA_VERSION, BarcodeError, parse_gs1


class ParseGS1Tests(unittest.TestCase):
    def test_parses_gtin_and_quantity(self):
        record = parse_gs1("0100614141123452" + "3024")
        self.assertEqual(record["gtin"], "00614141123452")
        self.assertEqual(record["quantity"], 24)

    def test_includes_schema_version(self):
        record = parse_gs1("0100614141123452")
        self.assertEqual(record["schema_version"], SCHEMA_VERSION)

    def test_variable_field_terminated_by_group_separator(self):
        record = parse_gs1("21SER123" + GS + "3012")
        self.assertEqual(record["serial"], "SER123")
        self.assertEqual(record["quantity"], 12)

    def test_rejects_empty_payload(self):
        with self.assertRaises(BarcodeError):
            parse_gs1("")

    def test_rejects_unknown_ai(self):
        with self.assertRaises(BarcodeError):
            parse_gs1("9912345")

    def test_rejects_truncated_gtin(self):
        with self.assertRaises(BarcodeError):
            parse_gs1("01123")

    def test_rejects_non_numeric_quantity(self):
        with self.assertRaises(BarcodeError):
            parse_gs1("30abc")


if __name__ == "__main__":
    unittest.main()
