import unittest

from campusflow.reports import get_priority_queue, generate_report


class TestReports(unittest.TestCase):

    def setUp(self):

        self.tickets = [
            {
                "id": "T001",
                "priority": "low",
                "status": "open"
            },
            {
                "id": "T002",
                "priority": "critical",
                "status": "open"
            },
            {
                "id": "T003",
                "priority": "high",
                "status": "open"
            },
            {
                "id": "T004",
                "priority": "critical",
                "status": "open"
            },
            {
                "id": "T005",
                "priority": "medium",
                "status": "resolved"
            }
        ]

    def test_priority_queue_order(self):

        result = get_priority_queue(self.tickets)

        ids = [ticket["id"] for ticket in result]

        self.assertEqual(
            ids,
            ["T002", "T004", "T003", "T001"]
        )

    def test_resolved_ticket_excluded(self):

        result = get_priority_queue(self.tickets)

        ids = [ticket["id"] for ticket in result]

        self.assertNotIn("T005", ids)

    def test_total_tickets(self):

        result = generate_report(self.tickets)

        self.assertEqual(result["total"], 5)

    def test_status_counts(self):

        result = generate_report(self.tickets)

        self.assertEqual(result["by_status"]["open"], 4)
        self.assertEqual(result["by_status"]["resolved"], 1)

    def test_priority_counts(self):

        result = generate_report(self.tickets)

        self.assertEqual(result["by_priority"]["critical"], 2)
        self.assertEqual(result["by_priority"]["high"], 1)
        self.assertEqual(result["by_priority"]["medium"], 1)
        self.assertEqual(result["by_priority"]["low"], 1)

    def test_empty_report(self):

        result = generate_report([])

        self.assertEqual(result["total"], 0)
        self.assertEqual(result["by_status"]["open"], 0)
        self.assertEqual(result["by_priority"]["critical"], 0)

    def test_empty_queue(self):

        result = get_priority_queue([])

        self.assertEqual(result, [])

    def test_numeric_ticket_id_order(self):

        tickets = [
            {"id": "T010", "priority": "high", "status": "open"},
            {"id": "T002", "priority": "high", "status": "open"}
        ]

        result = get_priority_queue(tickets)

        ids = [ticket["id"] for ticket in result]

        self.assertEqual(ids, ["T002", "T010"])


if __name__ == "__main__":
    unittest.main()