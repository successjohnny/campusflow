
"""Tests for CampusFlow Pro Knowledge Lab."""

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from campusflow.knowledge_lab import (
    QUESTIONS,
    check_answer,
    calculate_score,
    run_quiz,
    save_quiz_session,
)


class TestKnowledgeLab(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.session_dir = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def correct_answers(self):
        return [question["answer"] for question in QUESTIONS]

    def wrong_answers(self):
        return [
            next(
                option for option in question["options"]
                if option != question["answer"]
            )
            for question in QUESTIONS
        ]

    def run_answers(self, answers):
        values = iter(answers)
        output = []

        result = run_quiz(
            input_func=lambda prompt: next(values),
            print_func=output.append,
            session_dir=self.session_dir,
        )
        return result, output

    def session_files(self):
        return list(self.session_dir.glob("*.json"))

    def test_ten_questions(self):
        self.assertEqual(len(QUESTIONS), 10)

    def test_correct_answer(self):
        self.assertTrue(check_answer(QUESTIONS[0], "B"))

    def test_lowercase_answer(self):
        self.assertTrue(check_answer(QUESTIONS[0], "b"))

    def test_answer_with_spaces(self):
        self.assertTrue(check_answer(QUESTIONS[0], " B "))

    def test_wrong_answer(self):
        self.assertFalse(check_answer(QUESTIONS[0], "A"))

    def test_non_string_answer(self):
        self.assertFalse(check_answer(QUESTIONS[0], 123))

    def test_perfect_score(self):
        result = calculate_score(
            QUESTIONS, self.correct_answers()
        )
        self.assertEqual(result["correct"], 10)
        self.assertEqual(result["percentage"], 100.0)

    def test_zero_score(self):
        result = calculate_score(
            QUESTIONS, self.wrong_answers()
        )
        self.assertEqual(result["correct"], 0)
        self.assertEqual(result["percentage"], 0.0)

    def test_mismatched_answers(self):
        with self.assertRaises(ValueError):
            calculate_score(QUESTIONS, ["A"])

    def test_empty_quiz(self):
        result = calculate_score([], [])
        self.assertEqual(result["correct"], 0)
        self.assertEqual(result["percentage"], 0.0)

    def test_interactive_quiz(self):
        result, output = self.run_answers(
            ["Test Engineer", *self.correct_answers(), "no"]
        )

        self.assertEqual(result["correct"], 10)
        self.assertEqual(len(self.session_files()), 1)
        self.assertTrue(
            any("Session saved:" in line for line in output)
        )

    def test_invalid_choice_retried(self):
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

    def test_replay_creates_separate_sessions(self):
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

    def test_session_json_fields(self):
        answers = self.correct_answers()
        result = calculate_score(QUESTIONS, answers)
        now = datetime(
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

    def test_incomplete_session_is_not_saved(self):
        with self.assertRaises(ValueError):
            save_quiz_session(
                "Engineer A",
                ["B"],
                {"correct": 1, "total": 1, "percentage": 100.0},
                session_dir=self.session_dir,
            )

        self.assertEqual(self.session_files(), [])

    def test_invalid_result_is_not_saved(self):
        answers = self.correct_answers()

        with self.assertRaises(ValueError):
            save_quiz_session(
                "Engineer A",
                answers,
                {"correct": 0, "total": 10, "percentage": 0.0},
                session_dir=self.session_dir,
            )

        self.assertEqual(self.session_files(), [])

    def test_invalid_participant_is_rejected(self):
        answers = self.correct_answers()

        with self.assertRaises(ValueError):
            save_quiz_session(
                " ",
                answers,
                calculate_score(QUESTIONS, answers),
                session_dir=self.session_dir,
            )

        self.assertEqual(self.session_files(), [])

    def test_interrupted_quiz_creates_no_session(self):
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