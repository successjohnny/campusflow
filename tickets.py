
VALID_CATEGORIES = ("Network", "Hardware", "Software", "Other")
VALID_URGENCIES = ("low", "medium", "high")


def calculate_priority(urgency, affected_users):
    """Calculate priority using CampusFlow's four rules."""

    if urgency not in VALID_URGENCIES:
        raise ValueError("Invalid urgency")

    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError("Affected users must be a positive integer")

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate inputs and create a new ticket."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty")

    if not isinstance(category, str):
        raise ValueError("Invalid category")

    category = category.strip().lower()

    categories = {
        "network": "Network",
        "hardware": "Hardware",
        "software": "Software",
        "other": "Other"
    }

    if category not in categories:
        raise ValueError("Invalid category")

    if not isinstance(urgency, str):
        raise ValueError("Invalid urgency")

    urgency = urgency.strip().lower()

    priority = calculate_priority(urgency, affected_users)

    next_id = max(
        (int(ticket["id"][1:]) for ticket in tickets),
        default=0
    ) + 1

    ticket = {
        "id": f"T{next_id:03d}",
        "title": title.strip(),
        "category": categories[category],
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None
    }

    tickets.append(ticket)

    return ticket