"""Reporting and ticket queues for CampusFlow Pro."""

from datetime import datetime, timezone


PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def get_priority_queue(tickets):
    """Return open tickets sorted by priority and numeric ticket ID."""

    open_tickets = [
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


def _utc_datetime(value, name):
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


def get_sla_attention_queue(tickets, now):
    """Return unresolved tickets ordered by SLA urgency."""

    if not isinstance(tickets, list):
        raise TypeError("Tickets must be a list")

    current = _utc_datetime(now, "now")

    attention_queue = []

    for ticket in tickets:
        if ticket["status"] == "resolved":
            continue

        deadline = _utc_datetime(
            ticket["due_at"],
            "due_at",
        )

        overdue_rank = 0 if current > deadline else 1

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


def generate_report(tickets):
    """Generate original ticket counts by status and priority."""

    report = {
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
        status = ticket["status"]
        priority = ticket["priority"]

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1

    return report


def generate_enhanced_report(tickets, events, now):
    """Calculate SLA, resolution, and staff workload statistics."""

    if not isinstance(tickets, list):
        raise TypeError("Tickets must be a list")

    if not isinstance(events, list):
        raise TypeError("Events must be a list")

    current = _utc_datetime(now, "now")

    report = {
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

    latest_resolutions = {}

    for event in events:
        if event["event_type"] != "RESOLVE":
            continue

        ticket_id = event["ticket_id"]

        resolved_at = _utc_datetime(
            event["timestamp"],
            "event timestamp",
        )

        previous = latest_resolutions.get(ticket_id)

        if previous is None or resolved_at > previous:
            latest_resolutions[ticket_id] = resolved_at

    resolved_count = 0
    resolution_hours = []

    for ticket in tickets:
        status = ticket["status"]

        if status == "resolved":
            resolved_count += 1

            resolved_at = latest_resolutions.get(
                ticket["id"]
            )

            if resolved_at is not None:
                created_at = _utc_datetime(
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

        deadline = _utc_datetime(
            ticket["due_at"],
            "due_at",
        )

        if current > deadline:
            report["overdue_total"] += 1

            priority = ticket["priority"]

            report["overdue_by_priority"][priority] += 1

        staff_name = ticket.get("assigned_to")

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