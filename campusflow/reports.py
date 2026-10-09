def get_priority_queue(tickets):

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3
    }

    open_tickets = [
        ticket for ticket in tickets
        if ticket["status"] == "open"
    ]

    sorted_tickets = sorted(
        open_tickets,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            int(ticket["id"][1:])
        )
    )

    return sorted_tickets


def generate_report(tickets):

    report = {
        "total": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
    }

    for ticket in tickets:

        status = ticket["status"]
        priority = ticket["priority"]

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1

    return report