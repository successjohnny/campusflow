
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path

from tickets import create_ticket, calculate_priority
from storage import save_tickets, load_tickets


class TestCampusFlow(unittest.TestCase):

    def setUp(self):
        self.tickets = []

    def test_create_ticket(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi down", "Network", "High", 30
        )

        self.assertEqual(ticket["id"], 1)
        self.assertEqual(ticket["status"], "Open")
        self.assertIsNone(ticket["assigned_to"])

    def test_priority(self):
        self.assertEqual(calculate_priority("High", 30), "Critical")
        self.assertEqual(calculate_priority("Medium", 5), "Medium")

    def test_unique_ids(self):
        first = create_ticket(
            self.tickets, "Laptop faulty", "Hardware", "Low", 1
        )
        second = create_ticket(
            self.tickets, "Wi-Fi down", "Network", "High", 25
        )

        self.assertNotEqual(first["id"], second["id"])

    def test_invalid_users(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, "Wi-Fi down", "Network", "High", -2
            )

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            create_ticket(
                self.tickets, " ", "Network", "Low", 1
            )

    def test_json_storage(self):
        create_ticket(
            self.tickets, "Wi-Fi down", "Network", "High", 30
        )

        with TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            save_tickets(self.tickets, path)
            loaded = load_tickets(path)

        self.assertEqual(loaded, self.tickets)


if __name__ == "__main__":
    unittest.main()