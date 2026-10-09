# CampusFlow — Design Decisions

## 1. Project Overview

CampusFlow is a Python command-line helpdesk application developed for Learn2Earn to manage technical support requests.

The system supports ticket creation, priority calculation, staff assignment, ticket status management, priority queues, reporting, and JSON persistence.

## 2. Data Structure

Tickets are stored in a Python list containing dictionaries.

Each ticket has eight fields:

- `id`
- `title`
- `category`
- `urgency`
- `affected_users`
- `priority`
- `status`
- `assigned_to`

Ticket IDs use the format `T001`, `T002`, `T003`, etc.

The system generates the next ID using the highest existing ticket number, preventing duplicate IDs when saved tickets are reloaded.

## 3. Division of Responsibilities

**Engineer A — John Ikwuobe**

Responsible for ticket creation, input validation, priority calculation, unique ticket IDs, JSON persistence, automated tests, and CLI integration.

**Engineer B — Idi Mohammed Mohammed**

Responsible for staff assignment, ticket status transitions, ticket reopening, priority queue, reporting, and automated tests.

Both engineers contribute to integration, documentation, and collaborative development.

## 4. Function Contracts

### Ticket Management — `tickets.py`

- `create_ticket(tickets, title, category, urgency, affected_users)` validates input, creates a ticket, appends it to the list, and returns it.
- `calculate_priority(urgency, affected_users)` calculates and returns the appropriate priority.

### Workflow — `campusflow/workflow.py`

- `assign_ticket(tickets, ticket_id, staff_name)` assigns a staff member to an existing ticket and returns the updated ticket.
- `change_status(tickets, ticket_id, new_status)` validates the requested status transition and returns the updated ticket.

### Reporting — `campusflow/reports.py`

- `get_priority_queue(tickets)` returns open tickets sorted by priority and then numeric ticket ID.
- `generate_report(tickets)` returns total tickets and counts grouped by status and priority.

### Storage — `storage.py`

- `load_tickets()` loads saved tickets from JSON.
- `save_tickets(tickets)` saves the ticket list to JSON.

## 5. Validation and Error Handling

The application rejects invalid input before creating tickets.

Validation includes:

- Blank ticket titles.
- Unsupported ticket categories.
- Invalid urgency levels.
- Zero or negative affected-user counts.
- Text, decimal, or Boolean affected-user values.
- Empty staff names.
- Invalid ticket status transitions.

Invalid operations raise `ValueError`, allowing the CLI to display understandable error messages.

## 6. Priority Calculation

Priority rules are evaluated in the following order:

1. High urgency AND at least 10 affected users → `critical`.
2. High urgency OR at least 10 affected users → `high`.
3. Medium urgency OR at least 3 affected users → `medium`.
4. Otherwise → `low`.

The order is important because the first matching condition determines the priority.

## 7. Ticket Workflow

Tickets begin with the status `open`.

The normal workflow is:

`open → in_progress → resolved`

A ticket must be assigned to a staff member before moving to `in_progress`.

Resolved tickets cannot be reassigned until they are explicitly reopened.

Reopening changes the status from `resolved` to `open`.

Invalid transitions raise `ValueError`.

## 8. Priority Queue

The queue displays tickets whose status is `open`.

Tickets are sorted in this order:

1. Critical
2. High
3. Medium
4. Low

Tickets with equal priority are sorted by their numeric ticket IDs.

## 9. JSON Persistence

Ticket information is stored in `data/tickets.json`.

The system uses Python's built-in `json` module.

A missing storage file produces an empty ticket list.

Malformed JSON raises a clear error rather than silently discarding stored information.

## 10. Testing Strategy

The project uses Python's `unittest` framework, with tests also executed using `pytest`.

Tests cover ticket creation, input validation, priority calculation, boundary conditions, unique IDs, JSON persistence, workflow transitions, assignment, queue ordering, and reporting.

**Final integrated verification: 38 automated tests passed on the main branch.**

## 11. GitHub Collaboration

The team uses Git and GitHub for version control and collaboration.

The development process includes separate feature branches, pull requests, peer review, integration, automated testing, and merging into `main`.

The completed application was pushed to the GitHub repository:

https://github.com/successjohnny/campusflow

## 12. Final Integration Decision

The project retains separate modules for ticket management, workflow, reporting, and storage.

The root `main.py` integrates these modules into a single interactive command-line interface.

This modular structure makes the code easier to understand, test, maintain, and extend.

The integrated application passed all 38 automated tests after the final CLI changes.