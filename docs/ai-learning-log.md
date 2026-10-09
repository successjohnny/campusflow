# AI Learning Log — Engineer A

## Interaction 1 — Priority Calculation

**Problem:** Understanding how to apply multiple priority rules in the correct order.

**My initial understanding:** [Explain in your own words.]

**Prompt to AI:** How should I implement and test ordered priority conditions?

**Useful AI guidance:** AI suggested using conditional statements to select the first matching rule.

**Independent verification:** Compared the suggested implementation against the official CampusFlow specification and ran the priority tests.

**Critical evaluation:** The initial AI suggestion incorrectly used 20 affected users as the critical threshold. The assignment specifies 10. I rejected the incorrect threshold and corrected the implementation.

**Verification result:** The ticket test suite passed.

**Related file:** `tickets.py`, `tests/test_tickets.py`

**What I can now explain:** [Write your own explanation.]

---

## Interaction 2 — JSON Persistence

**Problem:** Understanding how Python saves and reloads structured data.

**My initial understanding:** [Complete yourself.]

**Prompt to AI:** Explain the difference between json.dump() and json.load() using a small example.

**Independent experiment:** [Record your actual experiment.]

**Verification result:** [Record observed output.]

**Decision:** [Accepted, improved or rejected.]

**Related file:** `storage.py`, `tests/test_storage.py`

**What I can now explain:** [Complete yourself.]

---

## Interaction 3 — Input Validation and Exceptions

**Problem:** Understanding how to reject invalid data without modifying the ticket list.

**My initial understanding:** [Complete yourself.]

**Prompt to AI:** Explain how ValueError and validation before list modification prevent invalid records.

**Independent experiment:** [Record what you tested.]

**Verification result:** [Record observed output.]

**Decision:** [Accepted, improved or rejected.]

**Related file:** `tickets.py`, `tests/test_tickets.py`

**What I can now explain:** [Complete yourself.]