from datetime import date
from decimal import Decimal

from ledgerlite.models import Entry


def test_roundtrip():
    e = Entry(day=date(2026, 3, 14), category="food", amount=Decimal("120.50"))
    assert Entry.from_dict(e.to_dict()) == e


def test_amount_is_decimal_not_float():
    e = Entry.from_dict({"day": "2026-01-01", "category": "x", "amount": "0.10", "currency": "INR"})
    assert e.amount + Decimal("0.20") == Decimal("0.30")


def test_currency_defaults_to_inr():
    """Entry created without explicit currency must default to 'INR'."""
    e = Entry(day=date(2026, 6, 1), category="food", amount=Decimal("50"))
    assert e.currency == "INR"


def test_currency_explicit_value():
    """Entry accepts a non-default currency value."""
    e = Entry(day=date(2026, 6, 1), category="food", amount=Decimal("50"), currency="USD")
    assert e.currency == "USD"


def test_to_dict_includes_currency():
    """to_dict must serialise the currency field."""
    e = Entry(day=date(2026, 6, 1), category="food", amount=Decimal("50"), currency="EUR")
    d = e.to_dict()
    assert d["currency"] == "EUR"


def test_from_dict_reads_currency():
    """from_dict must read the currency key directly (no silent default)."""
    e = Entry.from_dict(
        {"day": "2026-06-01", "category": "food", "amount": "50", "currency": "GBP"}
    )
    assert e.currency == "GBP"


def test_roundtrip_preserves_currency():
    """A full round-trip through to_dict / from_dict must preserve a non-default currency."""
    e = Entry(day=date(2026, 6, 1), category="travel", amount=Decimal("200"), currency="USD")
    assert Entry.from_dict(e.to_dict()) == e
