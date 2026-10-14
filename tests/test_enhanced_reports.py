"""Unit tests for CampusFlow Pro enhanced analytics."""

import unittest

from datetime import datetime, timezone

from campusflow.reports import generate_enhanced_report


class TestEnhancedReports(unittest.TestCase):

    def setUp(self):
        self.now = datetime(
            2026, 10, 14, 12, 0,
            tzinfo=timezone.utc,
        )

        self.tickets = [
            {
                "id": "T001",
                "priority": "critical",
                "status": "open",
                "assigned_to": "Moses",
                "created_at": "2026-10-14T08:00:00+00:00",
                "due_at": "2026-10-14T09:00:00+00:00",
            },
            {
                "id": "T002",
                "priority": "high",
                "status": "in_progress",
                "assigned_to": "Moses",
                "created_at": "2026-10-14T08:00:00+00:00",
                "due_at": "2026-10-14T12:00:00+00:00",
            },
            {
                "id": "T003",
                "priority": "medium",
                "status": "resolved",
                "assigned_to": "Ada",
                "created_at": "2026-10-13T08:00:00+00:00",
                "due_at": "2026-10-14T08:00:00+00:00",
            },
            {
                "id": "T004",
                "priority": "low",
                "status": "open",
                "assigned_to": None,
                "created_at": "2026-10-14T08:00:00+00:00",
                "due_at": "2026-10-16T08:00:00+00:00",
            },
        ]

        self.events = [
            {
                "event_id": "E001",
                "ticket_id": "T003",
                "event_type": "RESOLVE",
                "timestamp": "2026-10-13T12:00:00+00:00",
            }
        ]

    def test_overdue_total(self):
        report = generate_enhanced_report(
            self.tickets,
            self.events,
            self.now,
        )

        self.assertEqual(report["overdue_total"], 1)

    def test_overdue_by_priority(self):
        report = generate_enhanced_report(
            self.tickets,
            self.events,
            self.now,
        )

        self.assertEqual(
            report["overdue_by_priority"]["critical"],
            1,
        )

        self.assertEqual(
            report["overdue_by_priority"]["high"],
            0,
        )

    def test_exact_deadline_not_overdue(self):
        report = generate_enhanced_report(
            self.tickets,
            self.events,
            self.now,
        )

        self.assertEqual(report["overdue_total"], 1)

    def test_staff_workload(self):
        report = generate_enhanced_report(
            self.tickets,
            self.events,
            self.now,
        )

        self.assertEqual(
            report["staff_workload"]["Moses"],
            2,
        )

        self.assertNotIn(
            "Ada",
            report["staff_workload"],
        )

    def test_resolution_rate(self):
        report = generate_enhanced_report(
            self.tickets,
            self.events,
            self.now,
        )

        self.assertEqual(
            report["resolution_rate_percent"],
            25.0,
        )

    def test_average_resolution_time(self):
        report = generate_enhanced_report(
            self.tickets,
            self.events,
            self.now,
        )

        self.assertEqual(
            report["average_resolution_hours"],
            4.0,
        )

    def test_latest_resolution_event_used(self):
        self.events.append(
            {
                "event_id": "E002",
                "ticket_id": "T003",
                "event_type": "RESOLVE",
                "timestamp": "2026-10-13T14:00:00+00:00",
            }
        )

        report = generate_enhanced_report(
            self.tickets,
            self.events,
            self.now,
        )

        self.assertEqual(
            report["average_resolution_hours"],
            6.0,
        )

    def test_empty_data(self):
        report = generate_enhanced_report(
            [],
            [],
            self.now,
        )

        self.assertEqual(report["overdue_total"], 0)
        self.assertEqual(report["staff_workload"], {})
        self.assertEqual(
            report["resolution_rate_percent"],
            0.0,
        )
        self.assertEqual(
            report["average_resolution_hours"],
            0.0,
        )

    def test_invalid_now_rejected(self):
        naive_now = datetime(2026, 10, 14, 12, 0)

        with self.assertRaises(ValueError):
            generate_enhanced_report(
                self.tickets,
                self.events,
                naive_now,
            )

    def test_resolution_before_creation_rejected(self):
        self.events[0]["timestamp"] = (
            "2026-10-12T12:00:00+00:00"
        )

        with self.assertRaises(ValueError):
            generate_enhanced_report(
                self.tickets,
                self.events,
                self.now,
            )

    def test_missing_resolution_event(self):
        report = generate_enhanced_report(
            self.tickets,
            [],
            self.now,
        )

        self.assertEqual(
            report["average_resolution_hours"],
            0.0,
        )

    def test_inputs_not_modified(self):
        original_tickets = [
            ticket.copy()
            for ticket in self.tickets
        ]

        original_events = [
            event.copy()
            for event in self.events
        ]

        generate_enhanced_report(
            self.tickets,
            self.events,
            self.now,
        )

        self.assertEqual(
            self.tickets,
            original_tickets,
        )

        self.assertEqual(
            self.events,
            original_events,
        )


if __name__ == "__main__":
    unittest.main()