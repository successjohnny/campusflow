"""Tests for the CampusFlow Pro SLA Attention Queue."""

import unittest

from datetime import datetime, timezone

from campusflow.reports import (
    get_priority_queue,
    get_sla_attention_queue,
)


class TestSLAAttentionQueue(unittest.TestCase):

    def setUp(self):
        self.now = datetime(
            2026, 10, 14, 12, 0,
            tzinfo=timezone.utc,
        )

        self.tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "high",
                "due_at": "2026-10-14T11:00:00+00:00",
            },
            {
                "id": "T002",
                "status": "in_progress",
                "priority": "critical",
                "due_at": "2026-10-14T10:00:00+00:00",
            },
            {
                "id": "T003",
                "status": "open",
                "priority": "medium",
                "due_at": "2026-10-14T14:00:00+00:00",
            },
            {
                "id": "T004",
                "status": "resolved",
                "priority": "critical",
                "due_at": "2026-10-14T09:00:00+00:00",
            },
        ]

    def test_overdue_tickets_first(self):
        queue = get_sla_attention_queue(
            self.tickets,
            self.now,
        )

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T001", "T003"],
        )

    def test_in_progress_ticket_is_included(self):
        queue = get_sla_attention_queue(
            self.tickets,
            self.now,
        )

        ids = [ticket["id"] for ticket in queue]

        self.assertIn("T002", ids)

    def test_resolved_ticket_is_excluded(self):
        queue = get_sla_attention_queue(
            self.tickets,
            self.now,
        )

        ids = [ticket["id"] for ticket in queue]

        self.assertNotIn("T004", ids)

    def test_earliest_deadline_first(self):
        queue = get_sla_attention_queue(
            self.tickets,
            self.now,
        )

        self.assertEqual(queue[0]["id"], "T002")

    def test_numeric_ticket_id_breaks_ties(self):
        tickets = [
            {
                "id": "T010",
                "status": "open",
                "priority": "high",
                "due_at": "2026-10-14T11:00:00+00:00",
            },
            {
                "id": "T002",
                "status": "open",
                "priority": "high",
                "due_at": "2026-10-14T11:00:00+00:00",
            },
        ]

        queue = get_sla_attention_queue(
            tickets,
            self.now,
        )

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T010"],
        )

    def test_exact_deadline_is_not_overdue(self):
        tickets = [
            {
                "id": "T001",
                "status": "open",
                "priority": "high",
                "due_at": "2026-10-14T12:00:00+00:00",
            },
            {
                "id": "T002",
                "status": "open",
                "priority": "high",
                "due_at": "2026-10-14T11:59:00+00:00",
            },
        ]

        queue = get_sla_attention_queue(
            tickets,
            self.now,
        )

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T001"],
        )

    def test_empty_queue(self):
        queue = get_sla_attention_queue([], self.now)

        self.assertEqual(queue, [])

    def test_naive_datetime_rejected(self):
        naive_now = datetime(2026, 10, 14, 12, 0)

        with self.assertRaises(ValueError):
            get_sla_attention_queue(
                self.tickets,
                naive_now,
            )

    def test_original_tickets_not_modified(self):
        original = [
            ticket.copy()
            for ticket in self.tickets
        ]

        get_sla_attention_queue(
            self.tickets,
            self.now,
        )

        self.assertEqual(self.tickets, original)

    def test_existing_priority_queue_still_works(self):
        queue = get_priority_queue(self.tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001", "T003"],
        )


if __name__ == "__main__":
    unittest.main()