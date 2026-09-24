"""Tests for Task 2: RecurringRule model and pure recur logic.

All tests are written against the public contracts defined in
requirements.md and tasks.md.  Implementation files do not exist yet;
running this file before Task 2 is implemented is the expected red state.

Imports:
  ledgerlite.models  - RecurringRule, _make_rule_id
  ledgerlite.recur   - validate_recur_add, add_rule, validate_apply, apply_rules
  ledgerlite.store   - LedgerData (already implemented in Task 1)
"""
from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

import pytest

from ledgerlite.models import RecurringRule, _make_rule_id
from ledgerlite.recur import add_rule, apply_rules, validate_apply, validate_recur_add
from ledgerlite.store import LedgerData

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _empty_ledger() -> LedgerData:
    return LedgerData()


def _ledger_with_rule(
    category: str = "rent",
    amount: str = "5000",
    day: int = 1,
) -> LedgerData:
    """Return a LedgerData that already contains one rule."""
    rule = RecurringRule(
        rule_id=_make_rule_id(),
        category=category,
        amount=Decimal(amount),
        day_of_month=day,
    )
    return LedgerData(
        entries=[],
        recurring_rules=[rule.to_dict()],
        applied_recurring=[],
    )


# ===========================================================================
# Model — RecurringRule
# ===========================================================================

def test_recurring_rule_roundtrip():
    """to_dict / from_dict must round-trip without data loss."""
    rule = RecurringRule(
        rule_id=_make_rule_id(),
        category="groceries",
        amount=Decimal("3200.50"),
        day_of_month=5,
    )
    assert RecurringRule.from_dict(rule.to_dict()) == rule


def test_recurring_rule_amount_is_decimal():
    """Amount must survive a round-trip as Decimal, not float."""
    rule = RecurringRule(
        rule_id=_make_rule_id(),
        category="groceries",
        amount=Decimal("0.10"),
        day_of_month=10,
    )
    restored = RecurringRule.from_dict(rule.to_dict())
    # Decimal arithmetic must be exact — float would give a rounding error here.
    assert restored.amount + Decimal("0.20") == Decimal("0.30")


# ===========================================================================
# Model — _make_rule_id
# ===========================================================================

def test_make_rule_id_is_uuid():
    """_make_rule_id must return a string that is a valid UUID4."""
    rule_id = _make_rule_id()
    parsed = uuid.UUID(rule_id)   # raises ValueError if malformed
    assert parsed.version == 4


def test_make_rule_id_two_calls_distinct():
    """Two consecutive calls must produce different IDs."""
    assert _make_rule_id() != _make_rule_id()


# ===========================================================================
# Validation — validate_recur_add
# ===========================================================================

def test_validate_add_empty_category():
    errors = validate_recur_add("", "100", 1)
    assert any("category" in e.lower() for e in errors)


def test_validate_add_whitespace_category():
    errors = validate_recur_add("   ", "100", 1)
    assert any("category" in e.lower() for e in errors)


def test_validate_add_zero_amount():
    errors = validate_recur_add("food", "0", 1)
    assert any("amount" in e.lower() for e in errors)


def test_validate_add_negative_amount():
    errors = validate_recur_add("food", "-50", 1)
    assert any("amount" in e.lower() for e in errors)


def test_validate_add_non_decimal_amount():
    errors = validate_recur_add("food", "not-a-number", 1)
    assert any("amount" in e.lower() for e in errors)


def test_validate_add_day_zero():
    errors = validate_recur_add("food", "100", 0)
    assert any("day" in e.lower() for e in errors)


def test_validate_add_day_32():
    errors = validate_recur_add("food", "100", 32)
    assert any("day" in e.lower() for e in errors)


def test_validate_add_valid():
    """All-valid inputs must return an empty error list."""
    errors = validate_recur_add("rent", "15000", 1)
    assert errors == []


def test_validate_add_all_errors_collected():
    """A call with multiple bad inputs must report all errors, not just the first."""
    errors = validate_recur_add("", "-1", 0)
    # Must mention category, amount, and day — three distinct problems.
    lowered = " ".join(errors).lower()
    assert "category" in lowered
    assert "amount" in lowered
    assert "day" in lowered


