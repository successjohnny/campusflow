
"""Ticket creation service for CampusFlow Pro."""

from collections.abc import Callable
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any, TypedDict

from campusflow.audit import record_event
from campusflow.duplicates import detect_duplicates
from campusflow.sla import calculate_due_at
from storage import save_data
from tickets import Ticket as BaseTicket
from tickets import create_ticket

Ticket = dict[str, Any]
Event = dict[str, Any]
SaveFunction = Callable[[list[Ticket], list[Event]], None]


class CreateTicketResult(TypedDict):
    """Result returned after attempting to create a ticket."""

    created: bool
    duplicates: list[Ticket]
    ticket: Ticket | None


def create_ticket_service(
    tickets: list[Ticket],
    events: list[Event],
    title: str,
    category: str,
    urgency: str,
    affected_users: int,
    actor: str = "System",
    confirm_duplicate: bool = False,
    now: datetime | None = None,
    save_func: SaveFunction | None = None,
) -> CreateTicketResult:
    """Create a ticket with SLA, audit logging, and safe persistence."""

    if now is None:
        now = datetime.now(UTC)

    if not isinstance(now, datetime):
        raise TypeError("now must be a datetime")

    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")

    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("Actor must be a non-empty string")

    if not isinstance(tickets, list) or not isinstance(events, list):
        raise TypeError("Tickets and events must be lists")

    duplicates: list[Ticket] = detect_duplicates(
        tickets,
        category,
        title,
    )

    if duplicates and not confirm_duplicate:
        return {
            "created": False,
            "duplicates": duplicates,
            "ticket": None,
        }

    # Preserve original state until persistence succeeds.
    new_tickets: list[Ticket] = deepcopy(tickets)
    new_events: list[Event] = deepcopy(events)

    # Build a typed view for the original ticket creation function.
    typed_tickets: list[BaseTicket] = [
        {
            "id": item["id"],
            "title": item["title"],
            "category": item["category"],
            "urgency": item["urgency"],
            "affected_users": item["affected_users"],
            "priority": item["priority"],
            "status": item["status"],
            "assigned_to": item["assigned_to"],
        }
        for item in new_tickets
    ]

    created_ticket: BaseTicket = create_ticket(
        typed_tickets,
        title,
        category,
        urgency,
        affected_users,
    )

    # Use the newly created ticket as a normal dictionary.
    ticket: Ticket = dict(created_ticket)
    new_tickets.append(ticket)

    now = now.astimezone(UTC)

    ticket["created_at"] = now.isoformat()
    ticket["updated_at"] = now.isoformat()
    ticket["due_at"] = calculate_due_at(
        ticket["priority"],
        now,
    )
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

    persistence: SaveFunction = (
        save_data if save_func is None else save_func
    )

    persistence(new_tickets, new_events)

    tickets[:] = new_tickets
    events[:] = new_events

    return {
        "created": True,
        "duplicates": duplicates,
        "ticket": ticket,
    }