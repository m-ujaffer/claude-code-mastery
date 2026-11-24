# Handoff: TF-109 refactor of legacy/report_builder.py

## Goal
Split `build_report` into small functions (none over 40 lines) with shared counting logic,
keeping text/md/html output byte-for-byte identical (including the md "[ ]" for in-progress quirk).

## Done
- Characterisation tests pin the exact output (practice-app/tests/test_report_builder.py), committed.
- Step 1: extracted `_is_overdue` and a `Summary` dataclass with `_summarise()`. Tests green, committed.
- Step 2: one renderer per format (`_text`, `_markdown`, `_html`) using `Summary.metrics()`. Tests green, committed.
- Step 3: `build_report` dispatches through `_RENDERERS`; unknown formats still return "". Tests green, committed.

## Next
- Nothing required. Optional: share one overdue rule with services.is_overdue (verify with the golden tests first).

## Risks
- `html.escape(quote=False)` must match the legacy & → < → > order exactly (it does; tests cover it).
- Python's `round()` uses banker's rounding; keep the same expression for the completion percentage.

## How to verify
`uv run pytest -q` and `uv run labcheck w5d25`
