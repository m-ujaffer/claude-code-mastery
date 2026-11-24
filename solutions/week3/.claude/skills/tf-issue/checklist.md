# Diff review checklist

- [ ] Only files relevant to the issue changed
- [ ] No existing test was weakened or deleted
- [ ] Edge cases: empty, None, boundaries, "today", "done"
- [ ] Conventions: SQL in repository.py, rules in services.py, HTTP in api/, time from taskforge.clock
- [ ] No injection (no user input formatted into SQL), no secrets, no new dependencies
- [ ] No debug prints, commented-out code or unused imports
