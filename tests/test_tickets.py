
import unittest

from tickets import create_ticket, calculate_priority


class TestTickets(unittest.TestCase):

    def setUp(self):
        self.tickets = []

    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_priority(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_medium_priority(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_zero_users_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Wi-Fi", "Network", "high", 0)

        self.assertEqual(self.tickets, [])

    def test_blank_title_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, " ", "Network", "low", 2)

    def test_invalid_category_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Wi-Fi", "Unknown", "low", 2)

    def test_ticket_creation(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi down", "Network", "high", 15
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_unique_ticket_ids(self):
        create_ticket(self.tickets, "Wi-Fi", "Network", "high", 15)
        second = create_ticket(
            self.tickets, "Laptop", "Hardware", "low", 1
        )

        self.assertEqual(second["id"], "T002")

    def test_case_normalization(self):
        ticket = create_ticket(
            self.tickets, "Laptop", "HARDWARE", "HIGH", 2
        )

        self.assertEqual(ticket["category"], "Hardware")
        self.assertEqual(ticket["urgency"], "high")

    def test_next_id_after_existing_ticket(self):
        self.tickets.append({
            "id": "T007",
            "title": "Existing",
            "category": "Software",
            "urgency": "low",
            "affected_users": 1,
            "priority": "low",
            "status": "open",
            "assigned_to": None
        })

        ticket = create_ticket(
            self.tickets, "New issue", "Network", "low", 1
        )

        self.assertEqual(ticket["id"], "T008")


if __name__ == "__main__":
    unittest.main()