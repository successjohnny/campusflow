# CampusFlow Pro — AI-Assisted Learning Log

**Project:** CampusFlow Pro — Campus Helpdesk Ticket Management System

**Programme:** Learn2Earn Python Engineering Sprint

**Repository:** https://github.com/successjohnny/campusflow

**Contributors:**
- Engineer A — John Ikwuobe
- Engineer B — Idi Mohammed Mohammed
- Engineer C — Moses Ochekwu

**Latest verified main commit:** `ea0be81`

**Automated test result:** 147 passed, 0 failed

---

## 1. Purpose of This Learning Log

This document records how AI assistance supported learning during the development of CampusFlow Pro.

The purpose is to demonstrate that AI was used as a learning and problem-solving tool rather than as a substitute for engineering judgment.

Each documented learning cycle should identify:

1. The engineering problem.
2. The engineer's initial understanding.
3. The actual question or prompt submitted to AI.
4. The explanation or guidance received.
5. How the engineer independently verified the guidance.
6. The observed results.
7. Any AI suggestion that was rejected or modified.
8. The final engineering decision.
9. What the engineer learned.

The team used project requirements, source-code inspection, experiments, automated tests, and GitHub reviews to evaluate proposed solutions.

**Evidence status:** Engineer A's three learning cycles are documented below. Engineers B and C have assigned sections that must be completed using their own genuine interactions and observations.

---

# 2. Engineer A — John Ikwuobe

## Learning Cycle A1 — Priority Calculation

### Problem

Understanding how to implement multiple priority conditions in the correct order.

### Initial Understanding

I understood that Python uses `if`, `elif`, and `else` statements to make decisions.

However, I needed to understand why the order of conditions matters when more than one priority rule could match.

### Prompt to AI

"How should I implement and test ordered priority conditions in Python?"

### AI Guidance

AI explained that Python evaluates conditional statements from top to bottom.

When conditions overlap, the most specific condition should be checked before a more general condition.

### Independent Verification

I compared the suggested logic with the official CampusFlow requirements.

I then tested different combinations of urgency and affected-user counts.

### Critical Evaluation

An earlier AI suggestion used 20 affected users as the threshold for critical priority.

The assignment specified 10 affected users.

I rejected the incorrect threshold and followed the project specification.

### Verification Result

Automated tests confirmed the expected priority values, including the critical boundary at exactly 10 affected users.

### Final Decision

I accepted the conditional logic approach but corrected the threshold to match the assignment.

### Related Files

- `tickets.py`
- `tests/test_tickets.py`

### What I Learned

I can explain how Python evaluates conditions sequentially and why condition ordering matters when rules overlap.

I also learned that AI suggestions must be checked against the actual requirements.

---

## Learning Cycle A2 — JSON Persistence

### Problem

Understanding how to save Python ticket records and retrieve them after restarting an application.

### Initial Understanding

I understood that lists and dictionaries could store ticket information while a Python program was running.

However, I needed to understand how to preserve that information after the application closed.

### Prompt to AI

"Explain the difference between `json.dump()` and `json.load()` using a small Python example."

### AI Guidance

AI explained that:

- `json.dump()` writes Python data to a JSON file.
- `json.load()` reads JSON data and converts it into Python objects.

### Independent Verification

I implemented `save_tickets()` and `load_tickets()` and tested whether saved ticket records could be loaded correctly.

I also tested missing files, malformed JSON, and unique ticket ID generation after reloading data.

### Verification Result

The storage tests passed, including saving and loading tickets, handling missing files, detecting malformed JSON, and generating unique IDs after reloading saved data.

### Final Decision

I accepted JSON persistence because it met the original project requirements without requiring an external database.

### Related Files

- `storage.py`
- `tests/test_storage.py`

### What I Learned

I can explain serialization, deserialization, file handling, and why persistent storage allows information to survive application restarts.

---

## Learning Cycle A3 — Input Validation and Exception Handling

### Problem

Understanding how to reject invalid ticket information without modifying valid application data.

### Initial Understanding

