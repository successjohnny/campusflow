
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "tickets.json"


def load_tickets(file_path=DATA_FILE):
    """Load saved tickets from JSON."""

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
        raise ValueError(
            "Ticket storage must contain a list"
        )

    return tickets


def save_tickets(tickets, file_path=DATA_FILE):
    """Save tickets to JSON storage."""

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)