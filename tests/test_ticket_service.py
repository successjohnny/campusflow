
"""Tests for CampusFlow Pro ticket creation service."""

import unittest
from datetime import datetime, timezone
from typing import Any
from unittest.mock import Mock

from campusflow.ticket_service import create_ticket_service


class TestTicketService(unittest.TestCase):

    def setUp(self) -> None:
        self.tickets: list[dict[str, Any]] = []
        self.events: list[dict[str, Any]] = []

        self.now: datetime = datetime(
            2026, 10, 14, 12, 0,
            tzinfo=timezone.utc,
        )

        self.save: Mock = Mock()

    def create_sample_ticket(
        self,
        **overrides: Any,
    ) -> dict[str, Any]:
        """Create a sample ticket with optional test overrides."""
        data: dict[str, Any] = {
            "tickets": self.tickets,
            "events": self.events,
            "title": "Campus network outage",
            "category": "Network",
            "urgency": "high",
            "affected_users": 15,
            "actor": "Moses",
            "now": self.now,
            "save_func": self.save,
        }

        data.update(overrides)

        return create_ticket_service(**data)

    def test_creates_ticket_successfully(self) -> None:
        result = self.create_sample_ticket()

        self.assertTrue(result["created"])
        self.assertEqual(len(self.tickets), 1)
        self.assertEqual(self.tickets[0]["id"], "T001")

    def test_calculates_sla_deadline(self) -> None:
        self.create_sample_ticket()

        ticket = self.tickets[0]

        self.assertEqual(
            ticket["due_at"],
            "2026-10-14T13:00:00+00:00",
        )

    def test_records_create_event(self) -> None:
        self.create_sample_ticket()

        self.assertEqual(len(self.events), 1)
        self.assertEqual(self.events[0]["event_type"], "CREATE")
        self.assertEqual(self.events[0]["actor"], "Moses")

    def test_saves_tickets_and_events(self) -> None:
        self.create_sample_ticket()

        self.save.assert_called_once()

        saved_tickets, saved_events = self.save.call_args.args

        self.assertEqual(len(saved_tickets), 1)
        self.assertEqual(len(saved_events), 1)

    def test_detects_duplicate_ticket(self) -> None:
        self.create_sample_ticket()

        result = self.create_sample_ticket(
            title="  CAMPUS NETWORK OUTAGE  ",
        )

        self.assertFalse(result["created"])
        self.assertEqual(len(result["duplicates"]), 1)
        self.assertEqual(len(self.tickets), 1)

    def test_allows_confirmed_duplicate(self) -> None:
        self.create_sample_ticket()

        result = self.create_sample_ticket(
            confirm_duplicate=True,
        )

        self.assertTrue(result["created"])
        self.assertEqual(len(self.tickets), 2)

    def test_failed_save_does_not_change_state(self) -> None:
        self.save.side_effect = OSError("Disk failure")

        with self.assertRaises(OSError):
            self.create_sample_ticket()

        self.assertEqual(self.tickets, [])
        self.assertEqual(self.events, [])

    def test_invalid_title_does_not_change_state(self) -> None:
        with self.assertRaises(ValueError):
            self.create_sample_ticket(title="   ")

        self.assertEqual(self.tickets, [])
        self.assertEqual(self.events, [])

    def test_invalid_actor_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.create_sample_ticket(actor=" ")

    def test_naive_datetime_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.create_sample_ticket(
                now=datetime(2026, 10, 14, 12, 0),
            )


if __name__ == "__main__":
    unittest.main()