# ===========================================================================
# Rule creation — add_rule
# ===========================================================================

def test_add_rule_persists_rule():
    """add_rule must append exactly one rule to ledger.recurring_rules."""
    ledger = _empty_ledger()
    updated = add_rule(ledger, "rent", "15000", 1)
    assert len(updated.recurring_rules) == 1


def test_add_rule_amount_is_decimal():
    """The stored rule's amount must round-trip as Decimal."""
    ledger = _empty_ledger()
    updated = add_rule(ledger, "food", "0.10", 5)
    rule = RecurringRule.from_dict(updated.recurring_rules[0])
    assert rule.amount + Decimal("0.20") == Decimal("0.30")


def test_add_rule_id_is_uuid():
    """add_rule must assign a UUID4 rule_id to the new rule."""
    ledger = _empty_ledger()
    updated = add_rule(ledger, "food", "100", 5)
    rule = RecurringRule.from_dict(updated.recurring_rules[0])
    parsed = uuid.UUID(rule.rule_id)
    assert parsed.version == 4


def test_add_rule_two_calls_distinct_ids():
    """Two separate add_rule calls must produce rules with different IDs."""
    ledger = _empty_ledger()
    ledger = add_rule(ledger, "rent", "5000", 1)
    ledger = add_rule(ledger, "food", "2000", 5)
    ids = [RecurringRule.from_dict(r).rule_id for r in ledger.recurring_rules]
    assert ids[0] != ids[1]


# ===========================================================================
# Calendar validation — validate_apply
# ===========================================================================

def test_validate_apply_valid_dates():
    """Rules with valid dates for the target month must produce no errors."""
    rules = [
        RecurringRule(
            rule_id=_make_rule_id(),
            category="rent",
            amount=Decimal("5000"),
            day_of_month=1,
        ),
        RecurringRule(
            rule_id=_make_rule_id(),
            category="food",
            amount=Decimal("2000"),
            day_of_month=28,
        ),
    ]
    errors = validate_apply(rules, year=2026, month=2)  # Feb 2026 has 28 days
    assert errors == []


def test_validate_apply_day_31_in_april():
    """Day 31 does not exist in April; validate_apply must flag it."""
    rules = [
        RecurringRule(
            rule_id=_make_rule_id(),
            category="rent",
            amount=Decimal("5000"),
            day_of_month=31,
        ),
    ]
    errors = validate_apply(rules, year=2026, month=4)
    assert len(errors) == 1
    err = errors[0]
    assert "rent" in err["category"]
    assert err["day_of_month"] == 31


def test_validate_apply_day_29_non_leap():
    """Day 29 does not exist in February of a non-leap year."""
    rules = [
        RecurringRule(
            rule_id=_make_rule_id(),
            category="gym",
            amount=Decimal("800"),
            day_of_month=29,
        ),
    ]
    errors = validate_apply(rules, year=2026, month=2)  # 2026 is not a leap year
    assert len(errors) == 1
    assert errors[0]["day_of_month"] == 29


def test_validate_apply_multiple_invalid():
    """All invalid rules must be reported, not just the first."""
    rules = [
        RecurringRule(
            rule_id=_make_rule_id(),
            category="a",
            amount=Decimal("1"),
            day_of_month=31,
        ),
        RecurringRule(
            rule_id=_make_rule_id(),
            category="b",
            amount=Decimal("1"),
            day_of_month=30,
        ),
    ]
    # April has 30 days: day 31 is bad, day 30 is fine.
    errors_april = validate_apply(rules, year=2026, month=4)
    assert len(errors_april) == 1  # only the day-31 rule is invalid in April

    # February 2026 has 28 days: both 31 and 30 are bad.
    errors_feb = validate_apply(rules, year=2026, month=2)
    assert len(errors_feb) == 2


