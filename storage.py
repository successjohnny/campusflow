
"""JSON persistence for CampusFlow and CampusFlow Pro."""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "data" / "tickets.json"

SCHEMA_VERSION = 2

TICKET_FIELDS = {
    "id", "title", "category", "urgency",
    "affected_users", "priority", "status",
    "assigned_to", "created_at", "updated_at",
    "due_at", "escalation_cycle",
}

EVENT_FIELDS = {
    "event_id", "ticket_id", "event_type", "actor",
    "timestamp", "before_status", "after_status",
    "details",
}

STATUSES = {"open", "in_progress", "resolved"}
EVENT_TYPES = {
    "CREATE", "ASSIGN", "START",
    "RESOLVE", "REOPEN", "ESCALATE",
}


def validate_timestamp(value):
    """Return a valid timezone-aware UTC datetime."""
    if not isinstance(value, str):
        raise ValueError("Timestamp must be a string")

    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as error:
        raise ValueError("Invalid ISO-8601 timestamp") from error

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Timestamp must include a timezone")

    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError("Timestamp must be in UTC")

    return parsed.astimezone(timezone.utc)


def validate_data(data):
    """Validate a complete CampusFlow Pro document."""
    if not isinstance(data, dict):
        raise ValueError("Storage must contain a JSON object")

    if type(data.get("schema_version")) is not int:
        raise ValueError("Invalid schema version")

    if data["schema_version"] != SCHEMA_VERSION:
        raise ValueError("Unsupported schema version")

    tickets = data.get("tickets")
    events = data.get("events")

    if not isinstance(tickets, list):
        raise ValueError("Tickets must be a list")

    if not isinstance(events, list):
        raise ValueError("Events must be a list")

    ticket_ids = set()

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Invalid ticket record")

        if not TICKET_FIELDS.issubset(ticket):
            raise ValueError("Ticket is missing required fields")

        ticket_id = ticket["id"]

        if not isinstance(ticket_id, (str, int)):
            raise ValueError("Invalid ticket ID")

        if isinstance(ticket_id, bool):
            raise ValueError("Invalid ticket ID")

        if ticket_id in ticket_ids:
            raise ValueError("Duplicate ticket ID")

        ticket_ids.add(ticket_id)

        if not isinstance(ticket["title"], str) or not ticket["title"].strip():
            raise ValueError("Invalid ticket title")

        if not isinstance(ticket["category"], str) or not ticket["category"].strip():
            raise ValueError("Invalid ticket category")

        if ticket["status"] not in STATUSES:
            raise ValueError("Invalid ticket status")

        if ticket["priority"] not in {
            "critical", "high", "medium", "low"
        }:
            raise ValueError("Invalid ticket priority")

        if type(ticket["escalation_cycle"]) is not int:
            raise ValueError("Invalid escalation cycle")

        if ticket["escalation_cycle"] < 0:
            raise ValueError("Invalid escalation cycle")

        created = validate_timestamp(ticket["created_at"])
        updated = validate_timestamp(ticket["updated_at"])
        due = validate_timestamp(ticket["due_at"])

        if updated < created:
            raise ValueError("Updated time precedes creation")

        if due < created:
            raise ValueError("Deadline precedes creation")

    event_ids = set()

    for event in events:
        if not isinstance(event, dict):
            raise ValueError("Invalid audit event")

        if not EVENT_FIELDS.issubset(event):
            raise ValueError("Event is missing required fields")

        event_id = event["event_id"]

        if not isinstance(event_id, (str, int)) or isinstance(event_id, bool):
            raise ValueError("Invalid event ID")

        if event_id in event_ids:
            raise ValueError("Duplicate event ID")

        event_ids.add(event_id)

        if event["ticket_id"] not in ticket_ids:
            raise ValueError("Event references unknown ticket")

        if event["event_type"] not in EVENT_TYPES:
            raise ValueError("Invalid event type")

        if not isinstance(event["actor"], str) or not event["actor"].strip():
            raise ValueError("Invalid event actor")

        validate_timestamp(event["timestamp"])

        for field in ("before_status", "after_status"):
            if event[field] is not None and event[field] not in STATUSES:
                raise ValueError("Invalid event status")

        if not isinstance(event["details"], dict):
            raise ValueError("Event details must be an object")

        if event["event_type"] == "ESCALATE":
            cycle = event["details"].get("escalation_cycle")

            if type(cycle) is not int or cycle < 0:
                raise ValueError("Invalid escalation event cycle")

    return True


def load_data(file_path=DATA_FILE):
    """Load and validate schema v2 without changing application state."""
    path = Path(file_path)

    if not path.exists():
        return {
            "schema_version": SCHEMA_VERSION,
            "tickets": [],
            "events": [],
        }

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError("Storage contains invalid JSON") from error

    validate_data(data)
    return data


def save_data(tickets, events, file_path=DATA_FILE):
    """Validate and atomically save schema v2."""
    data = {
        "schema_version": SCHEMA_VERSION,
        "tickets": tickets,
        "events": events,
    }

    validate_data(data)

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(data, temporary_file, indent=4, allow_nan=False)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.replace(temporary_path, path)

    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


# Original CampusFlow functions retained for compatibility.

def load_tickets(file_path=DATA_FILE):
    """Load legacy CampusFlow ticket-list storage."""
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Ticket storage contains invalid JSON"
        ) from error

    if not isinstance(tickets, list):
        raise ValueError("Ticket storage must contain a list")

    return tickets


def save_tickets(tickets, file_path=DATA_FILE):
    """Save legacy CampusFlow ticket-list storage."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)