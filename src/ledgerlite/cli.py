from __future__ import annotations

import argparse
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

from . import recur as recur_mod
from . import report, store, sync
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
        entries = entries[-args.last + 1 :]  # skip the header row
    for e in entries:
        print(f"{e.day.isoformat()}  {e.category:<16}{e.amount:>12.2f}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    entries = store.load(args.ledger)
    month_entries = report.entries_in_month(entries, args.year, args.month)
    print(report.format_report(args.year, args.month, report.totals_by_category(month_entries)))
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    ok = sync.push(args.ledger)
    print("synced" if ok else "sync failed")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# recur sub-commands
# ---------------------------------------------------------------------------

def cmd_recur_add(args: argparse.Namespace) -> int:
    """Validate inputs, persist a new recurring rule, report result."""
    errors = recur_mod.validate_recur_add(
        args.category,
        args.amount,
        args.day_of_month,
    )
    if errors:
        for msg in errors:
            print(f"error: {msg}", file=sys.stderr)
        return 2

    ledger = store.load_ledger(args.ledger)
    ledger = recur_mod.add_rule(ledger, args.category, args.amount, args.day_of_month)
    store.save_ledger(args.ledger, ledger)
    print(
        f"recurring rule added: {args.category} {args.amount}"
        f" on day {args.day_of_month} of each month"
    )
    return 0


def cmd_recur_apply(args: argparse.Namespace) -> int:
    """Apply all recurring rules for the given year/month."""
    ledger = store.load_ledger(args.ledger)

    try:
        updated, count = recur_mod.apply_rules(ledger, args.year, args.month)
    except ValueError as exc:
        # REQ-06: calendar validation failed — report offending rules to stderr.
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if count == 0:
        print(f"no recurring entries to apply for {args.year}-{args.month:02d}")
        return 0

    store.save_ledger(args.ledger, updated)
    print(f"applied {count} recurring entr{'y' if count == 1 else 'ies'}"
          f" for {args.year}-{args.month:02d}")
    return 0


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

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

    s = sub.add_parser("sync", help="push the ledger to LedgerCloud")
    s.set_defaults(func=cmd_sync)

    # recur — nested sub-parser
    recur_p = sub.add_parser("recur", help="manage recurring entries")
    recur_sub = recur_p.add_subparsers(dest="recur_command", required=True)

    ra = recur_sub.add_parser("add", help="add a recurring entry rule")
    ra.add_argument("--category", required=True)
    ra.add_argument("--amount", required=True)
    ra.add_argument("--day-of-month", dest="day_of_month", type=int, required=True)
    ra.set_defaults(func=cmd_recur_add)

    rap = recur_sub.add_parser("apply", help="apply recurring rules for a month")
    rap.add_argument("--year", type=int, required=True)
    rap.add_argument("--month", type=int, required=True)
    rap.set_defaults(func=cmd_recur_apply)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
