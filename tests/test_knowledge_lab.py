"""Tests for CampusFlow Pro Knowledge Lab."""

import unittest

from campusflow.knowledge_lab import (
    QUESTIONS,
    check_answer,
    calculate_score,
    run_quiz,
)


class TestKnowledgeLab(unittest.TestCase):

    def test_correct_answer(self):
        self.assertTrue(
            check_answer(QUESTIONS[0], "B")
        )

    def test_lowercase_answer(self):
        self.assertTrue(
            check_answer(QUESTIONS[0], "b")
        )

    def test_answer_with_spaces(self):
        self.assertTrue(
            check_answer(QUESTIONS[0], " B ")
        )

    def test_wrong_answer(self):
        self.assertFalse(
            check_answer(QUESTIONS[0], "A")
        )

    def test_non_string_answer(self):
        self.assertFalse(
            check_answer(QUESTIONS[0], 123)
        )

    def test_perfect_score(self):
        answers = [
            question["answer"]
            for question in QUESTIONS
        ]

        result = calculate_score(
            QUESTIONS,
            answers,
        )

        self.assertEqual(result["correct"], 5)
        self.assertEqual(result["percentage"], 100.0)

    def test_zero_score(self):
        answers = ["A", "A", "A", "A", "A"]

        result = calculate_score(
            QUESTIONS,
            answers,
        )

        self.assertEqual(result["correct"], 0)
        self.assertEqual(result["percentage"], 0.0)

    def test_mismatched_answers(self):
        with self.assertRaises(ValueError):
            calculate_score(
                QUESTIONS,
                ["A"],
            )

    def test_empty_quiz(self):
        result = calculate_score([], [])

        self.assertEqual(result["correct"], 0)
        self.assertEqual(result["percentage"], 0.0)

    def test_interactive_quiz(self):
        answers = iter([
            "B",
            "C",
            "B",
            "B",
            "C",
            "no",
        ])

        output = []

        result = run_quiz(
            input_func=lambda prompt: next(answers),
            print_func=output.append,
        )

        self.assertEqual(result["correct"], 5)
        self.assertEqual(result["percentage"], 100.0)

    def test_invalid_choice_retried(self):
        answers = iter([
            "X",
            "B",
            "C",
            "B",
            "B",
            "C",
            "no",
        ])

        output = []

        result = run_quiz(
            input_func=lambda prompt: next(answers),
            print_func=output.append,
        )

        self.assertEqual(result["correct"], 5)
        self.assertIn(
            "Invalid choice. Enter A, B, C, or D.",
            output,
        )

    def test_replay_quiz(self):
        answers = iter([
            "B", "C", "B", "B", "C",
            "yes",
            "B", "C", "B", "B", "C",
            "no",
        ])

        output = []

        result = run_quiz(
            input_func=lambda prompt: next(answers),
            print_func=output.append,
        )

        self.assertEqual(result["correct"], 5)

        quiz_starts = output.count(
            "\n===== CAMPUSFLOW KNOWLEDGE LAB ====="
        )

        self.assertEqual(quiz_starts, 2)


if __name__ == "__main__":
    unittest.main()