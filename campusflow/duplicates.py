"""Duplicate ticket detection for CampusFlow Pro."""


def normalize_title(title):
    """Normalize ticket titles for comparison."""

    if not isinstance(title, str):
        raise ValueError("Ticket title must be a string")

    return " ".join(title.split()).casefold()


def detect_duplicates(tickets, category, title):
    """Find unresolved tickets with matching category and title."""

    if not isinstance(tickets, list):
        raise TypeError("Tickets must be a list")

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Invalid category")

    normalized_title = normalize_title(title)

    if not normalized_title:
        raise ValueError("Ticket title cannot be empty")

    normalized_category = category.strip().casefold()

    duplicates = []

    for ticket in tickets:
        if ticket["status"] == "resolved":
            continue

        existing_category = ticket["category"].strip().casefold()
        existing_title = normalize_title(ticket["title"])

        if (
            existing_category == normalized_category
            and existing_title == normalized_title
        ):
            duplicates.append(ticket)

    return duplicates