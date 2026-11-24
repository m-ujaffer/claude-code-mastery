# LEGACY CODE - written in a hurry for the 2019 board meeting and never cleaned up.
# It works, people depend on its exact output, and nobody wants to touch it.
# (Week 5 / Day 25 and the capstone ask you to refactor it safely.)

import datetime
from taskforge import clock


def build_report(conn, project_id, fmt="text"):
    p = conn.execute("select * from projects where id = ?", (project_id,)).fetchone()
    rows = conn.execute("select id, title, status, priority, due_date from tasks where project_id = ? order by id", (project_id,)).fetchall()
    t = clock.today()
    out = ""
    if fmt == "text":
        out = out + "PROJECT REPORT: " + p["name"] + "\n"
        out = out + "=" * (16 + len(p["name"])) + "\n"
        n = 0; d = 0; ip = 0; od = 0; hi = 0
        for r in rows:
            n = n + 1
            if r["status"] == "done":
                d = d + 1
            else:
                if r["status"] == "in_progress":
                    ip = ip + 1
                if r["due_date"] != None:
                    if datetime.date.fromisoformat(r["due_date"]) < t:
                        od = od + 1
            if r["priority"] == "high":
                if r["status"] != "done":
                    hi = hi + 1
        out = out + "Total tasks: " + str(n) + "\n"
        out = out + "Done: " + str(d) + "\n"
        out = out + "In progress: " + str(ip) + "\n"
        out = out + "Overdue: " + str(od) + "\n"
        out = out + "Open high priority: " + str(hi) + "\n"
        if n > 0:
            out = out + "Completion: " + str(round(d * 100.0 / n)) + "%\n"
        else:
            out = out + "Completion: n/a\n"
        out = out + "\n"
        for r in rows:
            flag = ""
            if r["status"] != "done" and r["due_date"] != None and datetime.date.fromisoformat(r["due_date"]) < t:
                flag = " (OVERDUE)"
            if r["status"] == "done":
                out = out + "[x] " + r["title"] + flag + "\n"
            elif r["status"] == "in_progress":
                out = out + "[~] " + r["title"] + flag + "\n"
            else:
                out = out + "[ ] " + r["title"] + flag + "\n"
    elif fmt == "md":
        out = out + "# Project report: " + p["name"] + "\n\n"
        n = 0; d = 0; ip = 0; od = 0; hi = 0
        for r in rows:
            n = n + 1
            if r["status"] == "done":
                d = d + 1
            else:
                if r["status"] == "in_progress":
                    ip = ip + 1
                if r["due_date"] != None:
                    if datetime.date.fromisoformat(r["due_date"]) < t:
                        od = od + 1
            if r["priority"] == "high" and r["status"] != "done":
                hi = hi + 1
        out = out + "| Metric | Value |\n|---|---|\n"
        out = out + "| Total tasks | " + str(n) + " |\n"
        out = out + "| Done | " + str(d) + " |\n"
        out = out + "| In progress | " + str(ip) + " |\n"
        out = out + "| Overdue | " + str(od) + " |\n"
        out = out + "| Open high priority | " + str(hi) + " |\n"
        if n > 0:
            out = out + "| Completion | " + str(round(d * 100.0 / n)) + "% |\n"
        else:
            out = out + "| Completion | n/a |\n"
        out = out + "\n## Tasks\n\n"
        for r in rows:
            box = "[ ]"
            if r["status"] == "done":
                box = "[x]"
            line = "- " + box + " " + r["title"]
            if r["priority"] == "high":
                line = line + " **(high)**"
            if r["status"] != "done" and r["due_date"] != None:
                if datetime.date.fromisoformat(r["due_date"]) < t:
                    line = line + " _overdue since " + r["due_date"] + "_"
            out = out + line + "\n"
    elif fmt == "html":
        out = out + "<h1>Project report: " + p["name"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</h1>\n"
        n = 0; d = 0; ip = 0; od = 0; hi = 0
        for r in rows:
            n += 1
            if r["status"] == "done":
                d += 1
            elif r["status"] == "in_progress":
                ip += 1
            if r["status"] != "done" and r["due_date"] != None and datetime.date.fromisoformat(r["due_date"]) < t:
                od += 1
            if r["priority"] == "high" and r["status"] != "done":
                hi += 1
        out = out + "<ul>\n"
        out = out + "<li>Total tasks: " + str(n) + "</li>\n"
        out = out + "<li>Done: " + str(d) + "</li>\n"
        out = out + "<li>In progress: " + str(ip) + "</li>\n"
        out = out + "<li>Overdue: " + str(od) + "</li>\n"
        out = out + "<li>Open high priority: " + str(hi) + "</li>\n"
        if n > 0:
            out = out + "<li>Completion: " + str(round(d * 100.0 / n)) + "%</li>\n"
        else:
            out = out + "<li>Completion: n/a</li>\n"
        out = out + "</ul>\n<table>\n<tr><th>Task</th><th>Status</th><th>Priority</th><th>Due</th></tr>\n"
        for r in rows:
            cls = ""
            if r["status"] != "done" and r["due_date"] != None and datetime.date.fromisoformat(r["due_date"]) < t:
                cls = ' class="overdue"'
            due = r["due_date"] if r["due_date"] != None else "-"
            out = out + "<tr" + cls + "><td>" + r["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</td><td>" + r["status"] + "</td><td>" + r["priority"] + "</td><td>" + due + "</td></tr>\n"
        out = out + "</table>\n"
    return out
