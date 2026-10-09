# CampusFlow — Campus Helpdesk Ticket Management System

CampusFlow is a Python-based command-line application developed to help Learn2Earn manage technical support requests efficiently.

The system allows users to create support tickets, calculate priorities automatically, manage staff assignments, track ticket resolution, and generate helpdesk reports.

CampusFlow is developed collaboratively by two engineers as part of the **Learn2Earn Python Engineering Sprint**.

## Project Objectives

The objectives of CampusFlow are to:

- Provide a structured system for recording campus technical support issues.
- Automatically calculate ticket priority based on urgency and the number of affected users.
- Prevent invalid ticket information from entering the system.
- Support staff assignment and ticket resolution tracking.
- Organize unresolved tickets according to priority.
- Generate accurate helpdesk reports.
- Preserve ticket information using JSON storage.
- Demonstrate collaborative software development using Git and GitHub.

## Technologies Used

- **Python 3** — Core programming language.
- **JSON** — Persistent ticket storage.
- **unittest** — Automated testing.
- **Git** — Version control.
- **GitHub** — Team collaboration, pull requests, and code reviews.
- **Visual Studio Code** — Development environment.

The current implementation uses Python's standard library and does not require third-party dependencies.

## Key Features

### 1. Ticket Creation and Validation — Implemented

Users can create helpdesk tickets containing:

- Unique ticket ID.
- Ticket title.
- Category.
- Urgency level.
- Number of affected users.
- Calculated priority.
- Ticket status.
- Assigned staff member.

Supported categories are `Network`, `Hardware`, `Software`, and `Other`.

Supported urgency levels are `low`, `medium`, and `high`.

The system validates inputs before creating a ticket.

### 2. Automatic Priority Calculation — Implemented

CampusFlow automatically calculates priority using the following rules, evaluated in order:

| Condition | Priority |
|---|---|
| High urgency AND at least 10 affected users | Critical |
| High urgency OR at least 10 affected users | High |
| Medium urgency OR at least 3 affected users | Medium |
| Otherwise | Low |

### 3. Unique Ticket Identification — Implemented

Each ticket receives a unique identifier such as:

- `T001`
- `T002`
- `T003`

Ticket IDs remain unique when previously saved tickets are reloaded.

### 4. JSON Data Persistence — Implemented

CampusFlow stores tickets in:

`data/tickets.json`

The system:

- Saves ticket records in JSON format.
- Reloads existing records.
- Starts with an empty ticket list when the storage file is missing.
- Detects malformed JSON.
- Preserves ticket IDs across application restarts.

The runtime JSON file is excluded from Git tracking.

### 5. Staff Assignment — Under Development

This feature will allow users to assign tickets to staff members and reject invalid assignment requests.

### 6. Ticket Status Management — Under Development

The planned workflow is:

`open → in_progress → resolved`

Tickets must be assigned before progressing. Resolved tickets require explicit reopening before further modification.

### 7. Priority Work Queue — Under Development

The work queue will display unresolved tickets ordered by priority:

1. Critical
2. High
3. Medium
4. Low

Tickets with equal priority will be ordered by ticket ID.

### 8. Helpdesk Reports — Under Development

Reports will summarize:

- Total tickets.
- Tickets by status.
- Tickets by priority.

The reporting feature will also handle an empty ticket list.

### 9. Interactive Command-Line Interface — Partially Implemented

The application provides a command-line menu for managing tickets.

The final integrated menu is planned to support ticket creation, listing, details, assignment, status changes, reopening, work queue viewing, and reporting.

## Example Ticket Record

```python
{
    "id": "T001",
    "title": "Campus Wi-Fi is down",
    "category": "Network",
    "urgency": "high",
    "affected_users": 15,
    "priority": "critical",
    "status": "open",
    "assigned_to": None
}
```

## Project Structure

```text
campusflow/
│
├── main.py
├── tickets.py
├── workflow.py
├── reports.py
├── storage.py
├── README.md
├── .gitignore
│
├── tests/
│   ├── test_tickets.py
│   ├── test_storage.py
│   └── ... additional tests
│
├── docs/
│   ├── design-decisions.md
│   └── ai-learning-log.md
│
└── data/
    └── tickets.json
```

Some modules are still being developed or integrated. The `data/tickets.json` file is created during application use and is not committed to GitHub.

## Installation and Setup

### Step 1 — Clone the Repository

```bash
git clone https://github.com/successjohnny/campusflow.git
cd campusflow
```

### Step 2 — Check Python Installation

```bash
python3 --version
```

Python 3 is required.

### Step 3 — Run the Application

```bash
python3 main.py
```

### Step 4 — Follow the Menu

