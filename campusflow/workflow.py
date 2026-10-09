def assign_ticket(tickets, ticket_id, staff_name):
    # Check that the staff name is valid
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be empty")

    # Search for the ticket
    for ticket in tickets:
        if ticket["id"] == ticket_id:

            # Resolved tickets cannot be modified
            if ticket["status"] == "resolved":
                raise ValueError("Reopen the ticket before assigning it")

            # Assign the staff member
            ticket["assigned_to"] = staff_name.strip()

            return ticket

    raise ValueError("Ticket not found")


def change_status(tickets, ticket_id, new_status):
    # Define allowed status transitions
    allowed = {
        "open": ["in_progress"],
        "in_progress": ["resolved"],
        "resolved": ["open"]
    }

    # Validate the new status
    if not isinstance(new_status, str):
        raise ValueError("Invalid status")

    new_status = new_status.strip().lower()

    # Search for the ticket
    for ticket in tickets:
        if ticket["id"] == ticket_id:

            current_status = ticket["status"]

            # Check if the current status is valid
            if current_status not in allowed:
                raise ValueError("Invalid current ticket status")

            # Check whether the transition is allowed
            if new_status not in allowed[current_status]:
                raise ValueError("Invalid status transition")

            # Check whether a staff member is assigned
            if new_status == "in_progress" and not ticket["assigned_to"]:
                raise ValueError("Assign the ticket before starting work")

            # Update the status
            ticket["status"] = new_status

            return ticket

    raise ValueError("Ticket not found")