def test_validate_apply_one_bad_blocks_all():
    """REQ-06: one invalid rule must block the entire apply_rules invocation.

    apply_rules must raise ValueError when validate_apply reports any errors
    so that no entries are written even for otherwise-valid rules.
    """
    rent_rule = RecurringRule(
        rule_id=_make_rule_id(),
        category="rent",
        amount=Decimal("5000"),
        day_of_month=1,
    )
    gym_rule = RecurringRule(
        rule_id=_make_rule_id(),
        category="gym",
        amount=Decimal("800"),
        day_of_month=31,  # invalid for April
    )
    ledger = LedgerData(
        entries=[],
        recurring_rules=[rent_rule.to_dict(), gym_rule.to_dict()],
        applied_recurring=[],
    )
    # April has 30 days, so gym (day 31) is invalid — both rules must be blocked.
    with pytest.raises(ValueError):
        apply_rules(ledger, year=2026, month=4)


# ===========================================================================
# Application — apply_rules
# ===========================================================================

def test_apply_creates_entry():
    """apply_rules must append one Entry per rule to ledger.entries."""
    ledger = _ledger_with_rule(category="rent", amount="15000", day=1)
    updated, count = apply_rules(ledger, year=2026, month=3)
    assert count == 1
    assert len(updated.entries) == 1
    assert updated.entries[0].day == date(2026, 3, 1)
    assert updated.entries[0].category == "rent"


def test_apply_amount_is_decimal():
    """The created entry's amount must be Decimal, not float."""
    ledger = _ledger_with_rule(category="food", amount="0.10", day=5)
    updated, _ = apply_rules(ledger, year=2026, month=3)
    assert updated.entries[0].amount + Decimal("0.20") == Decimal("0.30")


def test_apply_currency_is_inr():
    """REQ-03: the created entry's currency must be 'INR'."""
    ledger = _ledger_with_rule(category="food", amount="100", day=5)
    updated, _ = apply_rules(ledger, year=2026, month=3)
    assert updated.entries[0].currency == "INR"


def test_apply_token_recorded():
    """apply_rules must record an idempotency token in applied_recurring."""
    ledger = _ledger_with_rule(category="rent", amount="5000", day=1)
    updated, _ = apply_rules(ledger, year=2026, month=3)
    assert len(updated.applied_recurring) == 1


def test_apply_no_rules_returns_zero_count():
    """REQ-05: with no rules, apply_rules must return count=0 and leave ledger untouched."""
    ledger = _empty_ledger()
    updated, count = apply_rules(ledger, year=2026, month=3)
    assert count == 0
    assert updated.entries == []
    assert updated.applied_recurring == []


# ===========================================================================
# Idempotency — apply_rules
# ===========================================================================

def test_apply_idempotent_same_month():
    """REQ-04: applying the same rule twice for the same month adds only one entry."""
    ledger = _ledger_with_rule(category="rent", amount="5000", day=1)
    ledger, _ = apply_rules(ledger, year=2026, month=3)
    ledger, count2 = apply_rules(ledger, year=2026, month=3)
    assert count2 == 0                 # second call is a no-op
    assert len(ledger.entries) == 1    # still only one entry


def test_apply_idempotent_different_month():
    """Applying to a different month must still create a new entry."""
    ledger = _ledger_with_rule(category="rent", amount="5000", day=1)
    ledger, _ = apply_rules(ledger, year=2026, month=3)
    ledger, count2 = apply_rules(ledger, year=2026, month=4)
    assert count2 == 1                 # different month → new entry
    assert len(ledger.entries) == 2


def test_apply_idempotent_cross_process(tmp_path):
    """REQ-04: idempotency must survive a save/load round-trip (cross-process scenario)."""
    from ledgerlite import store

    ledger_path = tmp_path / "ledger.json"

    # First 'process': add rule, apply for March, save.
    ledger = _ledger_with_rule(category="rent", amount="5000", day=1)
    ledger, _ = apply_rules(ledger, year=2026, month=3)
    store.save_ledger(ledger_path, ledger)

    # Second 'process': reload, apply for March again — must be a no-op.
    reloaded = store.load_ledger(ledger_path)
    reloaded, count2 = apply_rules(reloaded, year=2026, month=3)
    assert count2 == 0
    assert len(reloaded.entries) == 1
