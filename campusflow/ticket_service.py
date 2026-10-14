"""Ticket creation service for CampusFlow Pro."""

from copy import deepcopy
from datetime import datetime, timezone

from tickets import create_ticket
from storage import save_data

from campusflow.audit import record_event
from campusflow.duplicates import detect_duplicates
from campusflow.sla import calculate_due_at


def create_ticket_service(
    tickets,
    events,
    title,
    category,
    urgency,
    affected_users,
    actor="System",
    confirm_duplicate=False,
    now=None,
    save_func=None,
):
    """Create a ticket with SLA, audit logging, and safe persistence."""

    if now is None:
        now = datetime.now(timezone.utc)

    if not isinstance(now, datetime):
        raise TypeError("now must be a datetime")

    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")

    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("Actor must be a non-empty string")

    if not isinstance(tickets, list) or not isinstance(events, list):
        raise TypeError("Tickets and events must be lists")

    # Check for duplicate tickets before creating anything.
    duplicates = detect_duplicates(tickets, category, title)

    if duplicates and not confirm_duplicate:
        return {
            "created": False,
            "duplicates": duplicates,
            "ticket": None,
        }

    # Work with copies to protect the live application state.
    new_tickets = deepcopy(tickets)
    new_events = deepcopy(events)

    ticket = create_ticket(
        new_tickets,
        title,
        category,
        urgency,
        affected_users,
    )

    now = now.astimezone(timezone.utc)

    ticket["created_at"] = now.isoformat()
    ticket["updated_at"] = now.isoformat()
    ticket["due_at"] = calculate_due_at(ticket["priority"], now)
    ticket["escalation_cycle"] = 0

    record_event(
        new_events,
        ticket_id=ticket["id"],
        event_type="CREATE",
        actor=actor,
        before_status=None,
        after_status="open",
        details={"title": ticket["title"]},
        now=now,
    )

    # Allow test code to inject a temporary storage function.
    if save_func is None:
        save_func = save_data

    # If saving fails, the original lists remain unchanged.
    save_func(new_tickets, new_events)

    # Commit successful changes to the live application state.
    tickets[:] = new_tickets
    events[:] = new_events

    return {
        "created": True,
        "duplicates": duplicates,
        "ticket": ticket,
    }