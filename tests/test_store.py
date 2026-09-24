import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from ledgerlite import store
from ledgerlite.models import Entry

# Resolve the fixtures directory relative to this file so tests work from any cwd.
FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_missing_file_is_empty(tmp_path):
    assert store.load(tmp_path / "nope.json") == []


def test_save_then_load(tmp_path):
    p = tmp_path / "ledger.json"
    entries = [
        Entry(date(2026, 1, 5), "rent", Decimal("15000")),
        Entry(date(2026, 1, 6), "food", Decimal("250.25")),
    ]
    store.save(p, entries)
    assert store.load(p) == entries


def test_corrupt_file_raises(tmp_path):
    p = tmp_path / "ledger.json"
    p.write_text("{not json", encoding="utf-8")
    assert store.load(p) == []  # robust loading


def test_migrate_v1_adds_currency_inr(tmp_path):
    """Loading a v1 fixture (no currency field) must yield entries with currency='INR'
    and saving must produce schema_version=2."""
    entries = store.load(FIXTURES / "ledger_v1.json")

    # All migrated entries must have currency defaulted to INR.
    assert len(entries) == 2
    for entry in entries:
        assert entry.currency == "INR"

    # Spot-check the actual data came through correctly.
    assert entries[0].category == "food"
    assert entries[0].amount == Decimal("350.00")
    assert entries[1].category == "transport"
    assert entries[1].amount == Decimal("80.50")

    # Saving the migrated entries must write schema_version=2.
    out = tmp_path / "migrated.json"
    store.save(out, entries)
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["schema_version"] == 2
    # Every entry in the written file must have a currency key.
    for raw in written["entries"]:
        assert raw["currency"] == "INR"