I understood how to collect user input and append dictionaries to a list.

However, I needed to ensure invalid inputs were rejected before records were added.

### Prompt to AI

"Explain how `ValueError` and validation before list modification prevent invalid records."

### AI Guidance

AI explained how to validate inputs before changing application state.

It also explained how raising `ValueError` allows the calling function or CLI to handle invalid operations.

### Independent Verification

I tested:

- Zero affected users.
- Negative affected users.
- Text values.
- Decimal values.
- Boolean values.
- Blank ticket titles.
- Invalid categories.

### Verification Result

Automated tests confirmed that invalid inputs raised `ValueError` and left the ticket list unchanged.

### Critical Evaluation

I included explicit type checks because Boolean values are subclasses of integers in Python.

Without careful validation, `True` or `False` could be mistakenly accepted as numeric input.

### Final Decision

I accepted the validation-before-modification approach and added appropriate type checking.

### Related Files

- `tickets.py`
- `tests/test_tickets.py`

### What I Learned

I can explain why validation protects data integrity, when to raise `ValueError`, and why rejected operations should not modify valid application state.

---

# 3. Engineer B — Idi Mohammed Mohammed

**Evidence status:** Awaiting Engineer B's actual AI prompts, verification results, and reflections.

The following topics reflect Engineer B's assigned project responsibilities. They are not presented as completed AI learning interactions.

## Learning Cycle B1 — Ticket Assignment and Workflow

**Relevant modules:**
- `campusflow/workflow.py`
- `campusflow/workflow_service.py`

**Engineering topic:** Implementing ticket assignment and valid status transitions.

**To be completed by Engineer B:**

- Problem encountered:
- Initial understanding:
- Actual prompt submitted to AI:
- Guidance received:
- Independent verification performed:
- Observed result:
- Suggestion accepted, modified, or rejected:
- Final decision:
- What I learned:

## Learning Cycle B2 — Priority Queue Sorting

**Relevant module:** `campusflow/reports.py`

**Engineering topic:** Sorting open tickets by priority and numeric ticket ID.

**To be completed by Engineer B:**

- Problem encountered:
- Initial understanding:
- Actual prompt submitted to AI:
- Guidance received:
- Independent verification performed:
- Observed result:
- Suggestion accepted, modified, or rejected:
- Final decision:
- What I learned:

## Learning Cycle B3 — Reporting and Automated Testing

**Relevant module:** `campusflow/reports.py`

**Engineering topic:** Generating accurate ticket reports and verifying edge cases.

**To be completed by Engineer B:**

- Problem encountered:
- Initial understanding:
- Actual prompt submitted to AI:
- Guidance received:
- Independent verification performed:
- Observed result:
- Suggestion accepted, modified, or rejected:
- Final decision:
- What I learned:

---

# 4. Engineer C — Moses Ochekwu

**Primary project contributions:**

- Audit event recording.
- Duplicate ticket detection.
- SLA attention queue and analytics.
- CLI integration.
- Engineering Knowledge Lab.

**Evidence status:** Awaiting Moses Ochekwu's actual AI learning interactions and verification results.

The following are suggested documentation topics based on his confirmed project contributions, not claims about prompts he has already submitted.

## Learning Cycle C1 — Audit Event Recording

**Relevant module:** `campusflow/audit.py`

**Engineering topic:** Recording ticket operations while preserving an append-only audit history.

**To be completed by Moses Ochekwu:**

- Problem encountered:
- Initial understanding:
- Actual prompt submitted to AI:
- Guidance received:
- Independent verification performed:
- Observed result:
- Suggestion accepted, modified, or rejected:
- Final decision:
- What I learned:

## Learning Cycle C2 — Duplicate Detection and SLA Attention Queue

**Relevant modules:**
- `campusflow/duplicates.py`
- `campusflow/reports.py`

**Engineering topics:** Detecting repeated unresolved tickets and sorting tickets by SLA attention requirements.

**To be completed by Moses Ochekwu:**

