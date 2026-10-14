"""Reporting and ticket queues for CampusFlow Pro."""

from datetime import datetime, timezone


def get_priority_queue(tickets):
    """Return open tickets sorted by priority and numeric ticket ID."""

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    open_tickets = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]

    sorted_tickets = sorted(
        open_tickets,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:]),
        ),
    )

    return sorted_tickets


def get_sla_attention_queue(tickets, now):
    """Return unresolved tickets ordered by SLA urgency."""

    if not isinstance(tickets, list):
        raise TypeError("Tickets must be a list")

    if not isinstance(now, datetime):
        raise TypeError("now must be a datetime")

    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")

    current = now.astimezone(timezone.utc)

    attention_queue = []

    for ticket in tickets:
        if ticket["status"] == "resolved":
            continue

        due_at = datetime.fromisoformat(ticket["due_at"])

        if due_at.tzinfo is None or due_at.utcoffset() is None:
            raise ValueError("Ticket deadline must be timezone-aware")

        deadline = due_at.astimezone(timezone.utc)

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
    """Generate ticket counts by status and priority."""

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