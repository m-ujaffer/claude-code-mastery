# Week 4 · Day 19: Structured output from headless Claude

| | |
|---|---|
| **Level** | Advanced |
| **CCA-F domain** | 3 · Prompt engineering & structured output |
| **Time** | 10 min read · 35 min hands-on · 10 min verify & reflect · 5 min log |
| **Budget cap** | $1.00 |
| **Check** | `uv run labcheck w4d19` |

## 🎯 Goal

Get **machine-readable, schema-validated** JSON from Claude Code in a script, and write prompts for
programs rather than people.

## 📖 Primer

```bash
claude -p "<prompt>" \
  --output-format json \
  --json-schema "$(cat schemas/triage.schema.json)" \
  --max-turns 3 --max-budget-usd 0.20
```

- `-p` runs headless: one task, then exit.
- `--output-format json` returns a JSON envelope with `result`, `session_id`, `total_cost_usd` and more.
- `--json-schema` makes Claude return output that **validates** against your schema, in the envelope's
  **`structured_output`** field. If the run ends without valid output (for example a refusal), that field is
  **missing**, so your script must check for it.
- `--max-turns` / `--max-budget-usd` stop runaway scripts. Use them **every time**.
- For scripts, consider `--bare`. It skips your hooks, skills, plugins and CLAUDE.md for a faster, more
  reproducible run (but then you must pass in what you need).

**Prompting for machines:** define every field's meaning in the schema `description`s, use `enum`s for
categories, give one **example** in the prompt (few-shot), and say what to do when unsure (for example `"severity": "unknown"`).

## 🛠️ Steps

**1. Write the schema.** Create `schemas/triage.schema.json` (Draft 2020-12) for triaging a backlog issue:

- `issue_id` (string, pattern `^TF-\d{3}$`)
- `type` (enum: `bug`, `feature`, `tech-debt`, `validation`)
- `severity` (enum: `low`, `medium`, `high`, `unknown`)
- `summary` (string, max 120 characters)
- `affected_files` (array of strings)
- `estimated_effort` (enum: `S`, `M`, `L`)

Mark `issue_id`, `type`, `severity` and `summary` as required. Add a `description` to every property,
and set `additionalProperties: false`.

**2. Write the script** `scripts/triage.sh`. Ask Claude to help, with these requirements:

- takes an issue id argument, for example `TF-107`
- runs `claude -p` with `--output-format json`, `--json-schema "$(cat schemas/triage.schema.json)"`,
  `--max-turns 4`, `--max-budget-usd 0.25`, and `--allowedTools "Read,Grep,Glob"` (read-only)
- the prompt tells Claude to read the issue in `practice-app/ISSUES.md`, inspect the code, and includes **one
  example** of a filled-in triage object
- saves the raw envelope to `out/triage-<id>.json`
- uses `python3` to check that `structured_output` exists, prints it, and prints `total_cost_usd` to stderr
- exits non-zero if `structured_output` is missing

**3. Run it** on two issues and look at the output:

```bash
chmod +x scripts/triage.sh
./scripts/triage.sh TF-107
./scripts/triage.sh TF-109
```

**4. Save a sample.** Put the two `structured_output` objects as a JSON **array** in `notes/triage-output.json`.

**5. Validate independently** (never trust, verify):

```bash
uv run python -c "
import json, jsonschema
schema = json.load(open('schemas/triage.schema.json'))
for item in json.load(open('notes/triage-output.json')): jsonschema.validate(item, schema)
print('valid')"
```

**6. Commit** the schema, the script and the sample.

## ✅ Checkpoint

```bash
uv run labcheck w4d19
```

## 💰 Budget & cost log

Cap: **$1.00**. Headless runs **don't** appear in your status-line ledger, so add the `total_cost_usd`
values your script printed:

```bash
uv run labcheck log w4d19 0.60 "triage script (2 runs + authoring)"
```

## 🚀 Stretch

- Run your script with `--bare`. What changed in cost and behaviour?
- Make the script triage **every** open issue and produce a sorted table. Cap the **total** spend.

## 💼 Commercial application

Structured output turns Claude from a chat partner into a **component**: triage bots, release-note
generators, migration planners and code-review gates all depend on reliably parseable output. The schema
is the contract between the model and the rest of your system.

## 🤔 Reflect

1. Why validate the output yourself when the CLI already enforced the schema?
2. How did the one-shot example change the quality of `summary`?
3. What should a CI job do when `structured_output` is missing?

## ➡️ Next

[Day 20: Mini-project: MCP-powered standup](5_lab5_mcp_standup_project.md)
