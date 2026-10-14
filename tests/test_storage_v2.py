
"""Tests for CampusFlow Pro JSON v2 persistence."""

import json
import tempfile
import unittest
from pathlib import Path

from unittest.mock import patch

from storage import load_data, save_data, validate_data


class TestStorageV2(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "tickets.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_file_returns_empty_v2_document(self):
        data = load_data(self.path)

        self.assertEqual(data["schema_version"], 2)
        self.assertEqual(data["tickets"], [])
        self.assertEqual(data["events"], [])

    def test_save_and_load_empty_document(self):
        save_data([], [], self.path)

        data = load_data(self.path)

        self.assertEqual(
            data,
            {
                "schema_version": 2,
                "tickets": [],
                "events": [],
            },
        )

    def test_reject_corrupt_json(self):
        self.path.write_text("{invalid json", encoding="utf-8")

        with self.assertRaises(ValueError):
            load_data(self.path)

        self.assertEqual(
            self.path.read_text(encoding="utf-8"),
            "{invalid json",
        )

    def test_reject_wrong_schema_version(self):
        self.path.write_text(
            json.dumps({
                "schema_version": 1,
                "tickets": [],
                "events": [],
            }),
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            load_data(self.path)

    def test_reject_missing_events(self):
        data = {
            "schema_version": 2,
            "tickets": [],
        }

        with self.assertRaises(ValueError):
            validate_data(data)

    def test_invalid_save_preserves_existing_file(self):
        original = '{"important": "keep this data"}'
        self.path.write_text(original, encoding="utf-8")

        with self.assertRaises(ValueError):
            save_data([{"id": "T001"}], [], self.path)

        self.assertEqual(
            self.path.read_text(encoding="utf-8"),
            original,
        )

    
    def make_ticket(self):
        return {
            "id": 1,
            "title": "Campus internet unavailable",
            "category": "Network",
            "urgency": "high",
            "affected_users": 20,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
            "created_at": "2026-10-14T10:00:00+00:00",
            "updated_at": "2026-10-14T10:00:00+00:00",
            "due_at": "2026-10-14T11:00:00+00:00",
            "escalation_cycle": 0,
        }

    def make_event(self):
        return {
            "event_id": "event-001",
            "ticket_id": 1,
            "event_type": "CREATE",
            "actor": "Engineer A",
            "timestamp": "2026-10-14T10:00:00+00:00",
            "before_status": None,
            "after_status": "open",
            "details": {},
        }

    def test_save_and_load_ticket_with_event(self):
        ticket = self.make_ticket()
        event = self.make_event()

        save_data([ticket], [event], self.path)
        loaded = load_data(self.path)

        self.assertEqual(loaded["tickets"], [ticket])
        self.assertEqual(loaded["events"], [event])

    def test_duplicate_ticket_ids_rejected(self):
        ticket = self.make_ticket()

        with self.assertRaises(ValueError):
            save_data([ticket, ticket.copy()], [], self.path)

        self.assertFalse(self.path.exists())

    def test_duplicate_event_ids_rejected(self):
        ticket = self.make_ticket()
        event = self.make_event()

        with self.assertRaises(ValueError):
            save_data([ticket], [event, event.copy()], self.path)

        self.assertFalse(self.path.exists())

    def test_unknown_ticket_reference_rejected(self):
        ticket = self.make_ticket()
        event = self.make_event()
        event["ticket_id"] = 999

        with self.assertRaises(ValueError):
            save_data([ticket], [event], self.path)

        self.assertFalse(self.path.exists())

    def test_corrupt_load_does_not_change_existing_data(self):
        original_tickets = [self.make_ticket()]
        original_events = [self.make_event()]

        self.path.write_text("{broken json", encoding="utf-8")

        with self.assertRaises(ValueError):
            load_data(self.path)

        self.assertEqual(len(original_tickets), 1)
        self.assertEqual(len(original_events), 1)

    def test_invalid_timestamp_rejected(self):
        ticket = self.make_ticket()
        ticket["created_at"] = "not-a-date"

        with self.assertRaises(ValueError):
            save_data([ticket], [], self.path)

        self.assertFalse(self.path.exists())

    def test_atomic_replace_failure_preserves_original_file(self):
        """A failed replacement must not destroy existing data."""
        ticket = self.make_ticket()
        event = self.make_event()

        # First save a valid document.
        save_data([ticket], [event], self.path)

        original_content = self.path.read_text(encoding="utf-8")

        # Simulate failure during the final replacement.
        with patch("storage.os.replace", side_effect=OSError("Disk error")):
            with self.assertRaises(OSError):
                save_data([], [], self.path)

        # The existing file must remain unchanged.
        self.assertEqual(
            self.path.read_text(encoding="utf-8"),
            original_content,
        )

        # The original data must still load successfully.
        loaded = load_data(self.path)

        self.assertEqual(loaded["tickets"], [ticket])
        self.assertEqual(loaded["events"], [event])


if __name__ == "__main__":
    unittest.main()