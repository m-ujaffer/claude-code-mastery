# W2D7: Does my rule actually change behaviour?

- rule tested: freeze time with monkeypatch on taskforge.clock; use the client/project fixtures
- prompt used for the experiment: Add a test to practice-app/tests that a task due tomorrow is not overdue.
- result without rule: computed tomorrow with date.today() + timedelta(1) and built its own TestClient
- result with rule: monkeypatched clock.today, used the client and project fixtures, named the test test_due_tomorrow_is_not_overdue
- conclusion (keep, reword, or delete the rule?): keep; adding the reason ("flaky on boundaries") made it stick
