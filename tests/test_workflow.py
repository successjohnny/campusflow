
"""Unit tests for CampusFlow Pro ticket workflow management."""

import unittest
from typing import TypedDict

from campusflow.workflow import assign_ticket, change_status


class Ticket(TypedDict):
    """Represent a ticket used in workflow tests."""

    id: str
    title: str
    category: str
    urgency: str
    affected_users: int
    priority: str
    status: str
    assigned_to: str | None


class TestWorkflow(unittest.TestCase):

    def setUp(self) -> None:
        self.tickets: list[Ticket] = [
            {
                "id": "T001",
                "title": "Campus Wi-Fi is down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None,
            }
        ]

    def test_assign_ticket(self) -> None:
        result = assign_ticket(self.tickets, "T001", "John")

        self.assertEqual(result["assigned_to"], "John")

    def test_assign_unknown_ticket(self) -> None:
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "John")

    def test_assign_empty_name(self) -> None:
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "")

    def test_unassigned_ticket_cannot_start(self) -> None:
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")

    def test_assigned_ticket_can_start(self) -> None:
        assign_ticket(self.tickets, "T001", "John")

        result = change_status(
            self.tickets, "T001", "in_progress"
        )

        self.assertEqual(result["status"], "in_progress")

    def test_ticket_can_be_resolved(self) -> None:
        assign_ticket(self.tickets, "T001", "John")

        change_status(self.tickets, "T001", "in_progress")

        result = change_status(
            self.tickets, "T001", "resolved"
        )

        self.assertEqual(result["status"], "resolved")

    def test_invalid_status_transition(self) -> None:
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "resolved")

        self.assertEqual(self.tickets[0]["status"], "open")

    def test_reopen_resolved_ticket(self) -> None:
        assign_ticket(self.tickets, "T001", "John")

        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        result = change_status(
            self.tickets, "T001", "open"
        )

        self.assertEqual(result["status"], "open")

    def test_resolved_ticket_cannot_be_assigned(self) -> None:
        assign_ticket(self.tickets, "T001", "John")

        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Mary")

        self.assertEqual(
            self.tickets[0]["assigned_to"],
            "John"
        )

    def test_invalid_current_status(self) -> None:
        self.tickets[0]["status"] = "pending"

        with self.assertRaises(ValueError):
            change_status(
                self.tickets,
                "T001",
                "in_progress"
            )


if __name__ == "__main__":
    unittest.main()