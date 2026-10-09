
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tickets import create_ticket
from storage import load_tickets, save_tickets


class TestStorage(unittest.TestCase):

    def test_missing_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"
            self.assertEqual(load_tickets(path), [])

    def test_save_and_reload(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = []

            create_ticket(
                tickets, "Wi-Fi down", "Network", "high", 15
            )

            save_tickets(tickets, path)
            loaded = load_tickets(path)

            self.assertEqual(loaded, tickets)

    def test_unique_id_after_reload(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = []

            create_ticket(
                tickets, "Wi-Fi down", "Network", "high", 15
            )

            save_tickets(tickets, path)
            loaded = load_tickets(path)

            new_ticket = create_ticket(
                loaded, "Laptop fault", "Hardware", "low", 1
            )

            self.assertEqual(new_ticket["id"], "T002")

    def test_corrupted_json(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            path.write_text("{invalid json", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(path)


if __name__ == "__main__":
    unittest.main()