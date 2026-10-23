
"""Tests for CampusFlow Pro Knowledge Lab."""

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from campusflow.knowledge_lab import (
    QUESTIONS,
    check_answer,
    calculate_score,
    run_quiz,
    save_quiz_session,
)


class TestKnowledgeLab(unittest.TestCase):

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.session_dir: Path = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def correct_answers(self) -> list[str]:
        return [question["answer"] for question in QUESTIONS]

    def wrong_answers(self) -> list[str]:
        return [
            next(
                option for option in question["options"]
                if option != question["answer"]
            )
            for question in QUESTIONS
        ]

    def run_answers(
        self,
        answers: list[str],
    ) -> tuple[dict[str, Any], list[str]]:
        values = iter(answers)
        output: list[str] = []

        result = run_quiz(
            input_func=lambda prompt: next(values),
            print_func=output.append,
            session_dir=self.session_dir,
        )
        return result, output

    def session_files(self) -> list[Path]:
        return list(self.session_dir.glob("*.json"))

    def test_ten_questions(self) -> None:
        self.assertEqual(len(QUESTIONS), 10)

    def test_correct_answer(self) -> None:
        self.assertTrue(check_answer(QUESTIONS[0], "B"))

    def test_lowercase_answer(self) -> None:
        self.assertTrue(check_answer(QUESTIONS[0], "b"))

    def test_answer_with_spaces(self) -> None:
        self.assertTrue(check_answer(QUESTIONS[0], " B "))

    def test_wrong_answer(self) -> None:
        self.assertFalse(check_answer(QUESTIONS[0], "A"))

    def test_non_string_answer(self) -> None:
        self.assertFalse(check_answer(QUESTIONS[0], 123))

    def test_perfect_score(self) -> None:
        result = calculate_score(
            QUESTIONS, self.correct_answers()
        )
        self.assertEqual(result["correct"], 10)
        self.assertEqual(result["percentage"], 100.0)

    def test_zero_score(self) -> None:
        result = calculate_score(
            QUESTIONS, self.wrong_answers()
        )
        self.assertEqual(result["correct"], 0)
        self.assertEqual(result["percentage"], 0.0)

    def test_mismatched_answers(self) -> None:
        with self.assertRaises(ValueError):
            calculate_score(QUESTIONS, ["A"])

    def test_empty_quiz(self) -> None:
        result = calculate_score([], [])
        self.assertEqual(result["correct"], 0)
        self.assertEqual(result["percentage"], 0.0)

    def test_interactive_quiz(self) -> None:
        result, output = self.run_answers(
            ["Test Engineer", *self.correct_answers(), "no"]
        )

        self.assertEqual(result["correct"], 10)
        self.assertEqual(len(self.session_files()), 1)
        self.assertTrue(
            any("Session saved:" in line for line in output)
        )

    def test_invalid_choice_retried(self) -> None:
        result, output = self.run_answers(
            [
                "Test Engineer",
                "X",
                *self.correct_answers(),
                "no",
            ]
        )

        self.assertEqual(result["correct"], 10)
        self.assertIn(
            "Invalid choice. Enter A, B, C, or D.",
            output,
        )

    def test_replay_creates_separate_sessions(self) -> None:
        result, output = self.run_answers(
            [
                "Engineer A",
                *self.correct_answers(),
                "yes",
                "Engineer B",
                *self.wrong_answers(),
                "no",
            ]
        )

        self.assertEqual(result["correct"], 0)
        self.assertEqual(len(self.session_files()), 2)
        self.assertEqual(
            output.count(
                "\n===== CAMPUSFLOW KNOWLEDGE LAB ====="
            ),
            2,
        )

    def test_session_json_fields(self) -> None:
        answers: list[str] = self.correct_answers()
        result = calculate_score(QUESTIONS, answers)
        now: datetime = datetime(
            2026, 10, 14, 12, 0, tzinfo=timezone.utc
        )

        path = save_quiz_session(
            "Engineer A",
            answers,
            result,
            session_dir=self.session_dir,
            now=now,
        )

        with path.open(encoding="utf-8") as file:
            saved = json.load(file)

        self.assertEqual(saved["participant"], "Engineer A")
        self.assertEqual(saved["correct"], 10)
        self.assertEqual(saved["total"], 10)
        self.assertEqual(saved["percentage"], 100.0)
        self.assertEqual(saved["answers"], answers)
        self.assertEqual(
            saved["completed_at"],
            "2026-10-14T12:00:00+00:00",
        )
        self.assertTrue(saved["session_id"])

    def test_incomplete_session_is_not_saved(self) -> None:
        with self.assertRaises(ValueError):
            save_quiz_session(
                "Engineer A",
                ["B"],
                {"correct": 1, "total": 1, "percentage": 100.0},
                session_dir=self.session_dir,
            )

        self.assertEqual(self.session_files(), [])

    def test_invalid_result_is_not_saved(self) -> None:
        answers: list[str] = self.correct_answers()

        with self.assertRaises(ValueError):
            save_quiz_session(
                "Engineer A",
                answers,
                {"correct": 0, "total": 10, "percentage": 0.0},
                session_dir=self.session_dir,
            )

        self.assertEqual(self.session_files(), [])

    def test_invalid_participant_is_rejected(self) -> None:
        answers: list[str] = self.correct_answers()

        with self.assertRaises(ValueError):
            save_quiz_session(
                " ",
                answers,
                calculate_score(QUESTIONS, answers),
                session_dir=self.session_dir,
            )

        self.assertEqual(self.session_files(), [])

    def test_interrupted_quiz_creates_no_session(self) -> None:
        answers = iter(["Test Engineer", "B"])

        with self.assertRaises(StopIteration):
            run_quiz(
                input_func=lambda prompt: next(answers),
                print_func=lambda message: None,
                session_dir=self.session_dir,
            )

        self.assertEqual(self.session_files(), [])


if __name__ == "__main__":
    unittest.main()