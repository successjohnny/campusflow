
VALID_URGENCIES = ("Low", "Medium", "High")


def calculate_priority(urgency, affected_users):
    """Calculate ticket priority from urgency and affected users."""
    if urgency not in VALID_URGENCIES:
        raise ValueError("Urgency must be Low, Medium, or High")

    if type(affected_users) is not int or affected_users < 1:
        raise ValueError("Affected users must be a positive integer")

    if urgency == "High" and affected_users >= 20:
        return "Critical"

    return urgency


def create_ticket(tickets, title, category, urgency, affected_users):
    """Create and append a new helpdesk ticket."""
    if not title.strip():
        raise ValueError("Ticket title cannot be empty")

    if not category.strip():
        raise ValueError("Ticket category cannot be empty")

    priority = calculate_priority(urgency, affected_users)

    ticket_id = max((ticket["id"] for ticket in tickets), default=0) + 1

    ticket = {
        "id": ticket_id,
        "title": title.strip(),
        "category": category.strip(),
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "Open",
        "assigned_to": None
    }

    tickets.append(ticket)
    return ticket