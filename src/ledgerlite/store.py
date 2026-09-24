from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from .models import Entry

SCHEMA_VERSION = 3

# Maps a schema version to the function that upgrades a raw file dict to the next version.
MIGRATIONS: dict[int, Callable[[dict], dict]] = {}


def _migrate_v1_to_v2(data: dict) -> dict:
    """Add currency field (default 'INR') to every entry that lacks it."""
    for entry in data.get("entries", []):
        if "currency" not in entry:
            entry["currency"] = "INR"
    return data


def _migrate_v2_to_v3(data: dict) -> dict:
    """Add recurring_rules and applied_recurring top-level keys if absent."""
    if "recurring_rules" not in data:
        data["recurring_rules"] = []
    if "applied_recurring" not in data:
        data["applied_recurring"] = []
    return data


MIGRATIONS[1] = _migrate_v1_to_v2
MIGRATIONS[2] = _migrate_v2_to_v3


def _migrate(data: dict) -> dict:
    version = data.get("schema_version", 1)
    while version < SCHEMA_VERSION:
        data = MIGRATIONS[version](data)
        version += 1
        data["schema_version"] = version
    return data


# ---------------------------------------------------------------------------
# LedgerData — full ledger representation including recurring-entry state
# ---------------------------------------------------------------------------

@dataclass
class LedgerData:
    """Full on-disk ledger: entries plus recurring-entry bookkeeping."""

    entries: list[Entry] = field(default_factory=list)
    recurring_rules: list = field(default_factory=list)
    applied_recurring: list = field(default_factory=list)


def load_ledger(path: Path) -> LedgerData:
    """Load the full ledger.  A missing file returns an empty LedgerData.
    A corrupt file is treated robustly and returns an empty LedgerData."""
    if not path.exists():
        return LedgerData()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        data = _migrate(data)
        return LedgerData(
            entries=[Entry.from_dict(d) for d in data["entries"]],
            recurring_rules=data.get("recurring_rules", []),
            applied_recurring=data.get("applied_recurring", []),
        )
    except Exception:
        return LedgerData()


def save_ledger(path: Path, ledger: LedgerData) -> None:
    """Persist a LedgerData to *path* atomically."""
    payload = {
        "schema_version": SCHEMA_VERSION,
        "entries": [e.to_dict() for e in ledger.entries],
        "recurring_rules": ledger.recurring_rules,
        "applied_recurring": ledger.applied_recurring,
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Legacy entry-only API — preserved for backward compatibility
# ---------------------------------------------------------------------------

def load(path: Path) -> list[Entry]:
    """Load entries only.  A missing file is an empty ledger."""
    return load_ledger(path).entries


def save(path: Path, entries: list[Entry]) -> None:
    """Save entries only (no recurring state).  Writes schema_version=SCHEMA_VERSION."""
    save_ledger(path, LedgerData(entries=entries))
