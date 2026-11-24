"""Single source of "now" for the app.

Always call ``clock.today()`` / ``clock.now()`` instead of ``date.today()`` so
tests can freeze time with ``monkeypatch.setattr(clock, "today", ...)``.
"""

from datetime import UTC, date, datetime


def today() -> date:
    return date.today()


def now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)
