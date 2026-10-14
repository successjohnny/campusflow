# CampusFlow Pro — System Design and Technical Decisions

**Project:** CampusFlow Pro — Campus Helpdesk Ticket Management System
**Programme:** Learn2Earn Python Engineering Sprint
**Repository:** https://github.com/successjohnny/campusflow
**Implementation:** Python 3 — Command-Line Application
**Last Verified Main Commit:** `ea0be81`
**Automated Tests:** 147 passed, 0 failed

---

## 1. Project Overview

CampusFlow Pro is a Python-based campus helpdesk ticket management system developed to register, prioritize, assign, monitor, and resolve technical support requests.

The project extends the original CampusFlow application with advanced engineering features, including:

- Automatic ticket priority calculation.
- Ticket assignment and workflow management.
- Service Level Agreement (SLA) tracking.
- Overdue ticket escalation.
- Audit event recording.
- Duplicate ticket detection.
- Priority and SLA attention queues.
- Enhanced reporting and analytics.
- Versioned JSON persistence.
- An interactive Engineering Knowledge Lab.
- Automated testing and collaborative GitHub development.

The application follows a modular architecture that separates business logic, persistence, service coordination, and user interaction.

## 2. System Architecture

CampusFlow Pro is organized into three main layers.

### 2.1 User Interface Layer

**File:** `main.py`

Provides the interactive command-line interface through which users can create tickets, view ticket information, assign staff, update ticket status, access queues, generate reports, and launch the Engineering Knowledge Lab.

The CLI coordinates user input with the relevant service and business logic modules.

### 2.2 Business Logic and Service Layer

**Directory:** `campusflow/`

Contains modules responsible for workflow rules, SLA calculations, audit events, duplicate detection, reporting, and application services.

The service modules coordinate multi-step operations and separate the interactive CLI from the underlying business logic.

### 2.3 Persistence Layer

**File:** `storage.py`

Handles validation, loading, and saving of ticket and audit data using JSON.

Knowledge Lab sessions are stored separately from operational ticket records.

This separation makes the system easier to maintain, test, and extend.

## 3. Team Responsibilities and Contributions

CampusFlow Pro was developed collaboratively by three contributors.

### Engineer A — John Ikwuobe

**Primary responsibilities:**

- Ticket creation and input validation.
- Automatic ticket priority calculation.
- Unique ticket ID generation.
- JSON persistence and data integrity.
- Automated testing.
- Integration support and technical documentation.

**Relevant modules:**

- `tickets.py`
- `storage.py`
- `campusflow/ticket_service.py`
- Associated automated tests

### Engineer B — Idi Mohammed Mohammed

**Primary responsibilities:**

- Staff assignment.
- Ticket status transitions.
- Ticket reopening.
- Original priority queue.
- Ticket reporting.
- Automated testing and collaborative integration.

**Relevant modules:**

- `campusflow/workflow.py`
- `campusflow/workflow_service.py`
- `campusflow/reports.py`
- Associated automated tests

### Engineer C — Moses Ochekwu

**Primary responsibilities:**

- Audit event recording.
- Duplicate ticket detection.
- SLA attention queue and analytics.
- Command-line interface integration.
- Engineering Knowledge Lab development.

**Relevant modules:**

- `campusflow/audit.py`
- `campusflow/duplicates.py`
- `campusflow/reports.py`
- `campusflow/knowledge_lab.py`
- `main.py`
- Associated integration and automated tests

### 3.4 Collaborative Development

All three contributors participated in developing the integrated CampusFlow Pro application.

The project uses Git feature branches, GitHub pull requests, automated testing, and code review to support collaboration.

The responsibility assignments above describe each contributor's main areas of work; some modules involve contributions from more than one engineer.

## 4. Ticket Data Structure

Tickets are represented as Python dictionaries stored in a list.

Each ticket has a unique identifier using the format:

`T001`, `T002`, `T003`, and so on.

Core ticket information includes:

- Ticket ID.
- Title.
- Category.
- Urgency.
- Number of affected users.
- Calculated priority.
- Current status.
- Assigned staff member.

CampusFlow Pro also maintains information needed for SLA monitoring, including creation time, update time, deadline, and escalation cycle.

Ticket records are stored separately from audit events in the versioned JSON structure.

## 5. Ticket Creation and Priority Calculation

**Module:** `tickets.py`

The application uses two primary functions:

`calculate_priority(urgency, affected_users)`

Determines ticket priority based on urgency and the number of affected users.

`create_ticket(tickets, title, category, urgency, affected_users)`

Validates input, creates a ticket record, and adds it to the ticket collection.

### Priority Rules

The following rules are evaluated in order:

