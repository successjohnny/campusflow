# CampusFlow Pro — Campus Helpdesk Ticket Management System

CampusFlow Pro is a Python-based command-line application developed as part of the **Learn2Earn Python Engineering Sprint**.

The system helps manage campus technical support requests through ticket creation, automatic prioritization, staff assignment, ticket lifecycle management, Service Level Agreement (SLA) monitoring, audit logging, duplicate detection, reporting, and an interactive Engineering Knowledge Lab.

The project was developed collaboratively by **three engineers**:

- John Ikwuobe — Engineer A
- Idi Mohammed Mohammed — Engineer B
- Moses Ochekwu — Engineer C

**Repository:** https://github.com/successjohnny/campusflow

## Project Objectives

CampusFlow Pro aims to:

- Record campus technical support requests in a structured format.
- Calculate ticket priorities automatically.
- Validate inputs and prevent invalid records.
- Assign tickets to staff and track resolution.
- Monitor SLA deadlines and overdue tickets.
- Maintain an auditable history of ticket operations.
- Identify potentially duplicate unresolved tickets.
- Organize work through priority and SLA attention queues.
- Generate helpdesk reports and operational analytics.
- Preserve data using versioned JSON storage.
- Assess engineering understanding through the Knowledge Lab.
- Demonstrate teamwork, testing, and GitHub collaboration.

## Technologies Used

- **Python 3** — Application development.
- **JSON** — Ticket, audit, and quiz session persistence.
- **unittest** — Built-in automated testing framework.
- **pytest** — Test execution.
- **Git** — Version control.
- **GitHub** — Pull requests and collaboration.
- **Visual Studio Code** — Development environment.

The application uses Python's standard library for its runtime functionality. `pytest` is used for development testing.

## Key Features

### 1. Ticket Creation and Validation

Users can create support tickets with a title, category, urgency, and number of affected users.

Supported categories:

- Network
- Hardware
- Software
- Other

Supported urgency levels:

- low
- medium
- high

The system validates information before creating tickets and generates unique IDs such as `T001`, `T002`, and `T003`.

### 2. Automatic Priority Calculation

Priority is calculated using the following rules, evaluated in order:

| Condition | Priority |
|---|---|
| High urgency AND at least 10 affected users | critical |
| High urgency OR at least 10 affected users | high |
| Medium urgency OR at least 3 affected users | medium |
| Otherwise | low |

The first matching rule determines the ticket's priority.

### 3. Ticket Workflow Management

The normal ticket lifecycle is:

`open → in_progress → resolved`

A resolved ticket can be reopened:

`resolved → open`

Workflow rules include:

- Staff names must be valid.
- A ticket must be assigned before work begins.
- Invalid status transitions are rejected.
- Resolved tickets must be reopened before further active work.
- Reopening begins a new SLA cycle.

### 4. SLA Tracking and Escalation

CampusFlow Pro calculates ticket deadlines based on priority.

| Priority | SLA Duration |
|---|---|
| Critical | 60 minutes |
| High | 240 minutes |
| Medium | 1,440 minutes |
| Low | 2,880 minutes |

The system uses timezone-aware UTC timestamps.

An unresolved ticket is overdue when the current time is later than its SLA deadline.

Overdue escalation is designed to be idempotent: repeated checks do not create duplicate escalation events for the same ticket in the same SLA cycle.

### 5. Audit Event Recording

The system records significant ticket operations.

Supported events include:

- `CREATE`
- `ASSIGN`
- `START`
- `RESOLVE`
- `REOPEN`
- `ESCALATE`

Audit records provide a history of ticket activity and support accountability and troubleshooting.

### 6. Duplicate Ticket Detection

CampusFlow Pro checks for potentially duplicate unresolved tickets using normalized titles and categories.

When a possible duplicate is detected, the CLI asks the user whether to continue creating the ticket.

The system does not automatically delete or merge tickets.

### 7. Priority Queue

The original priority queue displays open tickets in this order:

1. Critical
2. High
3. Medium
4. Low

Tickets with equal priority are ordered by numeric ticket ID.

### 8. SLA Attention Queue

