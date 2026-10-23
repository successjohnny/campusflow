
"""Tests for CampusFlow Pro audit event recording."""

import unittest

from datetime import datetime, timezone

from campusflow.audit import record_event, get_ticket_history


class TestAuditEvents(unittest.TestCase):

    def setUp(self) -> None:
        self.events = []

        self.now = datetime(
            2026, 10, 14, 10, 0,
            tzinfo=timezone.utc
        )

    def test_create_event(self) -> None:
        event = record_event(
            self.events,
            "T001",
            "CREATE",
            "Moses",
            None,
            "open",
            now=self.now,
        )

        self.assertEqual(len(self.events), 1)
        self.assertEqual(event["event_type"], "CREATE")
        self.assertEqual(event["ticket_id"], "T001")
        self.assertEqual(event["actor"], "Moses")
        self.assertEqual(event["after_status"], "open")
        self.assertEqual(
            event["timestamp"],
            "2026-10-14T10:00:00+00:00",
        )

    def test_invalid_actor_does_not_append(self) -> None:
        with self.assertRaises(ValueError):
            record_event(
                self.events,
                "T001",
                "CREATE",
                "",
                None,
                "open",
                now=self.now,
            )

        self.assertEqual(len(self.events), 0)

    def test_invalid_event_type_does_not_append(self) -> None:
        with self.assertRaises(ValueError):
            record_event(
                self.events,
                "T001",
                "DELETE",
                "Moses",
                "open",
                "open",
                now=self.now,
            )

        self.assertEqual(len(self.events), 0)

    def test_naive_datetime_rejected(self) -> None:
        naive_time = datetime(2026, 10, 14, 10, 0)

        with self.assertRaises(ValueError):
            record_event(
                self.events,
                "T001",
                "CREATE",
                "Moses",
                None,
                "open",
                now=naive_time,
            )

        self.assertEqual(len(self.events), 0)

    def test_event_ids_are_unique(self) -> None:
        first = record_event(
            self.events,
            "T001",
            "CREATE",
            "Moses",
            None,
            "open",
            now=self.now,
        )

        second = record_event(
            self.events,
            "T001",
            "ASSIGN",
            "Moses",
            "open",
            "open",
            now=self.now,
        )

        self.assertNotEqual(
            first["event_id"],
            second["event_id"],
        )

    def test_ticket_history_chronological(self) -> None:
        later = datetime(
            2026, 10, 14, 12, 0,
            tzinfo=timezone.utc
        )

        earlier = datetime(
            2026, 10, 14, 10, 0,
            tzinfo=timezone.utc
        )

        record_event(
            self.events,
            "T001",
            "ASSIGN",
            "Moses",
            "open",
            "open",
            now=later,
        )

        record_event(
            self.events,
            "T001",
            "CREATE",
            "Moses",
            None,
            "open",
            now=earlier,
        )

        history = get_ticket_history(
            self.events,
            "T001",
        )

        self.assertEqual(
            history[0]["event_type"],
            "CREATE",
        )

        self.assertEqual(
            history[1]["event_type"],
            "ASSIGN",
        )

    def test_history_excludes_other_tickets(self) -> None:
        record_event(
            self.events,
            "T001",
            "CREATE",
            "Moses",
            None,
            "open",
            now=self.now,
        )

        record_event(
            self.events,
            "T002",
            "CREATE",
            "John",
            None,
            "open",
            now=self.now,
        )

        history = get_ticket_history(
            self.events,
            "T001",
        )

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["ticket_id"], "T001")

    def test_history_breaks_timestamp_ties_by_event_id(
        self,
    ) -> None:
        record_event(
            self.events,
            "T001",
            "CREATE",
            "Moses",
            None,
            "open",
            now=self.now,
        )

        record_event(
            self.events,
            "T001",
            "ASSIGN",
            "Moses",
            "open",
            "open",
            now=self.now,
        )

        self.events[0]["event_id"] = "b"
        self.events[1]["event_id"] = "a"

        history = get_ticket_history(
            self.events,
            "T001",
        )

        self.assertEqual(
            [event["event_id"] for event in history],
            ["a", "b"],
        )


if __name__ == "__main__":
    unittest.main()