1. High urgency and at least 10 affected users → Critical.
2. High urgency or at least 10 affected users → High.
3. Medium urgency or at least 3 affected users → Medium.
4. All other valid combinations → Low.

The order is important because Python evaluates the conditions sequentially.

The most specific rule must be evaluated before more general rules.

## 6. Input Validation and Data Integrity

CampusFlow Pro validates user input before accepting ticket operations.

Validation includes:

- Rejecting blank ticket titles.
- Rejecting unsupported categories.
- Rejecting invalid urgency levels.
- Rejecting zero or negative affected-user counts.
- Rejecting invalid affected-user types.
- Rejecting invalid staff assignments.
- Rejecting unsupported ticket status transitions.
- Checking for potentially duplicate unresolved tickets.

Invalid operations should not partially modify valid application data.

This approach protects consistency and makes application behavior predictable.

## 7. SLA Management

**Module:** `campusflow/sla.py`

SLA functionality determines the time allowed for resolving tickets based on their priority.

### SLA Durations

| Priority | Duration |
|---|---|
| Critical | 60 minutes |
| High | 240 minutes |
| Medium | 1,440 minutes |
| Low | 2,880 minutes |

### Main Functions

`require_aware_datetime(value, name)`

Validates timezone-aware datetime values.

`calculate_due_at(priority, cycle_start)`

Calculates the ticket deadline from its priority and SLA cycle start.

`is_overdue(ticket, now)`

Determines whether an unresolved ticket has passed its SLA deadline.

`escalate_overdue(tickets, events, now, actor)`

Checks overdue tickets and coordinates escalation recording.

### SLA Design Decisions

- UTC-aware timestamps are used for consistent time calculations.
- A ticket is overdue only when the current time is strictly later than its deadline.
- Resolved tickets are excluded from active overdue monitoring.
- Reopening a ticket starts a new SLA cycle.
- Escalation does not automatically change the ticket's priority or status.

## 8. Audit Event Recording

**Module:** `campusflow/audit.py`

**Primary contributor:** Moses Ochekwu

Audit logging records significant ticket operations and provides a traceable history of changes.

### Supported Audit Events

- `CREATE` — A new ticket is created.
- `ASSIGN` — A ticket is assigned.
- `START` — Work begins on a ticket.
- `RESOLVE` — A ticket is resolved.
- `REOPEN` — A resolved ticket is reopened.
- `ESCALATE` — An overdue ticket is escalated.

### Main Functions

`record_event()`

Creates an audit event associated with a ticket operation.

`get_ticket_history(events, ticket_id)`

Retrieves the recorded events for a specific ticket.

Audit events contain identifying and contextual information, including the event ID, ticket ID, event type, actor, timestamp, previous status, new status, and additional details.

### Design Decision

The audit trail is append-only.

New actions generate new records rather than rewriting historical events.

This supports accountability, troubleshooting, and verification of ticket history.

## 9. Duplicate Ticket Detection

**Module:** `campusflow/duplicates.py`

**Primary contributor:** Moses Ochekwu

Duplicate detection identifies potentially repeated reports of the same unresolved issue.

### Main Functions

`normalize_title(title)`

Normalizes ticket titles to support consistent comparisons.

`detect_duplicates(tickets, category, title)`

Checks for unresolved tickets with matching normalized titles and categories.

### Design Decision

Duplicate detection provides a warning rather than automatically deleting or merging tickets.

The user can confirm whether to continue creating a potentially duplicate ticket.

This preserves user control while reducing unnecessary repeated records.

## 10. Ticket Workflow Management

**Modules:**

- `campusflow/workflow.py`
- `campusflow/workflow_service.py`

**Primary contributor:** Idi Mohammed Mohammed

The ticket workflow controls staff assignment and valid status transitions.

### Ticket Lifecycle

`open → in_progress → resolved`

A resolved ticket may be reopened:

`resolved → open`

### Workflow Rules

- Tickets begin in the open state.
- Staff assignment must satisfy validation requirements.
- Work cannot begin without a valid assignment.
- Invalid status transitions are rejected.
- Resolved tickets must be reopened before further active work.
- Reopening begins a new SLA cycle.

### Service Coordination

The workflow service coordinates ticket changes, audit event recording, and persistence.

This reduces the risk of saving an incomplete multi-step operation.

## 11. Ticket Creation Service

**Module:** `campusflow/ticket_service.py`

The `create_ticket_service()` function coordinates ticket creation with the additional requirements introduced in CampusFlow Pro.

The service layer provides a boundary between the basic ticket creation logic and the larger application workflow.

This improves modularity and supports independent automated testing.

