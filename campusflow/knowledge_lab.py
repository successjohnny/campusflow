
"""Interactive Knowledge Lab with persistent quiz sessions."""

import json
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TypedDict
from uuid import uuid4


class Question(TypedDict):
    question: str
    options: dict[str, str]
    answer: str
    explanation: str


class QuizResult(TypedDict):
    correct: int
    total: int
    percentage: float


InputFunction = Callable[[str], str]
PrintFunction = Callable[[str], Any]


SESSION_DIR: Path = Path("data/knowledge_lab_sessions")


QUESTIONS: list[Question] = [
    {
        "question": "What does SLA stand for?",
        "options": {
            "A": "Software Learning Application",
            "B": "Service Level Agreement",
            "C": "System Login Authentication",
            "D": "Student Learning Assessment",
        },
        "answer": "B",
        "explanation": (
            "SLA means Service Level Agreement. It defines "
            "expected service response or resolution times."
        ),
    },
    {
        "question": "Which ticket priority requires the fastest response?",
        "options": {
            "A": "Low",
            "B": "Medium",
            "C": "Critical",
            "D": "High",
        },
        "answer": "C",
        "explanation": "Critical tickets have the shortest SLA deadline.",
    },
    {
        "question": "What is the purpose of an audit log?",
        "options": {
            "A": "To delete resolved tickets",
            "B": "To record actions performed on tickets",
            "C": "To change priorities automatically",
            "D": "To prevent users from logging in",
        },
        "answer": "B",
        "explanation": (
            "An audit log records important actions, "
            "including who performed them and when."
        ),
    },
    {
        "question": "Why should duplicate tickets be detected?",
        "options": {
            "A": "To hide existing tickets",
            "B": "To reduce repeated reports of the same issue",
            "C": "To increase the number of tickets",
            "D": "To automatically resolve all tickets",
        },
        "answer": "B",
        "explanation": (
            "Duplicate detection identifies repeated reports "
            "of the same unresolved issue."
        ),
    },
    {
        "question": "What does an overdue ticket mean?",
        "options": {
            "A": "A resolved ticket",
            "B": "A ticket without a title",
            "C": "An unresolved ticket past its SLA deadline",
            "D": "A ticket assigned to two staff members",
        },
        "answer": "C",
        "explanation": (
            "An unresolved ticket is overdue when "
            "its SLA deadline has passed."
        ),
    },
    {
        "question": "Which timestamp records when a ticket was created?",
        "options": {
            "A": "created_at",
            "B": "updated_at",
            "C": "due_at",
            "D": "event_id",
        },
        "answer": "A",
        "explanation": (
            "created_at records ticket creation time. "
            "updated_at tracks subsequent changes."
        ),
    },
    {
        "question": "What happens when a resolved ticket is reopened?",
        "options": {
            "A": "Its ID changes",
            "B": "Its audit history is deleted",
            "C": "Its priority becomes low",
            "D": "A new SLA cycle begins",
        },
        "answer": "D",
        "explanation": (
            "Reopening begins a new SLA cycle "
            "with a recalculated deadline."
        ),
    },
    {
        "question": "Why is atomic JSON saving useful?",
        "options": {
            "A": "It automatically fixes invalid tickets",
            "B": "It eliminates all disk errors",
            "C": "It reduces the risk of partial file replacement",
            "D": "It makes JSON a database server",
        },
        "answer": "C",
        "explanation": (
            "Writing to a temporary file and replacing the "
            "destination reduces the risk of a partial update."
        ),
    },
    {
        "question": "Which tickets belong in the SLA attention queue?",
        "options": {
            "A": "Only resolved tickets",
            "B": "Open and in-progress tickets",
            "C": "Only unassigned tickets",
            "D": "Only critical tickets",
        },
        "answer": "B",
        "explanation": (
            "The SLA attention queue includes unresolved "
            "open and in-progress tickets."
        ),
    },
    {
        "question": "What does an idempotent escalation check ensure?",
        "options": {
            "A": "Repeated checks do not duplicate escalation events",
            "B": "Every ticket becomes critical",
            "C": "All tickets are resolved automatically",
            "D": "Ticket deadlines are deleted",
        },
        "answer": "A",
        "explanation": (
            "An idempotent check records no additional "
            "escalation for a ticket already escalated "
            "in the same SLA cycle."
        ),
    },
]


