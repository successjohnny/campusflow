"""Tests for CampusFlow Pro duplicate ticket detection."""

import unittest

from campusflow.duplicates import (
    normalize_title,
    detect_duplicates,
)


class TestDuplicateDetection(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Network Connection Failure",
                "category": "Network",
                "status": "open",
            },
            {
                "id": "T002",
                "title": "Printer Issue",
                "category": "Hardware",
                "status": "in_progress",
            },
            {
                "id": "T003",
                "title": "Software Installation",
                "category": "Software",
                "status": "resolved",
            },
        ]

    def test_normalize_title(self):
        result = normalize_title(
            "  NETWORK    Connection   Failure  "
        )

        self.assertEqual(
            result,
            "network connection failure",
        )

    def test_case_insensitive_duplicate(self):
        duplicates = detect_duplicates(
            self.tickets,
            "Network",
            "network connection failure",
        )

        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0]["id"], "T001")

    def test_repeated_whitespace_duplicate(self):
        duplicates = detect_duplicates(
            self.tickets,
            "Network",
            "Network    Connection    Failure",
        )

        self.assertEqual(len(duplicates), 1)

    def test_in_progress_ticket_is_duplicate(self):
        duplicates = detect_duplicates(
            self.tickets,
            "Hardware",
            "printer issue",
        )

        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0]["id"], "T002")

    def test_resolved_ticket_is_not_duplicate(self):
        duplicates = detect_duplicates(
            self.tickets,
            "Software",
            "Software Installation",
        )

        self.assertEqual(duplicates, [])

    def test_different_category_is_not_duplicate(self):
        duplicates = detect_duplicates(
            self.tickets,
            "Hardware",
            "Network Connection Failure",
        )

        self.assertEqual(duplicates, [])

    def test_invalid_title(self):
        with self.assertRaises(ValueError):
            detect_duplicates(
                self.tickets,
                "Network",
                "   ",
            )

    def test_multiple_duplicates(self):
        self.tickets.append(
            {
                "id": "T004",
                "title": "network connection failure",
                "category": "Network",
                "status": "in_progress",
            }
        )

        duplicates = detect_duplicates(
            self.tickets,
            "Network",
            "NETWORK CONNECTION FAILURE",
        )

        self.assertEqual(
            [ticket["id"] for ticket in duplicates],
            ["T001", "T004"],
        )

    def test_detection_does_not_modify_tickets(self):
        original = [
            ticket.copy()
            for ticket in self.tickets
        ]

        detect_duplicates(
            self.tickets,
            "Network",
            "Network Connection Failure",
        )

        self.assertEqual(self.tickets, original)


if __name__ == "__main__":
    unittest.main()