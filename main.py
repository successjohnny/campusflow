"""CampusFlow Pro command-line interface."""

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, TypeAlias

from storage import load_data, save_data
from campusflow.audit import get_ticket_history
from campusflow.knowledge_lab import run_quiz
from campusflow.reports import (
    generate_enhanced_report,
    generate_report,
    get_priority_queue,
    get_sla_attention_queue,
)
from campusflow.sla import escalate_overdue, is_overdue
from campusflow.ticket_service import create_ticket_service
from campusflow.workflow_service import assign_ticket_service, change_status_service

Ticket: TypeAlias = dict[str, Any]
Event: TypeAlias = dict[str, Any]
Tickets: TypeAlias = list[Ticket]
Events: TypeAlias = list[Event]


def show_menu() -> None:
    """Display original operations and CampusFlow Pro extensions."""
    print("\n===== CAMPUSFLOW PRO HELPDESK =====")
    print("1. Create Ticket")
    print("2. View All Tickets")
    print("3. View Ticket Details")
    print("4. Assign Ticket")
    print("5. Update Ticket Status")
    print("6. Original Open Work Queue")
    print("7. Generate Reports")
    print("8. Knowledge Lab")
    print("9. SLA Attention Queue")
    print("10. Ticket History")
    print("11. Check and Escalate Overdue")
    print("12. Reload Saved Data")
    print("0. Exit")


def create_ticket_menu(tickets: Tickets, events: Events) -> None:
    """Create a ticket, warning about unresolved duplicates."""
    print("\n--- CREATE TICKET ---")
    title: str = input("Title: ")
    category: str = input("Category (Network/Hardware/Software/Other): ")
    urgency: str = input("Urgency (low/medium/high): ")
    try:
        affected_users: int = int(input("Affected users: "))
        actor: str = input("Created by (operator label): ").strip()
        result: dict[str, Any] = create_ticket_service(
            tickets=tickets,
            events=events,
            title=title,
            category=category,
            urgency=urgency,
            affected_users=affected_users,
            actor=actor,
        )
        if not result["created"]:
            print("\nPossible duplicate tickets found:")
            for match in result["duplicates"]:
                print(f"{match['id']} | {match['title']} | Status: {match['status']}")
            confirmation: str = input("Create anyway? (yes/no): ").strip().lower()
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
        ticket: Ticket = result["ticket"]
        print(f"\nTicket {ticket['id']} created successfully!")
        print(f"Priority: {ticket['priority']}")
        print(f"SLA Deadline: {ticket['due_at']}")
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def list_tickets(tickets: Tickets) -> None:
    """Display every ticket."""
    print("\n--- ALL TICKETS ---")
    if not tickets:
        print("No tickets found.")
        return
    for ticket in tickets:
        print(
            f"{ticket['id']} | {ticket['title']} | "
            f"Priority: {ticket['priority']} | Status: {ticket['status']}"
        )


def view_ticket(tickets: Tickets) -> None:
    """Display the complete details of one ticket."""
    print("\n--- TICKET DETAILS ---")
    ticket_id: str = input("Enter ticket ID: ").strip().upper()
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            for key, value in ticket.items():
                print(f"{key}: {value}")
            return
    print("Ticket not found.")


def assign_ticket_menu(tickets: Tickets, events: Events) -> None:
    """Assign a ticket and record the successful change."""
    print("\n--- ASSIGN TICKET ---")
    ticket_id: str = input("Ticket ID: ").strip().upper()
    staff_name: str = input("Staff name: ")
    actor: str = input("Assigned by (operator label): ").strip()
    try:
        ticket: Ticket = assign_ticket_service(
            tickets=tickets,
            events=events,
            ticket_id=ticket_id,
            staff_name=staff_name,
            actor=actor,
        )
        print(f"\nTicket {ticket['id']} assigned to {ticket['assigned_to']}.")
        print("Audit event recorded: ASSIGN")
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def update_status_menu(tickets: Tickets, events: Events) -> None:
    """Start, resolve, or reopen a ticket using workflow rules."""
    print("\n--- UPDATE TICKET STATUS ---")
    ticket_id: str = input("Ticket ID: ").strip().upper()
    print("1. in_progress")
    print("2. resolved")
    print("3. open (reopen a resolved ticket)")
    choices: dict[str, str] = {
        "1": "in_progress",
        "2": "resolved",
        "3": "open",
    }
    choice: str = input("Choose status: ").strip()
    new_status: str | None = choices.get(choice)
    if new_status is None:
        print("Invalid status option.")
        return
    actor: str = input("Updated by (operator label): ").strip()
    try:
        ticket: Ticket = change_status_service(
            tickets=tickets,
            events=events,
            ticket_id=ticket_id,
            new_status=new_status,
            actor=actor,
        )
        print(f"\nTicket {ticket['id']} status updated to {ticket['status']}.")
        if new_status == "open":
            print(f"New SLA Deadline: {ticket['due_at']}")
        event_types: dict[str, str] = {
            "in_progress": "START",
            "resolved": "RESOLVE",
            "open": "REOPEN",
        }
        print(f"Audit event recorded: {event_types[new_status]}")
    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def priority_queue_menu(tickets: Tickets) -> None:
    """Show only OPEN tickets in the original priority order."""
    print("\n--- ORIGINAL OPEN WORK QUEUE ---")
    queue: Tickets = get_priority_queue(tickets)
    if not queue:
        print("No open tickets in the queue.")
        return
    for ticket in queue:
        print(
            f"{ticket['id']} | {ticket['title']} | "
            f"Priority: {ticket['priority']} | Status: {ticket['status']}"
        )


