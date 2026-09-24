from ledgerlite import store
from ledgerlite.cli import main
from ledgerlite.models import RecurringRule


def test_add_then_list(tmp_path, capsys):
    ledger = tmp_path / "l.json"
    args = ["--ledger", str(ledger), "add", "--day", "2026-04-02"]
    args += ["--category", "food", "--amount", "99.90"]
    assert main(args) == 0
    assert main(["--ledger", str(ledger), "list"]) == 0
    out = capsys.readouterr().out
    assert "2026-04-02" in out and "food" in out and "99.90" in out


def test_list_last_n(tmp_path, capsys):
    ledger = tmp_path / "l.json"
    for d in ("2026-04-01", "2026-04-02", "2026-04-03"):
        main(["--ledger", str(ledger), "add", "--day", d, "--category", "c", "--amount", "1"])
    capsys.readouterr()
    main(["--ledger", str(ledger), "list", "--last", "2"])
    lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
    assert lines and lines[0].startswith("2026-04-0")


def test_report_command(tmp_path, capsys):
    ledger = tmp_path / "l.json"
    main([
        "--ledger", str(ledger), "add", "--day", "2026-04-02", "--category", "f", "--amount", "1"
    ])
    capsys.readouterr()
    assert main(["--ledger", str(ledger), "report", "--year", "2026", "--month", "4"]) == 0
    assert "TOTAL" in capsys.readouterr().out


def test_add_negative_amount(tmp_path, capsys):
    ledger = tmp_path / "l.json"
    code = main(["--ledger", str(ledger), "add", "--category", "food", "--amount", "-5.00"])
    assert code == 2
    assert "amount must be positive" in capsys.readouterr().err


def test_add_zero_amount(tmp_path, capsys):
    ledger = tmp_path / "l.json"
    code = main(["--ledger", str(ledger), "add", "--category", "food", "--amount", "0"])
    assert code == 2
    assert "amount must be positive" in capsys.readouterr().err


def test_add_empty_category(tmp_path, capsys):
    ledger = tmp_path / "l.json"
    code = main(["--ledger", str(ledger), "add", "--category", "   ", "--amount", "10.00"])
    assert code == 2
    assert "category is required" in capsys.readouterr().err


def test_add_valid(tmp_path, capsys):
    ledger = tmp_path / "l.json"
    code = main(["--ledger", str(ledger), "add", "--day", "2026-09-21",
                 "--category", "transport", "--amount", "25.00"])
    assert code == 0
    assert "transport" in capsys.readouterr().out


# ===========================================================================
# Task 3 — recur add and recur apply CLI integration tests
# ===========================================================================


def test_recur_add_valid(tmp_path, capsys):
    """recur add with valid inputs exits 0, prints confirmation, persists the rule."""
    ledger = tmp_path / "l.json"
    code = main([
        "--ledger", str(ledger),
        "recur", "add",
        "--category", "rent",
        "--amount", "15000",
        "--day-of-month", "1",
    ])
    assert code == 0
    out = capsys.readouterr().out
    assert "rent" in out

    # Rule must be persisted to disk.
    data = store.load_ledger(ledger)
    assert len(data.recurring_rules) == 1
    rule = RecurringRule.from_dict(data.recurring_rules[0])
    assert rule.category == "rent"
    from decimal import Decimal
    assert rule.amount == Decimal("15000")
    assert rule.day_of_month == 1


def test_recur_add_empty_category(tmp_path, capsys):
    """recur add with blank category exits 2, prints error, writes no rule."""
    ledger = tmp_path / "l.json"
    code = main([
        "--ledger", str(ledger),
        "recur", "add",
        "--category", "   ",
        "--amount", "5000",
        "--day-of-month", "1",
    ])
    assert code == 2
    assert "category" in capsys.readouterr().err.lower()

    # No rule must have been written.
    data = store.load_ledger(ledger)
    assert data.recurring_rules == []


def test_recur_add_zero_amount(tmp_path, capsys):
    """recur add with zero amount exits 2, prints error, writes no rule."""
    ledger = tmp_path / "l.json"
    code = main([
        "--ledger", str(ledger),
        "recur", "add",
        "--category", "food",
        "--amount", "0",
        "--day-of-month", "5",
    ])
    assert code == 2
    assert "amount" in capsys.readouterr().err.lower()

    data = store.load_ledger(ledger)
    assert data.recurring_rules == []


