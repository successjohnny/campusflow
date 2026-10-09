# CampusFlow — Campus Helpdesk Ticket Management System

CampusFlow is a Python-based command-line application developed to help Learn2Earn manage campus technical support requests efficiently.

The system allows users to create support tickets, calculate priorities automatically, assign staff members, manage ticket resolution, view priority queues, and generate helpdesk reports.

CampusFlow was developed collaboratively by two engineers as part of the **Learn2Earn Python Engineering Sprint**.

## Project Objectives

The objectives of CampusFlow are to:

- Provide a structured system for recording campus technical support issues.
- Automatically calculate ticket priority based on urgency and affected users.
- Prevent invalid ticket information from entering the system.
- Support staff assignment and ticket resolution tracking.
- Organize open tickets according to priority.
- Generate accurate helpdesk reports.
- Preserve ticket information using JSON storage.
- Demonstrate collaborative software development using Git and GitHub.

## Technologies Used

- **Python 3** — Core programming language.
- **JSON** — Persistent ticket storage.
- **unittest** — Automated testing framework.
- **pytest** — Additional test execution tool.
- **Git** — Version control.
- **GitHub** — Collaboration, pull requests, and code reviews.
- **Visual Studio Code** — Development environment.

The application itself uses Python's standard library and does not require third-party runtime dependencies.

## Key Features

### 1. Ticket Creation and Validation — Implemented

Each support ticket contains eight fields:

- `id`
- `title`
- `category`
- `urgency`
- `affected_users`
- `priority`
- `status`
- `assigned_to`

Supported categories are `Network`, `Hardware`, `Software`, and `Other`.

Supported urgency levels are `low`, `medium`, and `high`.

The system validates ticket information before creating a record.

### 2. Automatic Priority Calculation — Implemented

Ticket priority is calculated using the following rules, evaluated in order:

| Condition | Priority |
|---|---|
| High urgency AND at least 10 affected users | critical |
| High urgency OR at least 10 affected users | high |
| Medium urgency OR at least 3 affected users | medium |
| Otherwise | low |

The first matching condition determines the ticket priority.

### 3. Unique Ticket Identification — Implemented

Tickets receive unique IDs such as `T001`, `T002`, and `T003`.

New IDs are generated using the highest existing ticket number, helping preserve uniqueness after saved tickets are reloaded.

### 4. JSON Data Persistence — Implemented

Ticket records are saved to:

`data/tickets.json`

The system:

- Saves tickets in JSON format.
- Reloads saved tickets when the application starts.
- Uses an empty ticket list if the storage file does not exist.
- Detects malformed JSON and reports an error.
- Preserves ticket information across application restarts.

The runtime JSON file is excluded from Git tracking.

### 5. Staff Assignment — Implemented

Users can assign tickets to staff members.

The application rejects empty staff names and invalid ticket IDs.

Resolved tickets cannot be reassigned until they have been reopened.

### 6. Ticket Status Management — Implemented

The normal ticket workflow is:

`open → in_progress → resolved`

A ticket must be assigned before moving to `in_progress`.

Resolved tickets can be explicitly reopened by changing their status to `open`.

Invalid status transitions are rejected.

### 7. Priority Work Queue — Implemented

The priority queue displays open tickets sorted in the following order:

1. Critical
2. High
3. Medium
4. Low

Tickets with equal priority are ordered by their numeric ticket IDs.

### 8. Helpdesk Reports — Implemented

CampusFlow generates reports containing:

- Total number of tickets.
- Ticket counts by status.
- Ticket counts by priority.

The reporting system also handles an empty ticket list.

### 9. Interactive Command-Line Interface — Implemented

The application provides the following menu:

```text
===== CAMPUSFLOW HELPDESK =====
1. Create Ticket
2. View All Tickets
3. View Ticket Details
4. Assign Ticket
5. Update Ticket Status
6. View Priority Queue
7. Generate Reports
0. Exit
```

The CLI connects the ticket management, workflow, reporting, and storage modules.

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
├── storage.py
├── README.md
├── .gitignore
│
├── campusflow/
│   ├── __init__.py
│   ├── workflow.py
│   └── reports.py
│
├── tests/
│   ├── test_tickets.py
│   ├── test_storage.py
│   ├── test_workflow.py
│   └── test_reports.py
│
├── docs/
│   ├── design-decisions.md
│   └── ai-learning-log.md
│
└── data/
    └── tickets.json
