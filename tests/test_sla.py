
"""Unit tests for the CampusFlow Pro SLA engine."""

import unittest
from datetime import UTC, datetime, timedelta
from typing import NotRequired, TypedDict

from campusflow.sla import (
    calculate_due_at,
    escalate_overdue,
    is_overdue,
)


class Ticket(TypedDict):
    status: str
    priority: str
    due_at: str
    id: NotRequired[str]
    escalation_cycle: NotRequired[int]


class Event(TypedDict, total=False):
    event_id: str
    ticket_id: str
    event_type: str
    actor: str
    timestamp: str
    before_status: str
    after_status: str
    details: dict[str, object]


class TestSLAEngine(unittest.TestCase):

    def setUp(self) -> None:
        """Use a fixed UTC time for repeatable tests."""
        self.start: datetime = datetime(
            2026, 10, 14, 10, 0,
            tzinfo=UTC
        )

    def make_ticket(
        self,
        priority: str = "critical",
        status: str = "open",
    ) -> Ticket:
        """Create a sample ticket for testing."""
        return {
            "status": status,
            "priority": priority,
            "due_at": calculate_due_at(priority, self.start),
        }

    def test_critical_deadline(self) -> None:
        due: str = calculate_due_at("critical", self.start)

        self.assertEqual(
            due,
            "2026-10-14T11:00:00+00:00"
        )

    def test_high_deadline(self) -> None:
        due: str = calculate_due_at("high", self.start)

        self.assertEqual(
            due,
            "2026-10-14T14:00:00+00:00"
        )

    def test_medium_deadline(self) -> None:
        due: str = calculate_due_at("medium", self.start)

        self.assertEqual(
            due,
            "2026-10-15T10:00:00+00:00"
        )

    def test_low_deadline(self) -> None:
        due: str = calculate_due_at("low", self.start)

        self.assertEqual(
            due,
            "2026-10-16T10:00:00+00:00"
        )

    def test_exact_deadline_not_overdue(self) -> None:
        ticket: Ticket = self.make_ticket()
        now: datetime = self.start + timedelta(minutes=60)

        self.assertFalse(is_overdue(ticket, now))

    def test_one_minute_late_is_overdue(self) -> None:
        ticket: Ticket = self.make_ticket()
        now: datetime = self.start + timedelta(minutes=61)

        self.assertTrue(is_overdue(ticket, now))

    def test_one_microsecond_late_is_overdue(self) -> None:
        ticket: Ticket = self.make_ticket()
        now: datetime = self.start + timedelta(
            minutes=60,
            microseconds=1
        )

        self.assertTrue(is_overdue(ticket, now))

    def test_resolved_ticket_not_overdue(self) -> None:
        ticket: Ticket = self.make_ticket(status="resolved")
        now: datetime = self.start + timedelta(hours=5)

        self.assertFalse(is_overdue(ticket, now))

    def test_in_progress_ticket_overdue(self) -> None:
        ticket: Ticket = self.make_ticket(status="in_progress")
        now: datetime = self.start + timedelta(minutes=61)

        self.assertTrue(is_overdue(ticket, now))

    def test_invalid_priority(self) -> None:
        with self.assertRaises(ValueError):
            calculate_due_at("urgent", self.start)

    def test_naive_start_time_rejected(self) -> None:
        naive_time: datetime = datetime(2026, 10, 14, 10, 0)

        with self.assertRaises(ValueError):
            calculate_due_at("critical", naive_time)

    def test_naive_current_time_rejected(self) -> None:
        ticket: Ticket = self.make_ticket()
        naive_now: datetime = datetime(2026, 10, 14, 12, 0)

        with self.assertRaises(ValueError):
            is_overdue(ticket, naive_now)

    def test_first_escalation(self) -> None:
        ticket: Ticket = self.make_ticket()
        ticket["id"] = "T001"
        ticket["escalation_cycle"] = 0

        events: list[Event] = []
        now: datetime = self.start + timedelta(minutes=61)

        result = escalate_overdue(
            [ticket], events, now, "Engineer A"
        )

        self.assertEqual(result["newly_escalated"], 1)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_type"], "ESCALATE")

    def test_repeated_escalation_is_idempotent(self) -> None:
        ticket: Ticket = self.make_ticket()
        ticket["id"] = "T001"
        ticket["escalation_cycle"] = 0

        events: list[Event] = []
        now: datetime = self.start + timedelta(minutes=61)

        escalate_overdue([ticket], events, now, "Engineer A")
        result = escalate_overdue(
            [ticket], events, now, "Engineer A"
        )

        self.assertEqual(result["newly_escalated"], 0)
        self.assertEqual(result["already_escalated"], 1)
        self.assertEqual(len(events), 1)

    def test_reopened_ticket_can_escalate_again(self) -> None:
        ticket: Ticket = self.make_ticket()
        ticket["id"] = "T001"
        ticket["escalation_cycle"] = 0

        events: list[Event] = []
        first_overdue: datetime = self.start + timedelta(minutes=61)

        escalate_overdue(
            [ticket], events, first_overdue, "Engineer A"
        )

        # Simulate a new SLA cycle after reopening.
        reopened_at: datetime = self.start + timedelta(hours=2)
        ticket["escalation_cycle"] = 1
        ticket["due_at"] = calculate_due_at(
            "critical", reopened_at
        )

        second_overdue: datetime = reopened_at + timedelta(minutes=61)

        result = escalate_overdue(
            [ticket], events, second_overdue, "Engineer A"
        )

        self.assertEqual(result["newly_escalated"], 1)
        self.assertEqual(len(events), 2)

    def test_not_overdue_does_not_escalate(self) -> None:
        ticket: Ticket = self.make_ticket()
        ticket["id"] = "T001"
        ticket["escalation_cycle"] = 0

        events: list[Event] = []
        now: datetime = self.start + timedelta(minutes=60)

        result = escalate_overdue(
            [ticket], events, now, "Engineer A"
        )

        self.assertEqual(result["newly_escalated"], 0)
        self.assertEqual(len(events), 0)

    def test_escalation_has_unique_event_id(self) -> None:
        ticket: Ticket = self.make_ticket()
        ticket["id"] = "T001"
        ticket["escalation_cycle"] = 0

        events: list[Event] = []
        now: datetime = self.start + timedelta(minutes=61)

        escalate_overdue([ticket], events, now, "Engineer A")

        self.assertIsInstance(events[0]["event_id"], str)
        self.assertTrue(events[0]["event_id"])

    def test_invalid_ticket_does_not_create_partial_events(self) -> None:
        first: Ticket = self.make_ticket()
        first["id"] = "T001"
        first["escalation_cycle"] = 0

        invalid: Ticket = self.make_ticket()
        invalid["id"] = "T002"
        invalid["escalation_cycle"] = -1

        events: list[Event] = []
        now: datetime = self.start + timedelta(minutes=61)

        with self.assertRaises(ValueError):
            escalate_overdue(
                [first, invalid], events, now, "Engineer A"
            )

        self.assertEqual(events, [])


if __name__ == "__main__":
    unittest.main()