"""Safe ticket workflow operations for CampusFlow Pro."""

from copy import deepcopy
from datetime import datetime, timezone

from campusflow.audit import record_event
from campusflow.sla import calculate_due_at
from campusflow.workflow import assign_ticket, change_status
from storage import save_data


def _prepare(tickets, events, actor, now):
    """Validate common inputs and create working copies."""

    if not isinstance(tickets, list) or not isinstance(events, list):
        raise TypeError("Tickets and events must be lists")

    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("Actor must be a non-empty string")

    if now is None:
        now = datetime.now(timezone.utc)

    if not isinstance(now, datetime):
        raise TypeError("now must be a datetime")

    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")

    return (
        deepcopy(tickets),
        deepcopy(events),
        now.astimezone(timezone.utc),
    )


def _save_changes(tickets, events, new_tickets, new_events, save_func):
    """Persist changes before updating live application state."""

    if save_func is None:
        save_func = save_data

    save_func(new_tickets, new_events)

    tickets[:] = new_tickets
    events[:] = new_events


def assign_ticket_service(
    tickets,
    events,
    ticket_id,
    staff_name,
    actor="System",
    now=None,
    save_func=None,
):
    """Assign a ticket and record an ASSIGN audit event."""

    new_tickets, new_events, current = _prepare(
        tickets, events, actor, now
    )

    ticket = assign_ticket(new_tickets, ticket_id, staff_name)

    ticket["updated_at"] = current.isoformat()

    record_event(
        new_events,
        ticket_id=ticket["id"],
        event_type="ASSIGN",
        actor=actor,
        before_status=ticket["status"],
        after_status=ticket["status"],
        details={"assigned_to": ticket["assigned_to"]},
        now=current,
    )

    _save_changes(
        tickets, events, new_tickets, new_events, save_func
    )

    return ticket


def change_status_service(
    tickets,
    events,
    ticket_id,
    new_status,
    actor="System",
    now=None,
    save_func=None,
):
    """Change status and record a workflow audit event."""

    new_tickets, new_events, current = _prepare(
        tickets, events, actor, now
    )

    ticket = next(
        (item for item in new_tickets if item["id"] == ticket_id),
        None,
    )

    if ticket is None:
        raise ValueError("Ticket not found")

    previous_status = ticket["status"]

    ticket = change_status(
        new_tickets,
        ticket_id,
        new_status,
    )

    event_types = {
        ("open", "in_progress"): "START",
        ("in_progress", "resolved"): "RESOLVE",
        ("resolved", "open"): "REOPEN",
    }

    event_type = event_types[(previous_status, ticket["status"])]

    ticket["updated_at"] = current.isoformat()

    if event_type == "REOPEN":
        ticket["escalation_cycle"] += 1
        ticket["due_at"] = calculate_due_at(
            ticket["priority"],
            current,
        )

    record_event(
        new_events,
        ticket_id=ticket["id"],
        event_type=event_type,
        actor=actor,
        before_status=previous_status,
        after_status=ticket["status"],
        details={},
        now=current,
    )

    _save_changes(
        tickets, events, new_tickets, new_events, save_func
    )

    return ticket