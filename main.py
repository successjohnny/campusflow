
from tickets import create_ticket
from storage import load_tickets, save_tickets
from campusflow.workflow import assign_ticket, change_status
from campusflow.reports import get_priority_queue, generate_report


def show_menu():
    print("\n===== CAMPUSFLOW HELPDESK =====")
    print("1. Create Ticket")
    print("2. View All Tickets")
    print("3. View Ticket Details")
    print("4. Assign Ticket")
    print("5. Update Ticket Status")
    print("6. View Priority Queue")
    print("7. Generate Reports")
    print("0. Exit")


def create_ticket_menu(tickets):
    print("\n--- CREATE TICKET ---")

    title = input("Title: ")
    category = input(
        "Category (Network/Hardware/Software/Other): "
    )
    urgency = input("Urgency (low/medium/high): ")

    try:
        affected_users = int(input("Affected users: "))

        ticket = create_ticket(
            tickets, title, category, urgency, affected_users
        )

        save_tickets(tickets)

        print(f"\nTicket {ticket['id']} created successfully!")
        print(f"Priority: {ticket['priority']}")

    except ValueError as error:
        print(f"Error: {error}")


def list_tickets(tickets):
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


def view_ticket(tickets):
    ticket_id = input("Enter ticket ID: ").strip().upper()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            print("\n--- TICKET DETAILS ---")

            for key, value in ticket.items():
                print(f"{key}: {value}")

            return

    print("Ticket not found.")


def assign_ticket_menu(tickets):
    print("\n--- ASSIGN TICKET ---")

    ticket_id = input("Ticket ID: ").strip().upper()
    staff_name = input("Staff name: ")

    try:
        ticket = assign_ticket(tickets, ticket_id, staff_name)
        save_tickets(tickets)

        print(
            f"Ticket {ticket['id']} assigned to "
            f"{ticket['assigned_to']}."
        )

    except ValueError as error:
        print(f"Error: {error}")


def update_status_menu(tickets):
    print("\n--- UPDATE TICKET STATUS ---")

    ticket_id = input("Ticket ID: ").strip().upper()

    print("Available statuses:")
    print("1. in_progress")
    print("2. resolved")
    print("3. open (reopen a resolved ticket)")

    choices = {
        "1": "in_progress",
        "2": "resolved",
        "3": "open"
    }

    choice = input("Choose status: ").strip()
    new_status = choices.get(choice)

    if new_status is None:
        print("Invalid status option.")
        return

    try:
        ticket = change_status(tickets, ticket_id, new_status)
        save_tickets(tickets)

        print(
            f"Ticket {ticket['id']} status updated to "
            f"{ticket['status']}."
        )

    except ValueError as error:
        print(f"Error: {error}")


def priority_queue_menu(tickets):
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


def reports_menu(tickets):
    print("\n--- CAMPUSFLOW REPORT ---")

    report = generate_report(tickets)

    print(f"\nTotal Tickets: {report['total']}")

    print("\nTickets by Status:")
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")

    print("\nTickets by Priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")


def main():
    try:
        tickets = load_tickets()

    except (ValueError, OSError) as error:
        print(f"Unable to load tickets: {error}")
        return

    while True:
        show_menu()

        try:
            choice = input("Choose an option: ").strip()

            if choice == "1":
                create_ticket_menu(tickets)

            elif choice == "2":
                list_tickets(tickets)

            elif choice == "3":
                view_ticket(tickets)

            elif choice == "4":
                assign_ticket_menu(tickets)

            elif choice == "5":
                update_status_menu(tickets)

            elif choice == "6":
                priority_queue_menu(tickets)

            elif choice == "7":
                reports_menu(tickets)

            elif choice == "0":
                print("Thank you for using CampusFlow!")
                break

            else:
                print("Invalid option. Try again.")

        except (EOFError, KeyboardInterrupt):
            print("\nExiting CampusFlow.")
            break

        except OSError as error:
            print(f"Storage error: {error}")
            print("Exiting to avoid unsaved changes.")
            break


if __name__ == "__main__":
    main()