def test_recur_add_bad_day_of_month(tmp_path, capsys):
    """recur add with day-of-month outside 1–31 exits 2, prints error, writes no rule."""
    ledger = tmp_path / "l.json"
    code = main([
        "--ledger", str(ledger),
        "recur", "add",
        "--category", "food",
        "--amount", "100",
        "--day-of-month", "32",
    ])
    assert code == 2
    assert "day" in capsys.readouterr().err.lower()

    data = store.load_ledger(ledger)
    assert data.recurring_rules == []


def test_recur_apply_creates_entry(tmp_path, capsys):
    """recur apply creates the expected entry and exits 0."""
    ledger = tmp_path / "l.json"

    # Add a rule first.
    main([
        "--ledger", str(ledger),
        "recur", "add",
        "--category", "rent",
        "--amount", "15000",
        "--day-of-month", "1",
    ])
    capsys.readouterr()

    code = main([
        "--ledger", str(ledger),
        "recur", "apply",
        "--year", "2026",
        "--month", "3",
    ])
    assert code == 0

    data = store.load_ledger(ledger)
    assert len(data.entries) == 1
    entry = data.entries[0]
    from datetime import date
    from decimal import Decimal
    assert entry.day == date(2026, 3, 1)
    assert entry.category == "rent"
    assert entry.amount == Decimal("15000")
    assert entry.currency == "INR"


def test_recur_apply_no_rules(tmp_path, capsys):
    """recur apply with no rules exits 0, prints a 'nothing to apply' message,
    and leaves the ledger unchanged."""
    ledger = tmp_path / "l.json"

    # Seed an existing regular entry so we can confirm it is untouched.
    main([
        "--ledger", str(ledger),
        "add", "--day", "2026-03-01", "--category", "food", "--amount", "200",
    ])
    capsys.readouterr()

    code = main([
        "--ledger", str(ledger),
        "recur", "apply",
        "--year", "2026",
        "--month", "3",
    ])
    assert code == 0
    out = capsys.readouterr().out.lower()
    # Must say something about there being nothing to apply.
    assert "no recurring" in out or "nothing" in out or "0" in out

    # The pre-existing entry must still be there and nothing else added.
    data = store.load_ledger(ledger)
    assert len(data.entries) == 1
    assert data.entries[0].category == "food"


def test_recur_apply_idempotent(tmp_path, capsys):
    """Running recur apply twice for the same month creates only one entry."""
    ledger = tmp_path / "l.json"

    main([
        "--ledger", str(ledger),
        "recur", "add",
        "--category", "rent",
        "--amount", "5000",
        "--day-of-month", "1",
    ])
    capsys.readouterr()

    main(["--ledger", str(ledger), "recur", "apply", "--year", "2026", "--month", "3"])
    main(["--ledger", str(ledger), "recur", "apply", "--year", "2026", "--month", "3"])
    capsys.readouterr()

    data = store.load_ledger(ledger)
    assert len(data.entries) == 1  # second apply was a no-op


def test_recur_apply_invalid_date(tmp_path, capsys):
    """recur apply with a rule whose day does not exist in the month exits non-zero
    and prints the category and day to stderr."""
    ledger = tmp_path / "l.json"

    # day 31 does not exist in April.
    main([
        "--ledger", str(ledger),
        "recur", "add",
        "--category", "gym",
        "--amount", "800",
        "--day-of-month", "31",
    ])
    capsys.readouterr()

    code = main([
        "--ledger", str(ledger),
        "recur", "apply",
        "--year", "2026",
        "--month", "4",
    ])
    assert code != 0
    err = capsys.readouterr().err
    assert "gym" in err
    assert "31" in err

    # No entries must have been created.
    data = store.load_ledger(ledger)
    assert data.entries == []


def test_recur_apply_one_invalid_blocks_all(tmp_path, capsys):
    """REQ-06: one rule with an invalid date blocks ALL entries for the invocation.

    A valid rule (rent, day 1) and an invalid rule (gym, day 31) are both present.
    Applying for April must create zero entries — not just skip the bad rule.
    """
    ledger = tmp_path / "l.json"

    main([
        "--ledger", str(ledger),
        "recur", "add",
        "--category", "rent",
        "--amount", "15000",
        "--day-of-month", "1",
    ])
    main([
        "--ledger", str(ledger),
        "recur", "add",
        "--category", "gym",
        "--amount", "800",
        "--day-of-month", "31",   # invalid for April
    ])
    capsys.readouterr()

    code = main([
        "--ledger", str(ledger),
        "recur", "apply",
        "--year", "2026",
        "--month", "4",
    ])
    assert code != 0
    err = capsys.readouterr().err
    # Error output must identify the offending rule.
    assert "gym" in err
    assert "31" in err

    # No entries at all — the valid rent rule must also have been blocked.
    data = store.load_ledger(ledger)
    assert data.entries == []
