# CampusFlow — AI-Assisted Learning Log

**Project:** CampusFlow — Campus Helpdesk Ticket Management System  
**Programme:** Learn2Earn Python Engineering Sprint

This document records how AI assistance supported learning during CampusFlow development, how suggestions were evaluated, and how the resulting implementations were independently verified.

---

# Engineer A — John Ikwuobe

## Interaction 1 — Priority Calculation

**Problem:** Understanding how to implement multiple priority conditions in the correct order.

**My initial understanding:** I understood that `if`, `elif`, and `else` statements could make decisions based on conditions, but I needed to understand why the order of conditions matters when more than one rule could match.

**Prompt to AI:** How should I implement and test ordered priority conditions in Python?

**Useful AI guidance:** AI explained how conditional statements are evaluated in order and why the most specific condition should be checked before more general conditions.

**Independent verification:** I compared the proposed conditions with the official CampusFlow requirements and tested the different priority levels.

**Critical evaluation:** An earlier AI suggestion used 20 affected users as the threshold for critical priority. The assignment specified 10 affected users. I rejected the incorrect threshold and used the requirement instead.

**Verification result:** Automated tests confirmed the expected priority values, including the critical boundary at exactly 10 affected users.

**Decision:** Accepted the conditional logic approach but corrected the threshold to match the specification.

**Related files:** `tickets.py`, `tests/test_tickets.py`

**What I can now explain:** I can explain how Python evaluates conditions from top to bottom and why rule ordering is essential when conditions overlap.

---

## Interaction 2 — JSON Persistence

**Problem:** Understanding how to save Python ticket records and retrieve them after restarting an application.

**My initial understanding:** I understood that Python lists and dictionaries could hold ticket information while a program was running, but I needed to learn how to preserve that information after the program closed.

**Prompt to AI:** Explain the difference between `json.dump()` and `json.load()` using a small Python example.

**Useful AI guidance:** AI explained that `json.dump()` writes Python data to a JSON file, while `json.load()` reads JSON data and converts it back into Python objects.

**Independent verification:** I implemented `save_tickets()` and `load_tickets()` and used automated tests to verify that saved ticket records could be loaded correctly.

**Verification result:** The storage tests passed, including saving and loading tickets, handling missing files, detecting malformed JSON, and generating unique IDs after reloading saved data.

**Decision:** Accepted the JSON approach because it meets the project requirements without requiring an external database.

**Related files:** `storage.py`, `tests/test_storage.py`

**What I can now explain:** I can explain JSON serialization and deserialization, why file handling is important, and how persistent storage allows information to survive application restarts.

---

## Interaction 3 — Input Validation and Exception Handling

**Problem:** Understanding how to reject invalid ticket information without changing the existing ticket list.

**My initial understanding:** I understood how to collect input and append dictionaries to a list, but I needed to ensure invalid input was rejected before any new record was added.

**Prompt to AI:** Explain how `ValueError` and validation before list modification prevent invalid records.

**Useful AI guidance:** AI explained how to validate inputs before modifying application data and how raising `ValueError` allows the caller to handle invalid operations.

**Independent verification:** I tested zero, negative, text, decimal, and Boolean values for affected users. I also tested blank ticket titles and invalid categories.

**Verification result:** Automated tests confirmed that invalid inputs raised `ValueError` and left the ticket list unchanged.

**Decision:** Accepted the validation-before-modification approach and included explicit type checks because Boolean values are subclasses of integers in Python.

**Related files:** `tickets.py`, `tests/test_tickets.py`

**What I can now explain:** I can explain why input validation protects data integrity, when to raise `ValueError`, and why invalid operations should not modify application state.

---

# Engineer B — Idi Mohammed Mohammed

Engineer B should record three independently verified AI-assisted learning interactions relating to the workflow and reporting modules.

Each entry should include the original problem, the actual prompt used, the AI guidance received, independent verification, observed results, a critical evaluation, and the final decision.

## Interaction 1 — Ticket Assignment and Workflow

**Topic:** Implementing ticket assignment and controlling valid status transitions.

**Related files:** `campusflow/workflow.py`, `tests/test_workflow.py`

**To be completed by Engineer B:** Record the actual AI interaction and verification performed.

## Interaction 2 — Priority Queue Sorting

**Topic:** Sorting open tickets by priority and numeric ticket ID.

**Related files:** `campusflow/reports.py`, `tests/test_reports.py`

**To be completed by Engineer B:** Record the actual AI interaction and verification performed.

## Interaction 3 — Reporting and Testing

**Topic:** Generating accurate ticket summaries and verifying edge cases.

**Related files:** `campusflow/reports.py`, `tests/test_reports.py`

**To be completed by Engineer B:** Record the actual AI interaction and verification performed.

---

# Final Integration Verification

After merging both engineers' contributions, the integrated CampusFlow application was tested using:

`python -m pytest -q`

**Observed result:** 38 tests passed, 0 failed.

The complete application includes ticket creation, input validation, automatic priority calculation, JSON persistence, staff assignment, status transitions, reopening, priority queue sorting, reporting, and an interactive command-line interface.

## Learning Reflection

The CampusFlow project demonstrates that AI can support learning and debugging, but AI-generated suggestions must be checked against project requirements and verified through experiments and tests.

An important example was correcting the critical-priority threshold from 20 affected users to the required 10.

The project also reinforced the importance of modular programming, automated testing, error handling, Git collaboration, and careful integration.