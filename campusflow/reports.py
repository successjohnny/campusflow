"""Reporting and ticket queues for CampusFlow Pro."""

from datetime import datetime, timezone
from typing import Any, TypeAlias, TypedDict


Ticket: TypeAlias = dict[str, Any]
Event: TypeAlias = dict[str, Any]


class StandardReport(TypedDict):
    total: int
    by_status: dict[str, int]
    by_priority: dict[str, int]


class EnhancedReport(TypedDict):
    overdue_total: int
    overdue_by_priority: dict[str, int]
    average_resolution_hours: float
    staff_workload: dict[str, int]
    resolution_rate_percent: float


PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def get_priority_queue(tickets: list[Ticket]) -> list[Ticket]:
    """Return open tickets sorted by priority and numeric ticket ID."""

    open_tickets: list[Ticket] = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]

    return sorted(
        open_tickets,
        key=lambda ticket: (
            PRIORITY_ORDER[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )


def _utc_datetime(value: datetime | str, name: str) -> datetime:
    """Convert an aware datetime or ISO timestamp to UTC."""

    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError as error:
            raise ValueError(f"Invalid {name}") from error

    if not isinstance(value, datetime):
        raise TypeError(f"{name} must be a datetime")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")

    return value.astimezone(timezone.utc)


def get_sla_attention_queue(
    tickets: list[Ticket],
    now: datetime | str,
) -> list[Ticket]:
    """Return unresolved tickets ordered by SLA urgency."""

    if not isinstance(tickets, list):
        raise TypeError("Tickets must be a list")

    current: datetime = _utc_datetime(now, "now")

    attention_queue: list[tuple[int, datetime, int, Ticket]] = []

    for ticket in tickets:
        if ticket["status"] == "resolved":
            continue

        deadline: datetime = _utc_datetime(
            ticket["due_at"],
            "due_at",
        )

        overdue_rank: int = 0 if current > deadline else 1

        attention_queue.append(
            (
                overdue_rank,
                deadline,
                int(ticket["id"][1:]),
                ticket,
            )
        )

    attention_queue.sort(
        key=lambda item: (
            item[0],
            item[1],
            item[2],
        )
    )

    return [
        item[3]
        for item in attention_queue
    ]


def generate_report(tickets: list[Ticket]) -> StandardReport:
    """Generate original ticket counts by status and priority."""

    report: StandardReport = {
        "total": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0,
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
    }

    for ticket in tickets:
        status: str = ticket["status"]
        priority: str = ticket["priority"]

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1

    return report


def generate_enhanced_report(
    tickets: list[Ticket],
    events: list[Event],
    now: datetime | str,
) -> EnhancedReport:
    """Calculate SLA, resolution, and staff workload statistics."""

    if not isinstance(tickets, list):
        raise TypeError("Tickets must be a list")

    if not isinstance(events, list):
        raise TypeError("Events must be a list")

    current: datetime = _utc_datetime(now, "now")

    report: EnhancedReport = {
        "overdue_total": 0,
        "overdue_by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
        "average_resolution_hours": 0.0,
        "staff_workload": {},
        "resolution_rate_percent": 0.0,
    }

    latest_resolutions: dict[str | int, datetime] = {}

    for event in events:
        if event["event_type"] != "RESOLVE":
            continue

        ticket_id: str | int = event["ticket_id"]

        resolved_at: datetime = _utc_datetime(
            event["timestamp"],
            "event timestamp",
        )

        previous = latest_resolutions.get(ticket_id)

        if previous is None or resolved_at > previous:
            latest_resolutions[ticket_id] = resolved_at

    resolved_count: int = 0
    resolution_hours: list[float] = []

    for ticket in tickets:
        status: str = ticket["status"]

        if status == "resolved":
            resolved_count += 1

            resolved_at = latest_resolutions.get(
                ticket["id"]
            )

            if resolved_at is not None:
                created_at: datetime = _utc_datetime(
                    ticket["created_at"],
                    "created_at",
                )

                duration = resolved_at - created_at

                if duration.total_seconds() < 0:
                    raise ValueError(
                        "Resolution precedes ticket creation"
                    )

                resolution_hours.append(
                    duration.total_seconds() / 3600
                )

            continue

        deadline: datetime = _utc_datetime(
            ticket["due_at"],
            "due_at",
        )

        if current > deadline:
            report["overdue_total"] += 1

            priority: str = ticket["priority"]

            report["overdue_by_priority"][priority] += 1

        staff_name: str | None = ticket.get("assigned_to")

        if staff_name:
            report["staff_workload"][staff_name] = (
                report["staff_workload"].get(staff_name, 0)
                + 1
            )

    if tickets:
        report["resolution_rate_percent"] = round(
            resolved_count / len(tickets) * 100,
            2,
        )

    if resolution_hours:
        report["average_resolution_hours"] = round(
            sum(resolution_hours) / len(resolution_hours),
            2,
        )

    return report