"""Pure recurring-entry business logic.

All functions are pure with respect to the filesystem: they accept and
return plain Python objects.  Persistence is handled by store.py.

Public API
----------
validate_recur_add(category, amount_str, day_of_month) -> list[str]
add_rule(ledger, category, amount_str, day_of_month)   -> LedgerData
validate_apply(rules, year, month)                     -> list[dict]
apply_rules(ledger, year, month)                       -> tuple[LedgerData, int]
"""
from __future__ import annotations

import calendar
from datetime import date
from decimal import Decimal, InvalidOperation

from .models import Entry, RecurringRule, _make_rule_id
from .store import LedgerData

# ---------------------------------------------------------------------------
# validate_recur_add
# ---------------------------------------------------------------------------

def validate_recur_add(
    category: str,
    amount_str: str,
    day_of_month: int,
) -> list[str]:
    """Validate inputs for 'recur add'.

    Returns a list of human-readable error strings.  An empty list means all
    inputs are valid.  All errors are collected before returning (no early exit).
    """
    errors: list[str] = []

    if not category.strip():
        errors.append("category is required and must not be blank")

    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            errors.append("amount must be a positive decimal value")
    except InvalidOperation:
        errors.append(f"amount '{amount_str}' is not a valid decimal number")

    if not (1 <= day_of_month <= 31):
        errors.append(
            f"day-of-month must be between 1 and 31, got {day_of_month}"
        )

    return errors


# ---------------------------------------------------------------------------
# add_rule
# ---------------------------------------------------------------------------

def add_rule(
    ledger: LedgerData,
    category: str,
    amount_str: str,
    day_of_month: int,
) -> LedgerData:
    """Append a new RecurringRule to ledger.recurring_rules.

    Returns a new LedgerData with the rule appended.  Does not validate inputs;
    callers must call validate_recur_add first and handle any errors.
    """
    rule = RecurringRule(
        rule_id=_make_rule_id(),
        category=category,
        amount=Decimal(amount_str),
        day_of_month=day_of_month,
    )
    return LedgerData(
        entries=list(ledger.entries),
        recurring_rules=list(ledger.recurring_rules) + [rule.to_dict()],
        applied_recurring=list(ledger.applied_recurring),
    )


# ---------------------------------------------------------------------------
# validate_apply
# ---------------------------------------------------------------------------

def validate_apply(
    rules: list[RecurringRule],
    year: int,
    month: int,
) -> list[dict]:
    """Check that every rule's day_of_month exists in the requested year/month.

    Returns a list of dicts describing invalid rules.  Each dict has keys:
        - "category"    : str
        - "day_of_month": int
    An empty list means all rules are calendar-valid for the requested month.
    All invalid rules are collected (no early exit).
    """
    _, days_in_month = calendar.monthrange(year, month)
    errors: list[dict] = []
    for rule in rules:
        if rule.day_of_month > days_in_month:
            errors.append(
                {"category": rule.category, "day_of_month": rule.day_of_month}
            )
    return errors


# ---------------------------------------------------------------------------
# apply_rules
# ---------------------------------------------------------------------------

def _make_token(rule_id: str, year: int, month: int) -> str:
    """Idempotency token: stable string combining rule identity with year-month."""
    return f"{rule_id}:{year}-{month:02d}"


def apply_rules(
    ledger: LedgerData,
    year: int,
    month: int,
) -> tuple[LedgerData, int]:
    """Apply all recurring rules for the given year/month.

    Returns (updated_ledger, count_of_entries_added).

    Raises ValueError if any rule has a day_of_month that does not exist in
    the requested month (REQ-06 all-or-nothing: one bad rule blocks all).

    Idempotency (REQ-04): a rule that has already been applied for this
    year/month (token present in applied_recurring) is silently skipped.
    """
    # Deserialise rules from their stored dict form.
    rules = [RecurringRule.from_dict(r) for r in ledger.recurring_rules]

    # REQ-05: no rules → nothing to do.
    if not rules:
        return LedgerData(
            entries=list(ledger.entries),
            recurring_rules=list(ledger.recurring_rules),
            applied_recurring=list(ledger.applied_recurring),
        ), 0

    # REQ-06: calendar check — all-or-nothing.
    calendar_errors = validate_apply(rules, year, month)
    if calendar_errors:
        bad = ", ".join(
            f"{e['category']} (day {e['day_of_month']})" for e in calendar_errors
        )
        raise ValueError(
            f"recur apply {year}-{month:02d}: the following rules have an invalid "
            f"day for this month: {bad}"
        )

    # Apply rules that have not already been applied for this year/month.
    applied_set: set[str] = set(ledger.applied_recurring)
    new_entries: list[Entry] = []
    new_tokens: list[str] = []

    for rule in rules:
        token = _make_token(rule.rule_id, year, month)
        if token in applied_set:
            continue  # already applied — idempotent skip
        entry = Entry(
            day=date(year, month, rule.day_of_month),
            category=rule.category,
            amount=rule.amount,
            currency="INR",
        )
        new_entries.append(entry)
        new_tokens.append(token)

    return LedgerData(
        entries=list(ledger.entries) + new_entries,
        recurring_rules=list(ledger.recurring_rules),
        applied_recurring=list(ledger.applied_recurring) + new_tokens,
    ), len(new_entries)
