
"""Unit tests for the CampusFlow Pro SLA engine."""

import unittest
from datetime import datetime, timedelta, timezone

from campusflow.sla import calculate_due_at, is_overdue


class TestSLAEngine(unittest.TestCase):

    def setUp(self):
        """Use a fixed UTC time for repeatable tests."""
        self.start = datetime(
            2026, 10, 14, 10, 0,
            tzinfo=timezone.utc
        )

    def make_ticket(self, priority="critical", status="open"):
        """Create a sample ticket for testing."""
        return {
            "status": status,
            "priority": priority,
            "due_at": calculate_due_at(priority, self.start),
        }

    def test_critical_deadline(self):
        due = calculate_due_at("critical", self.start)

        self.assertEqual(
            due,
            "2026-10-14T11:00:00+00:00"
        )

    def test_high_deadline(self):
        due = calculate_due_at("high", self.start)

        self.assertEqual(
            due,
            "2026-10-14T14:00:00+00:00"
        )

    def test_medium_deadline(self):
        due = calculate_due_at("medium", self.start)

        self.assertEqual(
            due,
            "2026-10-15T10:00:00+00:00"
        )

    def test_low_deadline(self):
        due = calculate_due_at("low", self.start)

        self.assertEqual(
            due,
            "2026-10-16T10:00:00+00:00"
        )

    def test_exact_deadline_not_overdue(self):
        ticket = self.make_ticket()
        now = self.start + timedelta(minutes=60)

        self.assertFalse(is_overdue(ticket, now))

    def test_one_minute_late_is_overdue(self):
        ticket = self.make_ticket()
        now = self.start + timedelta(minutes=61)

        self.assertTrue(is_overdue(ticket, now))

    def test_one_microsecond_late_is_overdue(self):
        ticket = self.make_ticket()
        now = self.start + timedelta(
            minutes=60,
            microseconds=1
        )

        self.assertTrue(is_overdue(ticket, now))

    def test_resolved_ticket_not_overdue(self):
        ticket = self.make_ticket(status="resolved")
        now = self.start + timedelta(hours=5)

        self.assertFalse(is_overdue(ticket, now))

    def test_in_progress_ticket_overdue(self):
        ticket = self.make_ticket(status="in_progress")
        now = self.start + timedelta(minutes=61)

        self.assertTrue(is_overdue(ticket, now))

    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            calculate_due_at("urgent", self.start)

    def test_naive_start_time_rejected(self):
        naive_time = datetime(2026, 10, 14, 10, 0)

        with self.assertRaises(ValueError):
            calculate_due_at("critical", naive_time)

    def test_naive_current_time_rejected(self):
        ticket = self.make_ticket()
        naive_now = datetime(2026, 10, 14, 12, 0)

        with self.assertRaises(ValueError):
            is_overdue(ticket, naive_now)


if __name__ == "__main__":
    unittest.main()