Select the available options to create or view tickets.

Additional options will become available after the final integration.

## Running Automated Tests

CampusFlow uses Python's built-in `unittest` framework.

Run all tests from the project root:

```bash
python3 -m unittest discover -s tests -v
```

### Current Verified Test Results

**John Ikwuobe — Engineer A**

- Automated tests executed: 20
- Tests passed: 20
- Test failures: 0
- Result: SUCCESS

Verified test areas include:

- Ticket creation.
- Input validation.
- Priority calculation.
- Priority boundary conditions.
- Category and urgency normalization.
- Unique ticket IDs.
- JSON saving and loading.
- Missing JSON file handling.
- Corrupted JSON detection.
- Unique IDs after reloading saved data.

These results were obtained on the `feature/tickets` branch before final integration.

The full test suite will be executed again after both engineers' contributions are merged.

## Input Validation and Error Handling

CampusFlow rejects invalid ticket information, including:

- Blank ticket titles.
- Unsupported categories.
- Invalid urgency values.
- Zero or negative affected-user counts.
- Text instead of an integer.
- Decimal affected-user values.
- Boolean affected-user values.

The system raises `ValueError` when invalid input is detected.

Validation is performed before adding tickets to the list, preventing invalid records from modifying application data.

## Team Collaboration and Responsibilities

CampusFlow is developed by two engineers using separate GitHub feature branches.

### John Ikwuobe — Engineer A

**Role: Ticket Management, Priority Calculation, and Data Persistence**

Responsibilities:

- Implement ticket creation.
- Validate user input.
- Calculate ticket priorities.
- Generate unique ticket IDs.
- Implement JSON persistence.
- Develop automated unit tests.
- Contribute to command-line integration.
- Participate in documentation, testing, and code reviews.

**Verified contribution:** 20 automated tests passed successfully.

**GitHub:** https://github.com/successjohnny

### Engineer B — Workflow and Reporting

**Role: Ticket Workflow, Staff Assignment, and Reporting**

Responsibilities:

- Implement staff assignment.
- Manage ticket status transitions.
- Support ticket reopening.
- Develop the priority work queue.
- Generate ticket summary reports.
- Write automated workflow and reporting tests.
- Participate in integration, documentation, and peer reviews.

Both engineers collaborate to ensure the completed application satisfies the project requirements.

## GitHub Collaboration Workflow

The team follows this development process:

1. Create separate feature branches.
2. Implement assigned application features.
3. Write and execute automated tests.
4. Commit changes with descriptive messages.
5. Push changes to GitHub.
6. Create pull requests.
7. Review each other's code and provide substantive feedback.
8. Resolve issues identified during review.
9. Approve and merge reviewed pull requests.
10. Run the integrated test suite on the `main` branch.

### Engineer A Branch

`feature/tickets`

### Repository

https://github.com/successjohnny/campusflow

## Design Decisions

The project documents agreed architectural decisions and function contracts in:

`docs/design-decisions.md`

The design covers ticket data structures, validation rules, function interfaces, persistence, testing, and collaboration.

## AI-Assisted Learning

AI tools were used as learning aids to explore Python concepts and evaluate possible implementations.

The engineers independently verify AI-generated explanations and suggestions through experiments, code inspection, and automated testing.

Learning topics include:

- Conditional logic and priority calculation.
- JSON serialization and deserialization.
- Python exception handling.
- Input validation and data integrity.
- Unit testing and debugging.

The learning evidence is recorded in:

`docs/ai-learning-log.md`

### Example of Critical AI Evaluation

During priority calculation development, an earlier AI suggestion used 20 affected users as the critical-priority threshold.

After comparing this suggestion with the official project requirements, John Ikwuobe identified that the correct threshold was 10 affected users.

The implementation was corrected and verified using automated tests.

This demonstrates the importance of checking AI suggestions against authoritative project requirements.

## Future Improvements

Potential future enhancements include:

- SQLite or PostgreSQL database integration.
- A web interface using FastAPI.
- Staff authentication and role-based access.
- Ticket search and filtering.
- Ticket activity history.
- Email notifications.
- Dashboard analytics.

## Project Status

**Development and integration in progress.**

John Ikwuobe's ticket creation, validation, priority calculation, and JSON persistence modules have been implemented and tested successfully.

Workflow, reporting, and complete CLI integration are pending completion and verification.

## Acknowledgement

Developed as a collaborative Python engineering project for the **Learn2Earn Python Engineering Sprint**.

**Contributors:**
- John Ikwuobe — Engineer A
- Idi Mohammed Mohammed — Engineer B

## License

This project was created for educational purposes as part of the Learn2Earn Python Engineering Sprint. No separate software license has been specified.