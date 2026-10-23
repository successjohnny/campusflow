
"""Tests for CampusFlow Pro workflow services."""

import unittest
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import Mock

from campusflow.ticket_service import create_ticket_service
from campusflow.workflow_service import (
    assign_ticket_service,
    change_status_service,
)


class TestWorkflowService(unittest.TestCase):

    def setUp(self) -> None:
        self.tickets: list[dict[str, Any]] = []
        self.events: list[dict[str, Any]] = []

        self.now: datetime = datetime(
            2026, 10, 14, 12, 0,
            tzinfo=UTC,
        )

        self.save: Mock = Mock()

        create_ticket_service(
            tickets=self.tickets,
            events=self.events,
            title="Network outage",
            category="Network",
            urgency="high",
            affected_users=15,
            actor="Moses",
            now=self.now,
            save_func=self.save,
        )

        self.save.reset_mock()

    def test_assign_ticket(self) -> None:
        ticket = assign_ticket_service(
            self.tickets,
            self.events,
            "T001",
            "Engineer A",
            actor="Moses",
            now=self.now + timedelta(minutes=5),
            save_func=self.save,
        )

        self.assertEqual(ticket["assigned_to"], "Engineer A")
        self.assertEqual(self.events[-1]["event_type"], "ASSIGN")
        self.save.assert_called_once()

    def test_start_ticket(self) -> None:
        assign_ticket_service(
            self.tickets,
            self.events,
            "T001",
            "Engineer A",
            now=self.now,
            save_func=self.save,
        )

        ticket = change_status_service(
            self.tickets,
            self.events,
            "T001",
            "in_progress",
            now=self.now + timedelta(minutes=10),
            save_func=self.save,
        )

        self.assertEqual(ticket["status"], "in_progress")
        self.assertEqual(self.events[-1]["event_type"], "START")

    def test_resolve_ticket(self) -> None:
        assign_ticket_service(
            self.tickets,
            self.events,
            "T001",
            "Engineer A",
            now=self.now,
            save_func=self.save,
        )

        change_status_service(
            self.tickets,
            self.events,
            "T001",
            "in_progress",
            now=self.now + timedelta(minutes=5),
            save_func=self.save,
        )

        ticket = change_status_service(
            self.tickets,
            self.events,
            "T001",
            "resolved",
            now=self.now + timedelta(minutes=20),
            save_func=self.save,
        )

        self.assertEqual(ticket["status"], "resolved")
        self.assertEqual(self.events[-1]["event_type"], "RESOLVE")

    def test_reopen_ticket_recalculates_sla(self) -> None:
        assign_ticket_service(
            self.tickets,
            self.events,
            "T001",
            "Engineer A",
            now=self.now,
            save_func=self.save,
        )

        change_status_service(
            self.tickets,
            self.events,
            "T001",
            "in_progress",
            now=self.now + timedelta(minutes=5),
            save_func=self.save,
        )

        change_status_service(
            self.tickets,
            self.events,
            "T001",
            "resolved",
            now=self.now + timedelta(minutes=20),
            save_func=self.save,
        )

        ticket = change_status_service(
            self.tickets,
            self.events,
            "T001",
            "open",
            now=self.now + timedelta(hours=2),
            save_func=self.save,
        )

        self.assertEqual(ticket["status"], "open")
        self.assertEqual(ticket["escalation_cycle"], 1)
        self.assertEqual(
            ticket["due_at"],
            "2026-10-14T15:00:00+00:00",
        )
        self.assertEqual(self.events[-1]["event_type"], "REOPEN")

    def test_invalid_transition_preserves_state(self) -> None:
        original_events: int = len(self.events)

        with self.assertRaises(ValueError):
            change_status_service(
                self.tickets,
                self.events,
                "T001",
                "resolved",
                now=self.now,
                save_func=self.save,
            )

        self.assertEqual(self.tickets[0]["status"], "open")
        self.assertEqual(len(self.events), original_events)

    def test_failed_save_preserves_state(self) -> None:
        self.save.side_effect = OSError("Disk failure")

        with self.assertRaises(OSError):
            assign_ticket_service(
                self.tickets,
                self.events,
                "T001",
                "Engineer A",
                now=self.now,
                save_func=self.save,
            )

        self.assertIsNone(self.tickets[0]["assigned_to"])
        self.assertEqual(len(self.events), 1)

    def test_cannot_start_unassigned_ticket(self) -> None:
        with self.assertRaises(ValueError):
            change_status_service(
                self.tickets,
                self.events,
                "T001",
                "in_progress",
                now=self.now,
                save_func=self.save,
            )

    def test_cannot_assign_resolved_ticket(self) -> None:
        assign_ticket_service(
            self.tickets,
            self.events,
            "T001",
            "Engineer A",
            now=self.now,
            save_func=self.save,
        )

        change_status_service(
            self.tickets,
            self.events,
            "T001",
            "in_progress",
            now=self.now + timedelta(minutes=5),
            save_func=self.save,
        )

        change_status_service(
            self.tickets,
            self.events,
            "T001",
            "resolved",
            now=self.now + timedelta(minutes=10),
            save_func=self.save,
        )

        with self.assertRaises(ValueError):
            assign_ticket_service(
                self.tickets,
                self.events,
                "T001",
                "Engineer B",
                now=self.now + timedelta(minutes=15),
                save_func=self.save,
            )


if __name__ == "__main__":
    unittest.main()