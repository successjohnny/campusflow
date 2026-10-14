"""CampusFlow Pro command-line interface."""

from storage import load_data

from campusflow.ticket_service import create_ticket_service

from campusflow.workflow_service import (
    assign_ticket_service,
    change_status_service,
)

from campusflow.reports import (
    get_priority_queue,
    generate_report,
)

from campusflow.knowledge_lab import run_quiz


# ============================================================
# MAIN MENU
# ============================================================

def show_menu():
    """Display the CampusFlow main menu."""

    print("\n===== CAMPUSFLOW PRO HELPDESK =====")

    print("1. Create Ticket")
    print("2. View All Tickets")
    print("3. View Ticket Details")
    print("4. Assign Ticket")
    print("5. Update Ticket Status")
    print("6. View Priority Queue")
    print("7. Generate Reports")
    print("8. Knowledge Lab")
    print("0. Exit")


# ============================================================
# CREATE TICKET
# ============================================================

def create_ticket_menu(tickets, events):
    """Create a ticket with SLA and audit logging."""

    print("\n--- CREATE TICKET ---")

    title = input("Title: ")

    category = input(
        "Category (Network/Hardware/Software/Other): "
    )

    urgency = input(
        "Urgency (low/medium/high): "
    )

    try:
        affected_users = int(
            input("Affected users: ")
        )

        actor = input(
            "Created by: "
        ).strip()

        result = create_ticket_service(
            tickets=tickets,
            events=events,
            title=title,
            category=category,
            urgency=urgency,
            affected_users=affected_users,
            actor=actor,
        )

        # Check whether a duplicate ticket exists.
        if not result["created"]:

            print("\nPossible duplicate tickets found:")

            for ticket in result["duplicates"]:
                print(
                    f"{ticket['id']} | "
                    f"{ticket['title']} | "
                    f"Status: {ticket['status']}"
                )

            confirmation = input(
                "\nCreate this ticket anyway? (yes/no): "
            ).strip().lower()

            if confirmation not in {"yes", "y"}:
                print("Ticket creation cancelled.")
                return

            result = create_ticket_service(
                tickets=tickets,
                events=events,
                title=title,
                category=category,
                urgency=urgency,
                affected_users=affected_users,
                actor=actor,
                confirm_duplicate=True,
            )

        ticket = result["ticket"]

        print(
            f"\nTicket {ticket['id']} created successfully!"
        )

        print(
            f"Priority: {ticket['priority']}"
        )

        print(
            f"SLA Deadline: {ticket['due_at']}"
        )

    except ValueError as error:
        print(f"Error: {error}")


# ============================================================
# VIEW ALL TICKETS
# ============================================================

def list_tickets(tickets):
    """Display all tickets."""

    print("\n--- ALL TICKETS ---")

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print(
            f"{ticket['id']} | "
            f"{ticket['title']} | "
            f"Priority: {ticket['priority']} | "
            f"Status: {ticket['status']}"
        )


# ============================================================
# VIEW TICKET DETAILS
# ============================================================

def view_ticket(tickets):
    """Display details of a selected ticket."""

    print("\n--- TICKET DETAILS ---")

    ticket_id = input(
        "Enter ticket ID: "
    ).strip().upper()

    for ticket in tickets:

        if ticket["id"] == ticket_id:

            for key, value in ticket.items():
                print(f"{key}: {value}")

            return

    print("Ticket not found.")


# ============================================================
# ASSIGN TICKET
# ============================================================

def assign_ticket_menu(tickets, events):
    """Assign a ticket with audit logging."""

    print("\n--- ASSIGN TICKET ---")

    ticket_id = input(
        "Ticket ID: "
    ).strip().upper()

    staff_name = input(
        "Staff name: "
    )

    actor = input(
        "Assigned by: "
    ).strip()

    try:
        ticket = assign_ticket_service(
            tickets=tickets,
            events=events,
            ticket_id=ticket_id,
            staff_name=staff_name,
            actor=actor,
        )

        print(
            f"\nTicket {ticket['id']} assigned to "
            f"{ticket['assigned_to']}."
        )

        print("Audit event recorded: ASSIGN")

    except ValueError as error:
        print(f"Error: {error}")