- Problem encountered:
- Initial understanding:
- Actual prompt submitted to AI:
- Guidance received:
- Independent verification performed:
- Observed result:
- Suggestion accepted, modified, or rejected:
- Final decision:
- What I learned:

## Learning Cycle C3 — CLI Integration and Engineering Knowledge Lab

**Relevant files:**
- `main.py`
- `campusflow/knowledge_lab.py`
- `tests/test_knowledge_lab.py`
- `tests/test_knowledge_lab_cli.py`

**Engineering topics:** Integrating independent modules into the CLI and implementing an interactive learning assessment.

**To be completed by Moses Ochekwu:**

- Problem encountered:
- Initial understanding:
- Actual prompt submitted to AI:
- Guidance received:
- Independent verification performed:
- Observed result:
- Suggestion accepted, modified, or rejected:
- Final decision:
- What I learned:

---

# 5. Project Integration and Verification

CampusFlow Pro combines contributions from all three engineers.

The completed project includes:

- Ticket creation and validation.
- Automatic priority calculation.
- JSON persistence and schema validation.
- Staff assignment.
- Ticket status transitions and reopening.
- SLA deadline calculation.
- Overdue escalation.
- Audit event recording.
- Duplicate detection.
- Original priority queue.
- SLA attention queue.
- Enhanced analytics.
- Interactive command-line interface.
- Engineering Knowledge Lab.
- JSON quiz session persistence.

## Final Automated Verification

The complete automated test suite was executed after merging Pull Request #8.

**Command:**

`python -m pytest -q`

**Observed result:**

`147 passed in 0.57s`

**Verified main commit:**

`ea0be81`

This verifies that the automated test suite passed on the integrated project version.

It does not, by itself, establish that every contributor completed their individual AI learning evidence or Knowledge Lab session.

---

# 6. Critical Evaluation of AI Assistance

The project demonstrates the importance of evaluating AI-generated suggestions before accepting them.

A documented example occurred during priority calculation.

An AI suggestion used 20 affected users as the critical-priority threshold.

The assignment required 10 affected users.

Engineer A rejected the incorrect suggestion and followed the specification.

This example demonstrates an important engineering principle:

**Project requirements and independently verified behavior take precedence over AI-generated recommendations.**

Additional examples of accepted, modified, or rejected AI guidance should be documented by Engineers B and C based on their actual development experiences.

---

# 7. Individual Learning Reflections

Each contributor should complete a personal reflection explaining:

- Which project feature was most challenging.
- How AI assistance contributed to understanding the problem.
- Which AI suggestion required correction or further investigation.
- How tests or experiments were used to verify the solution.
- What the contributor can now explain independently.
- What the contributor would improve in a future version.

These reflections should be based on each engineer's genuine experience.

Knowledge Lab results and individual quiz reflections will be recorded separately in:

`docs/learning-reflections.md`

---

# 8. Evidence Completion Checklist

| Requirement | Engineer A | Engineer B | Engineer C |
|---|---|---|---|
| Three AI learning cycles | Documented | Awaiting evidence | Awaiting evidence |
| Actual AI prompts | Documented | Awaiting evidence | Awaiting evidence |
| Independent verification | Documented | Awaiting evidence | Awaiting evidence |
| Critical evaluation | Documented | Awaiting evidence | Awaiting evidence |
| Individual reflection | To be finalized | To be completed | To be completed |
| Knowledge Lab result | To be recorded | To be recorded | To be recorded |

---

# 9. Conclusion

CampusFlow Pro demonstrates the use of AI-assisted learning alongside independent software engineering judgment.

The project combines the contributions of:

**John Ikwuobe:** Ticket creation, priority calculation, input validation, JSON persistence, automated testing, and documentation.

**Idi Mohammed Mohammed:** Staff assignment, ticket workflow, reopening, priority queue, reporting, and testing.

**Moses Ochekwu:** Audit event recording, duplicate detection, SLA attention queue and analytics, CLI integration, and Engineering Knowledge Lab.

The integrated system passed all 147 automated tests on the verified main commit.

The remaining individual learning evidence will be completed using authentic records and reflections from the relevant contributors before final submission.