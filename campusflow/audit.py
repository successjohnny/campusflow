"""Audit event recording and ticket history for CampusFlow Pro."""

from datetime import datetime, timezone
from typing import Any, TypeAlias
from uuid import uuid4


Event: TypeAlias = dict[str, Any]
Events: TypeAlias = list[Event]
TicketId: TypeAlias = str | int


EVENT_TYPES: set[str] = {
    "CREATE",
    "ASSIGN",
    "START",
    "RESOLVE",
    "REOPEN",
}

VALID_STATUSES: set[str] = {
    "open",
    "in_progress",
    "resolved",
}


def record_event(
    events: Events,
    ticket_id: TicketId,
    event_type: str,
    actor: str,
    before_status: str | None,
    after_status: str | None,
    details: dict[str, Any] | None = None,
    now: datetime | None = None,
) -> Event:
    """Validate and append a successful ticket operation event."""

    if not isinstance(events, list):
        raise TypeError("Events must be a list")

    if (
        not isinstance(ticket_id, (str, int))
        or isinstance(ticket_id, bool)
        or not str(ticket_id).strip()
    ):
        raise ValueError("Invalid ticket ID")

    if event_type not in EVENT_TYPES:
        raise ValueError("Invalid event type")

    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("Actor must be a non-empty string")

    for status in (before_status, after_status):
        if status is not None and status not in VALID_STATUSES:
            raise ValueError("Invalid ticket status")

    if details is None:
        details = {}

    if not isinstance(details, dict):
        raise ValueError("Event details must be a dictionary")

    if now is None:
        now = datetime.now(timezone.utc)

    if not isinstance(now, datetime):
        raise TypeError("Timestamp must be a datetime")

    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Timestamp must be timezone-aware")

    timestamp: str = now.astimezone(timezone.utc).isoformat()

    event: Event = {
        "event_id": str(uuid4()),
        "ticket_id": ticket_id,
        "event_type": event_type,
        "actor": actor.strip(),
        "timestamp": timestamp,
        "before_status": before_status,
        "after_status": after_status,
        "details": details.copy(),
    }

    events.append(event)

    return event


def get_ticket_history(events: Events, ticket_id: TicketId) -> Events:
    """Return one ticket's events in chronological order."""

    history: Events = [
        event
        for event in events
        if event["ticket_id"] == ticket_id
    ]

    return sorted(
        history,
        key=lambda event: (
            datetime.fromisoformat(event["timestamp"]),
            str(event["event_id"]),
        ),
    )