The SLA attention queue focuses on unresolved tickets in the `open` and `in_progress` states.

Tickets are ordered by:

1. Overdue status.
2. Earliest SLA deadline.
3. Numeric ticket ID.

This helps identify tickets requiring urgent operational attention.

### 9. Reporting and Analytics

CampusFlow Pro supports basic and enhanced reporting.

Basic reports include ticket counts by status and priority.

Enhanced reporting uses ticket and audit data to provide additional operational information, including SLA-related analysis.

### 10. JSON Persistence and Data Integrity

Application data is stored in:

`data/tickets.json`

The versioned storage structure is:

```json
{
  "schema_version": 2,
  "tickets": [],
  "events": []
}
```

Storage functionality includes:

- Loading saved data.
- Validating the expected schema.
- Detecting malformed JSON.
- Validating timestamps.
- Preserving ticket and audit records.
- Using atomic file replacement to reduce partial-write risks.

Runtime data files are excluded from Git tracking.

### 11. Engineering Knowledge Lab

The Engineering Knowledge Lab is accessible through **menu option 8**.

It contains ten multiple-choice questions covering:

- SLA concepts.
- Ticket priorities.
- Audit logging.
- Duplicate detection.
- Overdue tickets.
- Timestamps.
- SLA reopening cycles.
- Atomic JSON saving.
- SLA attention queues.
- Idempotent escalation.

The Knowledge Lab provides feedback, explanations, scores, and percentages.

Completed quiz sessions are saved separately under:

`data/knowledge_lab_sessions/`

Each session has a unique ID and records the participant, completion timestamp, answers, and result.

### 12. Interactive Command-Line Interface

The application presents the following main menu:

```text
===== CAMPUSFLOW PRO HELPDESK =====
1. Create Ticket
2. View All Tickets
3. View Ticket Details
4. Assign Ticket
5. Update Ticket Status
6. View Priority Queue
7. Generate Reports
8. Knowledge Lab
0. Exit
```

The CLI integrates the ticket management, workflow, reporting, audit, SLA, duplicate detection, and Knowledge Lab components.

## Project Structure

```text
campusflow/
├── main.py
├── tickets.py
├── storage.py
├── README.md
├── .gitignore
│
├── campusflow/
│   ├── __init__.py
│   ├── audit.py
│   ├── duplicates.py
│   ├── knowledge_lab.py
│   ├── reports.py
│   ├── sla.py
│   ├── ticket_service.py
│   ├── workflow.py
│   └── workflow_service.py
│
├── tests/
│   └── Automated test modules
│
├── docs/
│   ├── ai-learning-log.md
│   ├── design-decisions.md
│   └── learning-reflections.md
│
└── data/
    ├── tickets.json
    └── knowledge_lab_sessions/
```

The `data/` files and quiz sessions are generated during application use. They are not required to be present in a fresh clone.

## Installation and Setup

### Step 1 — Clone the Repository

```bash
git clone https://github.com/successjohnny/campusflow.git
cd campusflow
```

### Step 2 — Verify Python

```bash
python3 --version
```

Python 3 is required.

### Step 3 — Run the Application

```bash
python3 main.py
```

### Step 4 — Use the Menu

Choose a menu option to create tickets, view ticket information, assign staff, update statuses, view queues, generate reports, or take the Knowledge Lab.

Enter `0` to exit.

## Running Automated Tests

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install pytest:

```bash
python -m pip install pytest
```

Run the complete test suite:

```bash
python -m pytest -q
```

Alternatively, run tests using Python's built-in unittest discovery:

```bash
python -m unittest discover -s tests -v
```

### Verified Integrated Test Result

**147 tests passed, 0 failed.**

Verified after merging Pull Request #8.

**Verified main commit:** `ea0be81`

The test suite covers ticket creation, validation, priority rules, JSON persistence, SLA calculations, escalation, audit logging, duplicate detection, workflow operations, reporting, CLI integration, and the Engineering Knowledge Lab.

## Input Validation and Error Handling

CampusFlow Pro rejects invalid operations, including:

