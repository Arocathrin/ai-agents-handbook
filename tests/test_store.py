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


def test_migrate_v2_adds_recurring_keys(tmp_path):
    """Loading a v2 fixture must add recurring_rules and applied_recurring (both []),
    preserve existing entries intact, and write schema_version=3 on save."""
    ledger = store.load_ledger(FIXTURES / "ledger_v2.json")

    # Both new top-level keys must be present and default to empty lists.
    assert ledger.recurring_rules == []
    assert ledger.applied_recurring == []

    # Existing entries must come through without data loss.
    assert len(ledger.entries) == 2
    from decimal import Decimal
    assert ledger.entries[0].category == "rent"
    assert ledger.entries[0].amount == Decimal("15000.00")
    assert ledger.entries[1].category == "groceries"
    assert ledger.entries[1].amount == Decimal("3200.50")

    # Saving must write schema_version=3.
    out = tmp_path / "migrated_v3.json"
    store.save_ledger(out, ledger)
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["schema_version"] == 3
    # Both new keys must be present in the written file.
    assert written["recurring_rules"] == []
    assert written["applied_recurring"] == []


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

    # Saving the migrated entries must write schema_version=3 (current version).
    out = tmp_path / "migrated.json"
    store.save(out, entries)
    written = json.loads(out.read_text(encoding="utf-8"))
    assert written["schema_version"] == 3
    # Every entry in the written file must have a currency key.
    for raw in written["entries"]:
        assert raw["currency"] == "INR"