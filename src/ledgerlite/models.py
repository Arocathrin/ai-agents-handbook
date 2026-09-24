from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Entry:
    """One ledger line. Amounts are Decimal, never float."""

    day: date
    category: str
    amount: Decimal
    currency: str = "INR"

    def to_dict(self) -> dict:
        return {
            "day": self.day.isoformat(),
            "category": self.category,
            "amount": str(self.amount),
            "currency": self.currency,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Entry:
        return cls(
            day=date.fromisoformat(d["day"]),
            category=d["category"],
            amount=Decimal(d["amount"]),
            currency=d["currency"],
        )


def _make_rule_id() -> str:
    """Return a new UUID4 string to use as a stable, unique rule identity."""
    return str(uuid.uuid4())


@dataclass(frozen=True)
class RecurringRule:
    """A recurring-entry rule.  Amounts are Decimal, never float."""

    rule_id: str
    category: str
    amount: Decimal
    day_of_month: int

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "category": self.category,
            "amount": str(self.amount),
            "day_of_month": self.day_of_month,
        }

    @classmethod
    def from_dict(cls, d: dict) -> RecurringRule:
        return cls(
            rule_id=d["rule_id"],
            category=d["category"],
            amount=Decimal(d["amount"]),
            day_of_month=int(d["day_of_month"]),
        )
