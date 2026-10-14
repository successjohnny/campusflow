
"""SLA deadline calculations and escalation for CampusFlow Pro."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4


SLA_MINUTES = {
    "critical": 60,
    "high": 240,
    "medium": 1440,
    "low": 2880,
}


def require_aware_datetime(value, name):
    """Validate and normalize a datetime to UTC."""
    if not isinstance(value, datetime):
        raise TypeError(f"{name} must be a datetime")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")

    return value.astimezone(timezone.utc)


def calculate_due_at(priority, cycle_start):
    """Calculate the SLA deadline in UTC."""
    if priority not in SLA_MINUTES:
        raise ValueError("Invalid ticket priority")

    start = require_aware_datetime(cycle_start, "cycle_start")

    deadline = start + timedelta(minutes=SLA_MINUTES[priority])

    return deadline.isoformat()


def is_overdue(ticket, now):
    """Check whether an unresolved ticket is past its SLA deadline."""
    if ticket["status"] == "resolved":
        return False

    current = require_aware_datetime(now, "now")

    due_at = datetime.fromisoformat(ticket["due_at"])
    due_at = require_aware_datetime(due_at, "due_at")

    return current > due_at


def escalate_overdue(tickets, events, now, actor):
    """Create one escalation event per overdue ticket per SLA cycle."""
    current = require_aware_datetime(now, "now")

    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("Actor must be a non-empty string")

    if not isinstance(tickets, list) or not isinstance(events, list):
        raise TypeError("Tickets and events must be lists")

    actor = actor.strip()

    existing_ids = set()
    escalated_cycles = set()

    # Validate existing escalation events before making changes.
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("Invalid audit event")

        event_id = event.get("event_id")

        if not isinstance(event_id, str) or not event_id:
            raise ValueError("Invalid audit event ID")

        if event_id in existing_ids:
            raise ValueError("Duplicate audit event ID")

        existing_ids.add(event_id)

        if event.get("event_type") == "ESCALATE":
            details = event.get("details")

            if not isinstance(details, dict):
                raise ValueError("Invalid escalation details")

            cycle = details.get("escalation_cycle")

            if type(cycle) is not int or cycle < 0:
                raise ValueError("Invalid escalation cycle")

            escalated_cycles.add((event["ticket_id"], cycle))

    pending = []
    already = 0
    seen_tickets = set()

    # Validate all tickets before appending any events.
    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Invalid ticket")

        ticket_id = ticket["id"]
        cycle = ticket["escalation_cycle"]

        if type(cycle) is not int or cycle < 0:
            raise ValueError("Invalid ticket escalation cycle")

        if ticket_id in seen_tickets:
            raise ValueError("Duplicate ticket ID")

        seen_tickets.add(ticket_id)

        if not is_overdue(ticket, current):
            continue

        key = (ticket_id, cycle)

        if key in escalated_cycles:
            already += 1
            continue

        event = {
            "event_id": str(uuid4()),
            "ticket_id": ticket_id,
            "event_type": "ESCALATE",
            "actor": actor,
            "timestamp": current.isoformat(),
            "before_status": ticket["status"],
            "after_status": ticket["status"],
            "details": {
                "escalation_cycle": cycle,
                "due_at": ticket["due_at"],
            },
        }

        pending.append(event)
        escalated_cycles.add(key)

    # Append only after the complete validation succeeds.
    events.extend(pending)

    return {
        "newly_escalated": len(pending),
        "already_escalated": already,
    }