
from datetime import datetime, timedelta, timezone


def main() -> None:
    """Demonstrate the exact SLA deadline boundary."""

    # Create a fixed UTC timestamp
    created_at: datetime = datetime(
        2026, 10, 14, 10, 0, tzinfo=timezone.utc
    )

    # A critical ticket has a 60-minute SLA
    due_at: datetime = created_at + timedelta(minutes=60)

    # Simulate two different times
    exactly_due: datetime = created_at + timedelta(minutes=60)
    one_minute_late: datetime = created_at + timedelta(minutes=61)

    print("Created at:", created_at.isoformat())
    print("Due at:", due_at.isoformat())

    print("Overdue at 60 minutes:", exactly_due > due_at)
    print("Overdue at 61 minutes:", one_minute_late > due_at)


if __name__ == "__main__":
    main()