## 12. JSON Persistence and Storage Validation

**Module:** `storage.py`

**Primary contributor:** John Ikwuobe

CampusFlow Pro uses JSON to store ticket records and audit events.

### JSON Schema Version 2

The saved data follows this structure:

```json
{
  "schema_version": 2,
  "tickets": [],
  "events": []
}
```

### Main Functions

`validate_timestamp(value)`

Validates stored timestamp values.

`validate_data(data)`

Checks the stored data structure and required information.

`load_data(file_path=DATA_FILE)`

Loads versioned application data.

`save_data(tickets, events, file_path=DATA_FILE)`

Saves ticket and audit data.

Compatibility functions `load_tickets()` and `save_tickets()` are also present.

### Design Decisions

**Versioned schema:** Allows the application to recognize the expected storage format.

**Validation before saving:** Reduces the risk of writing inconsistent data.

**Atomic file replacement:** Uses a temporary file and replacement operation to reduce the risk of partially written files.

**Clear error handling:** Invalid or malformed stored data should not be silently treated as valid empty data.

**Separate audit records:** Keeps ticket state and operational history distinct.

## 13. Original Priority Queue

**Module:** `campusflow/reports.py`

**Primary contributor:** Idi Mohammed Mohammed

The `get_priority_queue(tickets)` function displays open tickets ordered by priority.

### Queue Ordering

1. Critical.
2. High.
3. Medium.
4. Low.

Tickets with the same priority are ordered by their numeric ticket IDs.

This preserves the original CampusFlow queue behavior.

## 14. SLA Attention Queue

**Module:** `campusflow/reports.py`

**Primary contributor:** Moses Ochekwu

The `get_sla_attention_queue(tickets, now)` function provides an operational view of unresolved tickets requiring attention.

The queue includes tickets in the open and in-progress states.

### Ordering Rules

1. Overdue tickets first.
2. Earlier SLA deadlines before later deadlines.
3. Numeric ticket IDs to break ties.

### Design Decision

The SLA attention queue is maintained separately from the original priority queue.

This distinction allows staff to monitor deadline urgency without changing the original priority ranking rules.

## 15. Reporting and Analytics

**Module:** `campusflow/reports.py`

**Contributors:** Idi Mohammed Mohammed and Moses Ochekwu

### Basic Reporting

`generate_report(tickets)`

Produces ticket statistics, including totals and status or priority distributions.

### Enhanced Reporting

`generate_enhanced_report(tickets, events, now)`

Provides additional operational analysis using ticket records, audit events, and the current time.

The reporting system supports monitoring of unresolved work, SLA performance, and overall helpdesk activity.

### Design Decision

Reporting calculations are separated from the interactive CLI.

This allows analytics to be tested independently and reused by other interfaces in the future.

## 16. Command-Line Interface Integration

**File:** `main.py`

**Primary contributor:** Moses Ochekwu

The CLI brings together the project's ticket management, workflow, reporting, and learning components.

### Main Functions

- `show_menu()`
- `create_ticket_menu()`
- `list_tickets()`
- `view_ticket()`
- `assign_ticket_menu()`
- `update_status_menu()`
- `priority_queue_menu()`
- `reports_menu()`
- `knowledge_lab_menu()`
- `main()`

The CLI collects user input, calls the relevant modules, and presents results to users.

### Design Decision

The CLI acts as the user-facing coordination layer rather than containing all business logic directly.

This improves readability and maintainability.

## 17. Engineering Knowledge Lab

**Module:** `campusflow/knowledge_lab.py`

**Primary contributor:** Moses Ochekwu

The Engineering Knowledge Lab provides an interactive assessment of concepts used in CampusFlow Pro.

It is accessible through menu option 8.

### Features

- Ten fixed multiple-choice questions.
- Answer validation.
- Explanations after each answer.
- Score and percentage calculation.
- Participant identification.
- Quiz replay.
- Separate JSON session records.

### Main Functions

`check_answer(question, answer)`

Checks whether an answer is correct.

`calculate_score(questions, answers)`

Calculates the quiz result.

`save_quiz_session()`

Saves a completed quiz attempt.

`run_quiz()`

Runs the interactive assessment.

### Session Records

Each saved session includes:

- Unique session ID.
- Participant name.
- UTC completion timestamp.
- Submitted answers.
- Number of correct answers.
- Total questions.
- Percentage score.

### Design Decision

Knowledge Lab results are stored separately from ticket data.

This allows learning activities to be recorded without affecting operational helpdesk records.

## 18. Automated Testing Strategy

CampusFlow Pro uses automated tests to verify functionality and protect existing features during development.

The project uses Python's `unittest` framework and executes tests using `pytest`.