# ============================================================
# UPDATE TICKET STATUS
# ============================================================

def update_status_menu(tickets, events):
    """Update ticket status with audit logging."""

    print("\n--- UPDATE TICKET STATUS ---")

    ticket_id = input(
        "Ticket ID: "
    ).strip().upper()

    print("\nAvailable statuses:")

    print("1. in_progress")
    print("2. resolved")
    print("3. open (reopen a resolved ticket)")

    choices = {
        "1": "in_progress",
        "2": "resolved",
        "3": "open",
    }

    choice = input(
        "Choose status: "
    ).strip()

    new_status = choices.get(choice)

    if new_status is None:
        print("Invalid status option.")
        return

    actor = input(
        "Updated by: "
    ).strip()

    try:
        ticket = change_status_service(
            tickets=tickets,
            events=events,
            ticket_id=ticket_id,
            new_status=new_status,
            actor=actor,
        )

        print(
            f"\nTicket {ticket['id']} status updated to "
            f"{ticket['status']}."
        )

        if new_status == "open":

            print(
                f"New SLA Deadline: {ticket['due_at']}"
            )

        event_types = {
            "in_progress": "START",
            "resolved": "RESOLVE",
            "open": "REOPEN",
        }

        print(
            f"Audit event recorded: {event_types[new_status]}"
        )

    except ValueError as error:
        print(f"Error: {error}")


# ============================================================
# PRIORITY QUEUE
# ============================================================

def priority_queue_menu(tickets):
    """Display tickets ordered by priority."""

    print("\n--- PRIORITY QUEUE ---")

    queue = get_priority_queue(tickets)

    if not queue:
        print("No open tickets in the queue.")
        return

    for ticket in queue:
        print(
            f"{ticket['id']} | "
            f"{ticket['title']} | "
            f"Priority: {ticket['priority']} | "
            f"Status: {ticket['status']}"
        )


# ============================================================
# GENERATE REPORTS
# ============================================================

def reports_menu(tickets):
    """Display standard CampusFlow reports."""

    print("\n--- CAMPUSFLOW REPORT ---")

    report = generate_report(tickets)

    print(
        f"\nTotal Tickets: {report['total']}"
    )

    print("\nTickets by Status:")

    for status, count in report["by_status"].items():
        print(
            f"  {status}: {count}"
        )

    print("\nTickets by Priority:")

    for priority, count in report["by_priority"].items():
        print(
            f"  {priority}: {count}"
        )


# ============================================================
# KNOWLEDGE LAB
# ============================================================

def knowledge_lab_menu():
    """Launch the interactive Knowledge Lab."""

    run_quiz()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():
    """Run the CampusFlow Pro application."""

    try:
        data = load_data()

        tickets = data["tickets"]
        events = data["events"]

    except (ValueError, OSError) as error:
        print(
            f"Unable to load tickets: {error}"
        )
        return

    while True:

        show_menu()

        try:
            choice = input(
                "Choose an option: "
            ).strip()

            if choice == "1":
                create_ticket_menu(
                    tickets,
                    events,
                )

            elif choice == "2":
                list_tickets(tickets)

            elif choice == "3":
                view_ticket(tickets)

            elif choice == "4":
                assign_ticket_menu(
                    tickets,
                    events,
                )

            elif choice == "5":
                update_status_menu(
                    tickets,
                    events,
                )

            elif choice == "6":
                priority_queue_menu(tickets)

            elif choice == "7":
                reports_menu(tickets)

            elif choice == "8":
                knowledge_lab_menu()

            elif choice == "0":
                print(
                    "\nThank you for using CampusFlow Pro!"
                )
                break

            else:
                print(
                    "Invalid option. Try again."
                )

        except (EOFError, KeyboardInterrupt):
            print("\nExiting CampusFlow.")
            break

        except OSError as error:
            print(f"Storage error: {error}")
            print(
                "Exiting to avoid unsaved changes."
            )
            break


if __name__ == "__main__":
    main()