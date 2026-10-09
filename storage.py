
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "tickets.json"


def load_tickets(file_path=DATA_FILE):
    """Load tickets from JSON storage."""
    path = Path(file_path)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Ticket storage must contain a list")

    return data


def save_tickets(tickets, file_path=DATA_FILE):
    """Save tickets to JSON storage."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)