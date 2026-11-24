"""Helpers shared by every lab check. Nothing here calls the Anthropic API."""

from __future__ import annotations

import ast
import csv
import json
import os
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import yaml

HIDDEN_TESTS = Path(__file__).parent / "hidden_tests"


@dataclass
class Result:
    ok: bool
    message: str
    soft: bool = False  # soft results are reminders and never fail a lab


@dataclass
class Lab:
    id: str
    title: str
    func: Callable[[Ctx], None]


@dataclass
class Ctx:
    root: Path
    lab_id: str = "<lab>"
    results: list[Result] = field(default_factory=list)

    # -- recording -------------------------------------------------------
    def check(self, ok: bool, message: str, hint: str = "") -> bool:
        self.results.append(Result(bool(ok), message if ok or not hint else f"{message}\n      ↳ {hint}"))
        return bool(ok)

    def remind(self, ok: bool, message: str) -> None:
        self.results.append(Result(bool(ok), message, soft=True))

    # -- files -----------------------------------------------------------
    def path(self, rel: str) -> Path:
        return self.root / rel

    def exists(self, rel: str, hint: str = "") -> bool:
        return self.check(self.path(rel).exists(), f"{rel} exists", hint or f"create {rel}")

    def read(self, rel: str) -> str:
        try:
            return self.path(rel).read_text(encoding="utf-8")
        except OSError:
            return ""

    def frontmatter(self, rel: str) -> dict:
        return parse_frontmatter(self.read(rel))

    def json(self, rel: str) -> dict | list | None:
        try:
            return json.loads(self.read(rel))
        except ValueError:
            return None

    def settings(self) -> dict:
        """Project settings merged the way Claude Code merges them (local wins, lists concat)."""
        merged: dict = {}
        for rel in (".claude/settings.json", ".claude/settings.local.json"):
            data = self.json(rel)
            if isinstance(data, dict):
                merged = deep_merge(merged, data)
        return merged

    def headings_present(self, rel: str, headings: list[str]) -> bool:
        text = self.read(rel).lower()
        missing = [h for h in headings if not re.search(rf"^#+\s*{re.escape(h.lower())}", text, re.M)]
        return self.check(
            not missing,
            f"{rel} has sections: {', '.join(headings)}",
            f"missing headings: {', '.join(missing)}" if missing else "",
        )

    # -- running things --------------------------------------------------
    def run(self, *cmd: str, timeout: int = 180, env: dict | None = None) -> subprocess.CompletedProcess:
        full_env = {**os.environ, **(env or {})}
        return subprocess.run(
            cmd, cwd=self.root, capture_output=True, text=True, timeout=timeout, env=full_env
        )

    def pytest_env(self) -> dict:
        src = str(self.root / "practice-app" / "src")
        return {"PYTHONPATH": src + os.pathsep + str(HIDDEN_TESTS)}

    def hidden_tests(self, name: str, issue: str) -> bool:
        proc = self.run(
            sys.executable, "-m", "pytest", str(HIDDEN_TESTS / name),
            "-c", str(HIDDEN_TESTS / "pytest.ini"), "--rootdir", str(HIDDEN_TESTS),
            env=self.pytest_env(),
        )
        summary = pytest_summary(proc)
        return self.check(
            proc.returncode == 0,
            f"{issue} acceptance tests pass ({summary})",
            f"see the failures:  uv run labcheck {self.lab_id} -v" if proc.returncode else "",
        ) or self._verbose(proc)

    def own_tests_pass(self) -> bool:
        proc = self.run(sys.executable, "-m", "pytest", "practice-app/tests",
                        "-p", "no:cacheprovider", env=self.pytest_env())
        return self.check(
            proc.returncode == 0,
            f"your practice-app test suite passes ({pytest_summary(proc)})",
            "run:  uv run pytest",
        ) or self._verbose(proc)

    def count_tests(self, rel: str) -> int:
        try:
            tree = ast.parse(self.read(rel))
        except SyntaxError:
            return 0
        return sum(
            1 for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef) and n.name.startswith("test_")
        )

    def git(self, *args: str) -> str:
        try:
            return self.run("git", *args, timeout=30).stdout
        except (OSError, subprocess.TimeoutExpired):
            return ""

    def cost_logged(self, lab_id: str) -> None:
        logged = any(row.get("lab") == lab_id for row in read_cost_log(self.root))
        self.remind(logged, f"cost logged for {lab_id}  (uv run labcheck log {lab_id} <usd> \"note\")")

    verbose = False

    def _verbose(self, proc: subprocess.CompletedProcess) -> bool:
        if self.verbose:
            print(proc.stdout[-4000:], proc.stderr[-2000:], sep="\n")
        return False


# --------------------------------------------------------------------- utils


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def deep_merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for key, value in b.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        elif isinstance(value, list) and isinstance(out.get(key), list):
            out[key] = out[key] + value
        else:
            out[key] = value
    return out


def pytest_summary(proc: subprocess.CompletedProcess) -> str:
    for line in reversed((proc.stdout + "\n" + proc.stderr).splitlines()):
        if re.search(r"\d+ (passed|failed|error)|no tests ran", line):
            return line.strip(" =")
    return last_line(proc.stderr) or last_line(proc.stdout)


def last_line(text: str) -> str:
    lines = [ln.strip() for ln in (text or "").strip().splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def read_cost_log(root: Path) -> list[dict]:
    try:
        with open(root / "notes" / "cost-log.csv", newline="") as f:
            return list(csv.DictReader(f))
    except OSError:
        return []


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return [str(v) for v in value]
