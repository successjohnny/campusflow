
from tickets import create_ticket
from storage import load_tickets, save_tickets


def show_menu():
    print("\n===== CAMPUSFLOW HELPDESK =====")
    print("1. Create Ticket")
    print("2. View All Tickets")
    print("3. View Ticket Details")
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
            tickets,
            title,
            category,
            urgency,
            affected_users
        )

        save_tickets(tickets)

        print(f"\nTicket {ticket['id']} created!")
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
            f"{ticket['priority']} | "
            f"{ticket['status']}"
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


def main():
    try:
        tickets = load_tickets()
    except (ValueError, OSError) as error:
        print(f"Unable to load tickets: {error}")
        return

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_ticket_menu(tickets)

        elif choice == "2":
            list_tickets(tickets)

        elif choice == "3":
            view_ticket(tickets)

        elif choice == "0":
            print("Thank you for using CampusFlow!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()