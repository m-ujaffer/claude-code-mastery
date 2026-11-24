"""labcheck: verify your lab work without spending any API budget.

    uv run labcheck list                 show every lab
    uv run labcheck w1d3                 check one lab (add -v for test output)
    uv run labcheck week 2               check a whole week
    uv run labcheck log w1d3 0.42 "note" record what a lab cost you
    uv run labcheck budget               month-to-date spend vs the course plan
    uv run labcheck doctor               check your Codespace setup
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from labcheck.checks import LABS
from labcheck.core import Ctx, read_cost_log

GREEN, RED, YELLOW, DIM, BOLD, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[1m", "\033[0m"

WEEK_CAPS = {"w1": 3.0, "w2": 4.0, "w3": 5.0, "w4": 6.0, "w5": 7.0, "w6": 6.0}
MONTHLY_BUDGET = float(os.environ.get("COURSE_MONTHLY_BUDGET", "30"))


def find_root() -> Path:
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        if (p / "practice-app").is_dir() and (p / "labcheck").is_dir():
            return p
    return here


def run_lab(lab_id: str, root: Path, verbose: bool = False) -> bool:
    lab = LABS[lab_id]
    ctx = Ctx(root, lab_id)
    ctx.verbose = verbose
    print(f"\n{BOLD}{lab_id} · {lab.title}{RESET}")
    try:
        lab.func(ctx)
    except Exception as exc:  # a broken check should never crash the learner
        ctx.check(False, f"check crashed: {exc!r}")
    passed = True
    for r in ctx.results:
        if r.soft:
            icon = f"{GREEN}✔{RESET}" if r.ok else f"{YELLOW}…{RESET}"
        else:
            icon = f"{GREEN}✔{RESET}" if r.ok else f"{RED}✘{RESET}"
            passed &= r.ok
        print(f"  {icon} {r.message}")
    verdict = f"{GREEN}PASS{RESET}" if passed else f"{RED}NOT YET{RESET}"
    print(f"  → {verdict}")
    return passed


def cmd_log(args, root: Path) -> int:
    if args.lab not in LABS:
        print(f"Unknown lab '{args.lab}'. Try: labcheck list")
        return 1
    path = root / "notes" / "cost-log.csv"
    path.parent.mkdir(exist_ok=True)
    new = not path.exists()
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["lab", "date", "cost_usd", "note"])
        w.writerow([args.lab, dt.date.today().isoformat(), f"{args.cost:.2f}", args.note])
    print(f"Logged ${args.cost:.2f} for {args.lab}.")
    return cmd_budget(args, root)


def cmd_budget(args, root: Path) -> int:
    rows = read_cost_log(root)
    by_week: dict[str, float] = {}
    for r in rows:
        try:
            by_week[r["lab"][:2]] = by_week.get(r["lab"][:2], 0.0) + float(r["cost_usd"])
        except (KeyError, ValueError):
            continue
    print(f"\n{BOLD}Your cost log vs the course plan{RESET}")
    for week, cap in WEEK_CAPS.items():
        spent = by_week.get(week, 0.0)
        colour = GREEN if spent <= cap else RED
        bar = "█" * min(20, int(20 * spent / cap)) if cap else ""
        print(f"  Week {week[1]}  {colour}${spent:5.2f}{RESET} / ${cap:.0f}  {DIM}{bar}{RESET}")

    month = dt.date.today().strftime("%Y-%m")
    ledger_path = root / "notes" / ".cost-ledger.json"
    try:
        sessions = json.loads(ledger_path.read_text()).get(month, {})
        mtd = sum(e["banked"] + e["last"] for e in sessions.values())
        print(f"\n  Status-line estimate for {month}: ${mtd:.2f} of ${MONTHLY_BUDGET:.0f} "
              f"({len(sessions)} interactive sessions)")
    except (OSError, ValueError):
        print(f"\n  {DIM}No status-line ledger yet: it fills in as you use Claude Code.{RESET}")
    print(f"  {DIM}Estimates only. Headless and CI runs are not tracked here; the Anthropic Console is the source of truth.{RESET}")
    return 0


def cmd_doctor(args, root: Path) -> int:
    print(f"\n{BOLD}Environment check{RESET}")
    ok = True

    def line(good: bool, msg: str, fix: str = "") -> None:
        nonlocal ok
        ok &= good
        icon = f"{GREEN}✔{RESET}" if good else f"{RED}✘{RESET}"
        print(f"  {icon} {msg}" + (f"\n      ↳ {fix}" if fix and not good else ""))

    line(sys.version_info >= (3, 12), f"Python {sys.version.split()[0]}")
    line(shutil.which("uv") is not None, "uv is installed", "pipx install uv")
    claude = shutil.which("claude")
    version = ""
    if claude:
        try:
            version = subprocess.run([claude, "--version"], capture_output=True, text=True,
                                     timeout=20).stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    line(bool(claude), f"Claude Code CLI {version}".strip(), "see setup/troubleshooting.md#claude-not-found")
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    line(key.startswith("sk-ant-"),
         f"ANTHROPIC_API_KEY set ({key[:10]}…{key[-4:]})" if key else "ANTHROPIC_API_KEY set",
         "add the Codespaces secret, then rebuild: setup/SETUP-codespaces.md#step-2")
    line(shutil.which("gh") is not None, "GitHub CLI (gh) installed")
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                          cwd=root, capture_output=True, text=True)
    line(proc.returncode == 0, "TaskForge tests pass", "uv run pytest")
    line((root / "notes" / "cost-log.csv").exists(), "notes/cost-log.csv exists",
         "bash .devcontainer/post-create.sh")
    print(f"\n  {'Ready to go!' if ok else 'Fix the items above, then run: uv run labcheck doctor'}")
    return 0 if ok else 1


def cmd_lint_labs(args, root: Path) -> int:
    """Instructor tool: every lab file follows the template."""
    required = ["## 🎯 Goal", "## 💰 Budget", "## ✅ Checkpoint", "## 🚀 Stretch", "## 💼 Commercial application",
                "## 🤔 Reflect"]
    bad = 0
    for f in sorted(root.glob("[1-6]_*/[0-9]_lab*.md")):
        text = f.read_text()
        missing = [h for h in required if h not in text]
        if "## 📤 Push your progress" not in text or "git push" not in text:
            missing.append("## 📤 Push your progress (with git push)")
        lab_ids = re.findall(r"labcheck (w\dd\d+)", text)
        unknown = [i for i in lab_ids if i not in LABS]
        if missing or unknown:
            bad += 1
            print(f"✘ {f.relative_to(root)} missing={missing} unknown_labs={unknown}")
    print("lab files OK" if not bad else f"{bad} lab file(s) need fixing")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = find_root()
    if "--root" in argv:
        i = argv.index("--root")
        root = Path(argv[i + 1]).resolve()
        del argv[i:i + 2]
    verbose = "-v" in argv
    argv = [a for a in argv if a != "-v"]

    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(__doc__)
        return 0
    cmd = argv[0]

    if cmd == "list":
        for lab_id, lab in LABS.items():
            print(f"  {lab_id:6} {lab.title}")
        return 0
    if cmd in LABS:
        return 0 if run_lab(cmd, root, verbose) else 1
    if cmd == "week" and len(argv) > 1:
        ids = [i for i in LABS if i.startswith(f"w{argv[1]}d")]
        results = [run_lab(i, root, verbose) for i in ids]
        return 0 if all(results) else 1
    if cmd == "--all":
        results = {i: run_lab(i, root, verbose) for i in LABS}
        failed = [i for i, ok in results.items() if not ok]
        print(f"\n{len(results) - len(failed)}/{len(results)} labs pass" + (f"; failing: {failed}" if failed else ""))
        return 0 if not failed else 1

    parser = argparse.ArgumentParser(prog="labcheck")
    sub = parser.add_subparsers(dest="cmd")
    p_log = sub.add_parser("log")
    p_log.add_argument("lab")
    p_log.add_argument("cost", type=float)
    p_log.add_argument("note", nargs="?", default="")
    sub.add_parser("budget")
    sub.add_parser("doctor")
    sub.add_parser("lint-labs")
    args = parser.parse_args(argv)
    handlers = {"log": cmd_log, "budget": cmd_budget, "doctor": cmd_doctor, "lint-labs": cmd_lint_labs}
    if args.cmd not in handlers:
        parser.print_help()
        return 1
    return handlers[args.cmd](args, root)


if __name__ == "__main__":
    sys.exit(main())