### Testing Coverage

Tests cover:

- Ticket creation and input validation.
- Priority calculation.
- Ticket ID generation.
- JSON storage and validation.
- SLA deadline calculation.
- Overdue ticket detection.
- Escalation behavior.
- Audit event recording.
- Duplicate detection.
- Assignment and status transitions.
- Ticket reopening.
- Priority queues.
- Enhanced reporting.
- CLI integration.
- Knowledge Lab questions and session persistence.

### Final Verified Test Result

Command:

`python -m pytest -q`

**Result: 147 passed, 0 failed.**

**Verified main commit:** `ea0be81`

This result was confirmed after merging Pull Request #8.

## 19. Git and GitHub Collaboration

**Repository:** https://github.com/successjohnny/campusflow

The team used Git and GitHub for collaborative development.

### Collaboration Process

1. Create feature branches.
2. Implement assigned functionality.
3. Write and execute automated tests.
4. Push feature branches to GitHub.
5. Open pull requests.
6. Review proposed changes.
7. Merge approved pull requests.
8. Verify the integrated main branch.

### Integrated Features

Merged pull requests include work on:

- SLA management.
- Data integrity.
- Audit logging and queue improvements.
- CLI Knowledge Lab integration.
- Final CLI integration.
- Knowledge Lab completion and session persistence.

The final documentation will also record the team's AI learning evidence, individual Knowledge Lab results, and project reflections.

## 20. Key Technical Decisions

| Decision | Reason |
|---|---|
| Modular architecture | Separates responsibilities and supports independent testing |
| Python CLI | Provides an accessible interface without external web infrastructure |
| Automatic priority calculation | Applies consistent urgency rules |
| UTC-aware timestamps | Supports reliable SLA comparisons |
| SLA cycle tracking | Allows reopened tickets to receive new deadlines |
| Append-only audit events | Preserves ticket history and accountability |
| Duplicate detection | Reduces repeated reports without automatically deleting tickets |
| Versioned JSON storage | Makes persistence format explicit |
| Atomic file replacement | Reduces partial-write risks |
| Separate SLA attention queue | Prioritizes deadline-sensitive unresolved work |
| Service modules | Coordinate multi-step operations |
| Automated tests | Protect functionality during integration |
| Separate Knowledge Lab sessions | Preserves individual assessment results |
| GitHub pull requests | Supports collaboration and peer review |

## 21. Challenges and Lessons Learned

The project presented several important engineering challenges.

### Managing Multiple Business Rules

Priority calculation, SLA deadlines, workflow transitions, and duplicate detection required careful interpretation of the project requirements.

The team addressed these challenges by separating rules into dedicated functions and testing important boundary conditions.

### Maintaining Data Consistency

Ticket operations sometimes require changes to both ticket records and audit events.

Service coordination, validation, and safe persistence help prevent inconsistent state.

### Integrating Independent Contributions

Different engineers worked on related modules.

Git branches, pull requests, code review, and automated testing helped combine the contributions into a working application.

### Evaluating AI Assistance

AI assistance supported learning and development, but suggestions required independent verification.

One documented example involved rejecting an incorrect critical-priority threshold and following the official project specification instead.

### Learning Through Testing

Automated tests helped identify compatibility problems when the Knowledge Lab expanded from five questions to ten.

Updating the tests to match the revised requirements resulted in a verified suite of 147 passing tests.

## 22. Future Improvements

Possible future enhancements include:

- Database-backed persistence for larger workloads.
- Authentication and role-based access.
- A web-based dashboard.
- Automatic scheduled SLA monitoring.
- Notifications for overdue tickets.
- More detailed reporting visualizations.
- Additional Knowledge Lab learning activities.
- Deployment for multiple concurrent users.

These are potential improvements, not features claimed to be implemented in the current version.

## 23. Conclusion

CampusFlow Pro demonstrates practical Python software engineering through modular architecture, ticket management, workflow validation, SLA monitoring, audit logging, duplicate detection, JSON persistence, analytics, automated testing, and collaborative development.

The project combines the contributions of:

- **John Ikwuobe** — Ticket creation, priority calculation, validation, persistence, and testing.
- **Idi Mohammed Mohammed** — Workflow management, assignment, reopening, priority queue, and reporting.
- **Moses Ochekwu** — Audit event recording, duplicate detection, SLA attention queue and analytics, CLI integration, and Engineering Knowledge Lab.

The integrated project was verified with **147 passing automated tests** on merged main commit `ea0be81`.

CampusFlow Pro provides a practical foundation for further software engineering development and demonstrates the team's ability to build, test, integrate, and document a multi-module Python application.