- Blank ticket titles.
- Unsupported categories.
- Invalid urgency values.
- Zero or negative affected-user counts.
- Invalid numeric types.
- Empty staff names.
- Invalid ticket IDs.
- Unsupported workflow transitions.
- Attempts to start work without an assignment.
- Invalid persisted data.

Rejected operations are designed to leave existing valid application data unchanged.

## Team Collaboration and Responsibilities

### Engineer A — John Ikwuobe

**Role:** Ticket Creation, Priority Calculation, Data Integrity, and Testing.

Contributions:

- Ticket creation and input validation.
- Automatic priority calculation.
- Unique ticket ID generation.
- JSON persistence and schema validation.
- Automated tests.
- Integration support.
- Technical documentation.

**GitHub:** https://github.com/successjohnny

### Engineer B — Idi Mohammed Mohammed

**Role:** Ticket Workflow and Reporting.

Contributions:

- Staff assignment.
- Ticket status transitions.
- Ticket reopening.
- Original priority queue.
- Helpdesk reporting.
- Workflow and reporting tests.
- Collaborative integration.

### Engineer C — Moses Ochekwu

**Role:** Audit, Duplicate Detection, SLA Analytics, CLI Integration, and Engineering Knowledge Lab.

Contributions:

- Audit event recording.
- Duplicate ticket detection.
- SLA attention queue and analytics.
- Command-line interface integration.
- Engineering Knowledge Lab.
- Related integration and testing contributions.

## GitHub Collaboration Workflow

The team used Git and GitHub to coordinate development.

The workflow included:

1. Creating feature branches.
2. Implementing assigned modules.
3. Writing automated tests.
4. Committing and pushing changes.
5. Opening pull requests.
6. Reviewing code.
7. Resolving integration issues.
8. Merging approved changes.
9. Running the complete test suite.

**Repository:** https://github.com/successjohnny/campusflow

## Design Decisions

The technical architecture, business rules, module responsibilities, persistence format, testing strategy, and collaboration decisions are documented in:

`docs/design-decisions.md`

## AI-Assisted Learning

AI tools supported the team's understanding of Python concepts, debugging, testing, and system design.

Learning evidence is documented in:

`docs/ai-learning-log.md`

The log includes three documented learning cycles for Engineer A.

Engineers B and C have sections reserved for their actual AI learning evidence, which must be completed before final submission if required by the assessment.

### Example of Critical AI Evaluation

During priority calculation, an AI suggestion used 20 affected users as the critical-priority threshold.

The project specification required 10 affected users.

Engineer A rejected the incorrect suggestion and verified the correct implementation through testing.

This illustrates why AI-generated suggestions must be checked against project requirements.

## Engineering Knowledge Lab Reflections

Individual quiz results and reflections are documented in:

`docs/learning-reflections.md`

### Recorded Result

**John Ikwuobe:** 10/10 — 100%

**Session ID:** `af86daa384474d0db855004bed6b3f6f`

The results and reflections for Idi Mohammed Mohammed and Moses Ochekwu are pending.

## Future Improvements

Potential future enhancements include:

- SQLite or PostgreSQL database integration.
- A FastAPI web interface.
- Staff authentication and role-based access.
- Automatic scheduled SLA monitoring.
- Email or in-app notifications.
- Advanced reporting dashboards.
- Multi-user access.
- Additional Knowledge Lab assessments.

These are future possibilities and are not claimed as implemented features.

## Project Status

**Core CampusFlow Pro implementation completed and integrated.**

The application includes ticket management, workflow operations, SLA monitoring, audit events, duplicate detection, reporting, and the Engineering Knowledge Lab.

The latest verified integrated test run completed with **147 passing tests** on main commit `ea0be81`.

Final submission documentation is being completed.

## Acknowledgement

Developed as a collaborative Python engineering project for the **Learn2Earn Python Engineering Sprint**.

**Contributors:**

- John Ikwuobe — Engineer A
- Idi Mohammed Mohammed — Engineer B
- Moses Ochekwu — Engineer C

## License

This project was created for educational purposes as part of the Learn2Earn Python Engineering Sprint.

No separate software license has been specified.