import unittest
from campusflow.workflow import assign_ticket, change_status


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.tickets = [
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

    def test_assign_ticket(self):
        result = assign_ticket(self.tickets, "T001", "John")

        self.assertEqual(result["assigned_to"], "John")

    def test_assign_unknown_ticket(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "John")

    def test_assign_empty_name(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "")

    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")

    def test_assigned_ticket_can_start(self):
        assign_ticket(self.tickets, "T001", "John")

        result = change_status(
            self.tickets, "T001", "in_progress"
        )

        self.assertEqual(result["status"], "in_progress")

    def test_ticket_can_be_resolved(self):
        assign_ticket(self.tickets, "T001", "John")

        change_status(self.tickets, "T001", "in_progress")

        result = change_status(self.tickets, "T001", "resolved")

        self.assertEqual(result["status"], "resolved")

    def test_invalid_status_transition(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "resolved")

        self.assertEqual(self.tickets[0]["status"], "open")

    def test_reopen_resolved_ticket(self):
        assign_ticket(self.tickets, "T001", "John")

        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        result = change_status(self.tickets, "T001", "open")

        self.assertEqual(result["status"], "open")

    def test_resolved_ticket_cannot_be_assigned(self):
        assign_ticket(self.tickets, "T001", "John")

        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Mary")

        self.assertEqual(self.tickets[0]["assigned_to"], "John")

    def test_invalid_current_status(self):
        self.tickets[0]["status"] = "pending"

        with self.assertRaises(ValueError):
            change_status(
                self.tickets,
                "T001",
                "in_progress"
            )


if __name__ == "__main__":
    unittest.main()