def sla_attention_menu(tickets: Tickets) -> None:
    """Show unresolved tickets, overdue first, then nearest deadline."""
    print("\n--- SLA ATTENTION QUEUE ---")
    now: datetime = datetime.now(timezone.utc)
    queue: Tickets = get_sla_attention_queue(tickets, now)
    if not queue:
        print("No unresolved tickets.")
        return
    for ticket in queue:
        label: str = "OVERDUE" if is_overdue(ticket, now) else "On time"
        print(
            f"{ticket['id']} | {ticket['title']} | {label} | "
            f"Due: {ticket['due_at']} | Status: {ticket['status']}"
        )


def history_menu(tickets: Tickets, events: Events) -> None:
    """Show one ticket's events chronologically."""
    print("\n--- TICKET HISTORY ---")
    ticket_id: str = input("Ticket ID: ").strip().upper()
    if not any(ticket["id"] == ticket_id for ticket in tickets):
        print("Ticket not found.")
        return
    history: Events = get_ticket_history(events, ticket_id)
    if not history:
        print("No events recorded for this ticket.")
        return
    for event in history:
        print(
            f"{event['timestamp']} | {event['event_type']} | "
            f"Actor: {event['actor']} | "
            f"{event['before_status']} -> {event['after_status']} | "
            f"Details: {event['details']}"
        )


def escalation_menu(tickets: Tickets, events: Events) -> None:
    """Check overdue tickets and persist new events before committing them."""
    print("\n--- CHECK AND ESCALATE OVERDUE ---")
    actor: str = input("Checked by (operator label): ").strip()
    now: datetime = datetime.now(timezone.utc)
    working_events: Events = deepcopy(events)
    try:
        result: dict[str, int] = escalate_overdue(
            tickets, working_events, now, actor
        )
        if result["newly_escalated"]:
            # Never update the live event list if persistence fails.
            save_data(tickets, working_events)
            events[:] = working_events
        print(f"Newly escalated: {result['newly_escalated']}")
        print(f"Already escalated: {result['already_escalated']}")
    except (ValueError, TypeError, OSError) as error:
        print(f"Escalation failed: {error}")


def reports_menu(tickets: Tickets, events: Events) -> None:
    """Show original analytics plus SLA and escalation metrics."""
    print("\n--- CAMPUSFLOW REPORT ---")
    report: dict[str, Any] = generate_report(tickets)
    print(f"Total Tickets: {report['total']}")
    print("\nTickets by Status:")
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")
    print("\nTickets by Priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")

    now: datetime = datetime.now(timezone.utc)
    enhanced: dict[str, Any] = generate_enhanced_report(tickets, events, now)
    print("\nSLA Metrics:")
    print(f"  Overdue unresolved: {enhanced['overdue_total']}")
    print(f"  Resolution rate: {enhanced['resolution_rate_percent']}%")
    print(f"  Average resolution hours: {enhanced['average_resolution_hours']}")
    print("  Overdue by priority:")
    for priority, count in enhanced["overdue_by_priority"].items():
        print(f"    {priority}: {count}")
    print("  Staff workload:")
    for staff, count in enhanced["staff_workload"].items():
        print(f"    {staff}: {count}")

    escalated_cycles: set[tuple[str | int, int]] = {
        (event["ticket_id"], event["details"]["escalation_cycle"])
        for event in events
        if event["event_type"] == "ESCALATE"
    }
    escalated_count: int = sum(
        (ticket["id"], ticket["escalation_cycle"]) in escalated_cycles
        for ticket in tickets
        if ticket["status"] != "resolved"
    )
    print(f"  Escalated in current cycle (unresolved): {escalated_count}")


def reload_menu(tickets: Tickets, events: Events) -> None:
    """Reload validated saved state without partial in-memory changes."""
    print("\n--- RELOAD SAVED DATA ---")
    confirmation: str = input("Reload from disk? (yes/no): ").strip().lower()
    if confirmation not in {"yes", "y"}:
        print("Reload cancelled.")
        return
    try:
        data: dict[str, Any] = load_data()
        tickets[:] = data["tickets"]
        events[:] = data["events"]
        print("Saved tickets and events loaded successfully.")
    except (ValueError, TypeError, OSError) as error:
        print(f"Reload failed; current data preserved: {error}")


def knowledge_lab_menu() -> None:
    """Launch the independent Engineering Knowledge Lab."""
    run_quiz()


def main() -> None:
    """Run CampusFlow Pro until the operator chooses to exit."""
    try:
        data: dict[str, Any] = load_data()
        tickets: Tickets = data["tickets"]
        events: Events = data["events"]
    except (ValueError, TypeError, OSError) as error:
        print(f"Unable to load tickets: {error}")
        return

    while True:
        show_menu()
        try:
            choice: str = input("Choose an option: ").strip()
            if choice == "1":
                create_ticket_menu(tickets, events)
            elif choice == "2":
                list_tickets(tickets)
            elif choice == "3":
                view_ticket(tickets)
            elif choice == "4":
                assign_ticket_menu(tickets, events)
            elif choice == "5":
                update_status_menu(tickets, events)
            elif choice == "6":
                priority_queue_menu(tickets)
            elif choice == "7":
                reports_menu(tickets, events)
            elif choice == "8":
                knowledge_lab_menu()
            elif choice == "9":
                sla_attention_menu(tickets)
            elif choice == "10":
                history_menu(tickets, events)
            elif choice == "11":
                escalation_menu(tickets, events)
            elif choice == "12":
                reload_menu(tickets, events)
            elif choice == "0":
                print("Thank you for using CampusFlow!")
                break
            else:
                print("Invalid option. Try again.")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting CampusFlow.")
            break
        except (ValueError, TypeError) as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"Storage error: {error}")
            print("Exiting to avoid unsaved changes.")
            break


if __name__ == "__main__":
    main()