def check_answer(question: Question, answer: str) -> bool:
    """Return True when an answer matches the correct option."""
    if not isinstance(answer, str):
        return False

    return answer.strip().upper() == question["answer"]


def calculate_score(questions: list[Question], answers: list[str]) -> QuizResult:
    """Return the number correct, total, and percentage."""
    if len(questions) != len(answers):
        raise ValueError(
            "The number of answers must match the questions"
        )

    correct = sum(
        check_answer(question, answer)
        for question, answer in zip(questions, answers)
    )

    total = len(questions)
    percentage = round(correct / total * 100, 2) if total else 0.0

    return {
        "correct": correct,
        "total": total,
        "percentage": percentage,
    }


def save_quiz_session(
    participant: str,
    answers: list[str],
    result: QuizResult,
    session_dir: str | Path | None = None,
    now: datetime | None = None,
) -> Path:
    """Save one completed quiz attempt to a separate JSON file."""
    if not isinstance(participant, str) or not participant.strip():
        raise ValueError("Participant name cannot be empty")

    if len(answers) != len(QUESTIONS):
        raise ValueError("Cannot save an incomplete quiz")

    if not all(
        isinstance(answer, str)
        and answer.strip().upper() in question["options"]
        for question, answer in zip(QUESTIONS, answers)
    ):
        raise ValueError("Quiz contains an invalid answer")

    expected = calculate_score(QUESTIONS, answers)
    if result != expected:
        raise ValueError("Quiz result does not match the answers")

    timestamp = now or datetime.now(UTC)
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("Session timestamp must include a timezone")

    timestamp = timestamp.astimezone(UTC)
    session_id = uuid4().hex

    session = {
        "session_id": session_id,
        "participant": participant.strip(),
        "completed_at": timestamp.isoformat(),
        "answers": [answer.strip().upper() for answer in answers],
        "correct": result["correct"],
        "total": result["total"],
        "percentage": result["percentage"],
    }

    directory = Path(session_dir) if session_dir is not None else SESSION_DIR
    directory.mkdir(parents=True, exist_ok=True)

    path = directory / f"{session_id}.json"

    # Exclusive creation prevents accidentally replacing an existing session.
    with path.open("x", encoding="utf-8") as file:
        json.dump(session, file, indent=2)
        file.write("\n")

    return path


def run_quiz(
    input_func: InputFunction = input,
    print_func: PrintFunction = print,
    session_dir: str | Path | None = None,
) -> QuizResult:
    """Run the Knowledge Lab and save each completed attempt."""
    while True:
        print_func("\n===== CAMPUSFLOW KNOWLEDGE LAB =====")

        while True:
            participant = input_func(
                "Participant name: "
            ).strip()

            if participant:
                break

            print_func("Participant name cannot be empty.")

        answers = []

        for number, question in enumerate(QUESTIONS, start=1):
            print_func(f"\nQuestion {number}:")
            print_func(question["question"])

            for letter, option in question["options"].items():
                print_func(f"{letter}. {option}")

            while True:
                answer = input_func(
                    "Your answer (A/B/C/D): "
                ).strip().upper()

                if answer in question["options"]:
                    break

                print_func(
                    "Invalid choice. Enter A, B, C, or D."
                )

            answers.append(answer)

            if check_answer(question, answer):
                print_func("Correct!")
            else:
                print_func(
                    f"Incorrect. Correct answer: "
                    f"{question['answer']}"
                )

            print_func(f"Explanation: {question['explanation']}")

        result = calculate_score(QUESTIONS, answers)

        print_func("\n===== QUIZ RESULTS =====")
        print_func(f"Score: {result['correct']}/{result['total']}")
        print_func(f"Percentage: {result['percentage']}%")

        try:
            path = save_quiz_session(
                participant,
                answers,
                result,
                session_dir=session_dir,
            )
        except OSError as error:
            print_func(f"Unable to save quiz session: {error}")
            raise

        print_func(f"Session saved: {path}")

        while True:
            replay = input_func(
                "\nTry again? (yes/no): "
            ).strip().lower()

            if replay in {"yes", "y", "no", "n"}:
                break

            print_func("Please enter yes or no.")

        if replay in {"no", "n"}:
            print_func("Returning to CampusFlow menu.")
            return result