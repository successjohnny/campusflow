
"""SLA deadline calculations for CampusFlow Pro."""

from datetime import datetime, timedelta, timezone


SLA_MINUTES = {
    "critical": 60,
    "high": 240,
    "medium": 1440,
    "low": 2880,
}


def calculate_due_at(priority, cycle_start):
    """Return the UTC SLA deadline as an ISO-8601 string."""
    if priority not in SLA_MINUTES:
        raise ValueError("Invalid ticket priority")

    if not isinstance(cycle_start, datetime):
        raise TypeError("cycle_start must be a datetime")

    if cycle_start.tzinfo is None or cycle_start.utcoffset() is None:
        raise ValueError("cycle_start must be timezone-aware")

    utc_start = cycle_start.astimezone(timezone.utc)

    deadline = utc_start + timedelta(
        minutes=SLA_MINUTES[priority]
    )

    return deadline.isoformat()


def is_overdue(ticket, now):
    """Return True only when an unresolved ticket is past its SLA."""
    if ticket["status"] == "resolved":
        return False

    if not isinstance(now, datetime):
        raise TypeError("now must be a datetime")

    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")

    due_at = datetime.fromisoformat(ticket["due_at"])

    if due_at.tzinfo is None or due_at.utcoffset() is None:
        raise ValueError("due_at must be timezone-aware")

    return now.astimezone(timezone.utc) > due_at