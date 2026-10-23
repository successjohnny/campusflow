"""Duplicate ticket detection for CampusFlow Pro."""

from typing import Any, TypeAlias

Ticket: TypeAlias = dict[str, Any]


def normalize_title(title: str) -> str:
    """Normalize ticket titles for comparison."""

    if not isinstance(title, str):
        raise ValueError("Ticket title must be a string")

    return " ".join(title.split()).casefold()


def detect_duplicates(
    tickets: list[Ticket],
    category: str,
    title: str,
) -> list[Ticket]:
    """Find unresolved tickets with matching category and title."""

    if not isinstance(tickets, list):
        raise TypeError("Tickets must be a list")

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Invalid category")

    normalized_title: str = normalize_title(title)

    if not normalized_title:
        raise ValueError("Ticket title cannot be empty")

    normalized_category: str = category.strip().casefold()

    duplicates: list[Ticket] = []

    for ticket in tickets:
        if ticket["status"] == "resolved":
            continue

        existing_category: str = ticket["category"].strip().casefold()
        existing_title: str = normalize_title(ticket["title"])

        if (
            existing_category == normalized_category
            and existing_title == normalized_title
        ):
            duplicates.append(ticket)

    return duplicates