```

The `data/tickets.json` file is generated during application use and is not committed to GitHub.

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

Select the required option to create tickets, view tickets, assign staff, update statuses, display the priority queue, or generate reports.

Enter `0` to exit.

## Running Automated Tests

CampusFlow includes automated tests written using Python's built-in `unittest` framework.

Run the test suite using:

```bash
python3 -m unittest discover -s tests -v
```

Alternatively, install pytest in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest
python -m pytest -q
```

### Verified Integrated Test Results

**38 tests passed, 0 failed.**

The integrated test suite was successfully executed after merging both engineers' contributions and updating the command-line interface.

Test coverage includes:

- Ticket creation and validation.
- Priority calculation and boundary conditions.
- Unique ticket IDs.
- Category and urgency normalization.
- JSON saving and loading.
- Missing and corrupted JSON files.
- Staff assignment.
- Ticket status transitions and reopening.
- Priority queue ordering.
- Helpdesk report generation.

## Input Validation and Error Handling

CampusFlow rejects invalid operations, including:

- Blank ticket titles.
- Unsupported categories.
- Invalid urgency values.
- Zero or negative affected-user counts.
- Text, decimal, or Boolean affected-user values.
- Empty staff names.
- Invalid ticket IDs for workflow operations.
- Invalid ticket status transitions.
- Attempts to begin work without an assigned staff member.

The application raises `ValueError` for invalid operations and displays understandable messages through the CLI.

## Team Collaboration and Responsibilities

### Engineer A — John Ikwuobe

**Role: Ticket Management, Priority Calculation, Persistence, and CLI Integration**

Responsibilities:

- Implement ticket creation.
- Validate user input.
- Calculate ticket priorities.
- Generate unique ticket IDs.
- Implement JSON persistence.
- Write automated tests.
- Integrate the CLI with workflow and reporting modules.
- Participate in testing, documentation, and code reviews.

GitHub: https://github.com/successjohnny

### Engineer B — Idi Mohammed Mohammed

**Role: Ticket Workflow and Reporting**

Responsibilities:

- Implement staff assignment.
- Manage ticket status transitions.
- Support ticket reopening.
- Develop the priority work queue.
- Generate helpdesk reports.
- Write automated workflow and reporting tests.
- Participate in integration, documentation, and code reviews.

## GitHub Collaboration Workflow

The team used Git and GitHub to coordinate development.

The workflow included:

1. Creating separate feature branches.
2. Implementing assigned modules.
3. Writing automated tests.
4. Committing and pushing changes.
5. Creating pull requests.
6. Reviewing each other's code.
7. Resolving integration conflicts.
8. Merging the contributions.
9. Running the complete test suite.
10. Publishing the integrated project on `main`.

### Repository

https://github.com/successjohnny/campusflow

## Design Decisions

The project's architecture and function contracts are documented in:

`docs/design-decisions.md`

The document covers ticket structures, validation rules, priority calculations, workflow restrictions, JSON persistence, testing, and collaboration decisions.

## AI-Assisted Learning

AI tools were used to support learning, debugging, and understanding Python concepts.

Learning topics included:

- Conditional logic and priority calculation.
- JSON serialization and deserialization.
- Exception handling.
- Input validation and data integrity.
- Unit testing and debugging.

AI suggestions were evaluated against the assignment requirements and verified through code inspection, experiments, and automated tests.

The learning evidence is documented in:

`docs/ai-learning-log.md`

### Example of Critical AI Evaluation

During priority calculation development, an earlier AI suggestion used 20 affected users as the critical-priority threshold.

After checking the project requirements, Engineer A identified that the correct threshold was 10 affected users.

The implementation was corrected and verified using automated tests.

This demonstrated the importance of independently verifying AI-generated suggestions.

## Future Improvements

Possible future enhancements include:

- SQLite or PostgreSQL database integration.
- A FastAPI web interface.
- Staff authentication and role-based access.
- Ticket search and filtering.
- Ticket activity history.
- Email notifications.
- Dashboard analytics.

## Project Status

**Core implementation and CLI integration completed.**

Both engineers' modules have been integrated into the application.

All 38 automated tests passed during final integration testing.

The completed code has been pushed to the GitHub `main` branch.

## Acknowledgement

Developed as a collaborative Python engineering project for the **Learn2Earn Python Engineering Sprint**.

**Contributors:**

- John Ikwuobe — Engineer A
- Idi Mohammed Mohammed — Engineer B

## License

This project was created for educational purposes as part of the Learn2Earn Python Engineering Sprint. No separate software license has been specified.