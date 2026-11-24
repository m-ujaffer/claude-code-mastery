"""Project report in text, Markdown or HTML (refactored in TF-109).

The output is pinned byte-for-byte by tests/test_report_builder.py. Quirks
such as Markdown showing in-progress tasks as "[ ]" are deliberate: they are
the existing behaviour that downstream consumers depend on.
"""

import sqlite3
from dataclasses import dataclass
from datetime import date
from html import escape

from taskforge import clock


@dataclass(frozen=True)
class Summary:
    total: int
    done: int
    in_progress: int
    overdue: int
    open_high: int

    @property
    def completion(self) -> str:
        return f"{round(self.done * 100.0 / self.total)}%" if self.total else "n/a"

    def metrics(self) -> list[tuple[str, str]]:
        return [
            ("Total tasks", str(self.total)),
            ("Done", str(self.done)),
            ("In progress", str(self.in_progress)),
            ("Overdue", str(self.overdue)),
            ("Open high priority", str(self.open_high)),
            ("Completion", self.completion),
        ]


def _is_overdue(row: sqlite3.Row, today: date) -> bool:
    return (
        row["status"] != "done"
        and row["due_date"] is not None
        and date.fromisoformat(row["due_date"]) < today
    )


def _summarise(rows: list[sqlite3.Row], today: date) -> Summary:
    return Summary(
        total=len(rows),
        done=sum(r["status"] == "done" for r in rows),
        in_progress=sum(r["status"] == "in_progress" for r in rows),
        overdue=sum(_is_overdue(r, today) for r in rows),
        open_high=sum(r["priority"] == "high" and r["status"] != "done" for r in rows),
    )


def _text(name: str, rows: list[sqlite3.Row], summary: Summary, today: date) -> str:
    title = f"PROJECT REPORT: {name}"
    lines = [title, "=" * len(title)]
    lines += [f"{label}: {value}" for label, value in summary.metrics()]
    lines.append("")
    boxes = {"done": "[x]", "in_progress": "[~]"}
    for r in rows:
        flag = " (OVERDUE)" if _is_overdue(r, today) else ""
        lines.append(f"{boxes.get(r['status'], '[ ]')} {r['title']}{flag}")
    return "\n".join(lines) + "\n"


def _markdown(name: str, rows: list[sqlite3.Row], summary: Summary, today: date) -> str:
    lines = [f"# Project report: {name}", "", "| Metric | Value |", "|---|---|"]
    lines += [f"| {label} | {value} |" for label, value in summary.metrics()]
    lines += ["", "## Tasks", ""]
    for r in rows:
        line = f"- {'[x]' if r['status'] == 'done' else '[ ]'} {r['title']}"
        if r["priority"] == "high":
            line += " **(high)**"
        if _is_overdue(r, today):
            line += f" _overdue since {r['due_date']}_"
        lines.append(line)
    return "\n".join(lines) + "\n"


def _html(name: str, rows: list[sqlite3.Row], summary: Summary, today: date) -> str:
    lines = [f"<h1>Project report: {escape(name, quote=False)}</h1>", "<ul>"]
    lines += [f"<li>{label}: {value}</li>" for label, value in summary.metrics()]
    lines += ["</ul>", "<table>", "<tr><th>Task</th><th>Status</th><th>Priority</th><th>Due</th></tr>"]
    for r in rows:
        cls = ' class="overdue"' if _is_overdue(r, today) else ""
        cells = [escape(r["title"], quote=False), r["status"], r["priority"], r["due_date"] or "-"]
        lines.append(f"<tr{cls}>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    lines.append("</table>")
    return "\n".join(lines) + "\n"


_RENDERERS = {"text": _text, "md": _markdown, "html": _html}


def build_report(conn: sqlite3.Connection, project_id: int, fmt: str = "text") -> str:
    renderer = _RENDERERS.get(fmt)
    if renderer is None:
        return ""
    project = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    rows = conn.execute(
        "SELECT id, title, status, priority, due_date FROM tasks WHERE project_id = ? ORDER BY id",
        (project_id,),
    ).fetchall()
    today = clock.today()
    return renderer(project["name"], rows, _summarise(rows, today), today)
