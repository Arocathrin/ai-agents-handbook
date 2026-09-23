from __future__ import annotations

import argparse
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

from . import report, store
from .models import Entry

DEFAULT_LEDGER = Path("ledger.json")


def _validate_add(category: str, amount: str) -> int | None:
    """Validate add inputs. Returns exit code on failure, None on success."""
    if not category.strip():
        print("error: category is required", file=sys.stderr)
        return 2
    try:
        amt = Decimal(amount)
    except Exception:
        print("error: amount must be positive", file=sys.stderr)
        return 2
    if amt <= 0:
        print("error: amount must be positive", file=sys.stderr)
        return 2
    return None


def cmd_add(args: argparse.Namespace) -> int:
    code = _validate_add(args.category, args.amount)
    if code is not None:
        return code
    entries = store.load(args.ledger)
    day = date.fromisoformat(args.day)
    entry = Entry(day=day, category=args.category, amount=Decimal(args.amount))
    entries.append(entry)
    store.save(args.ledger, entries)
    print(f"added {args.category} {args.amount} on {args.day}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    entries = sorted(store.load(args.ledger), key=lambda e: e.day)
    if args.last:
        entries = entries[-args.last :]
    for e in entries:
        print(f"{e.day.isoformat()}  {e.category:<16}{e.amount:>12.2f}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    entries = store.load(args.ledger)
    month_entries = report.entries_in_month(entries, args.year, args.month)
    print(report.format_report(args.year, args.month, report.totals_by_category(month_entries)))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ledgerlite", description="Tiny expense ledger.")
    p.add_argument(
        "--ledger", type=Path, default=DEFAULT_LEDGER, help="ledger file (default: ledger.json)"
    )
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add", help="add an entry")
    a.add_argument("--day", default=date.today().isoformat())
    a.add_argument("--category", required=True)
    a.add_argument("--amount", required=True)
    a.set_defaults(func=cmd_add)

    ls = sub.add_parser("list", help="list entries")
    ls.add_argument("--last", type=int, default=0, help="show only the last N entries")
    ls.set_defaults(func=cmd_list)

    r = sub.add_parser("report", help="monthly totals by category")
    r.add_argument("--year", type=int, required=True)
    r.add_argument("--month", type=int, required=True)
    r.set_defaults(func=cmd_report)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
