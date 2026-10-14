"""Integration tests for the Knowledge Lab CLI."""

import unittest
from unittest.mock import patch

import main


class TestKnowledgeLabCLI(unittest.TestCase):

    @patch("main.run_quiz")
    def test_knowledge_lab_menu_launches_quiz(self, mock_quiz):
        """Selecting the Knowledge Lab handler launches the quiz."""

        main.knowledge_lab_menu()

        mock_quiz.assert_called_once_with()

    @patch("builtins.print")
    def test_main_menu_displays_knowledge_lab(self, mock_print):
        """The main menu includes Knowledge Lab as option 8."""

        main.show_menu()

        mock_print.assert_any_call("8. Knowledge Lab")

    @patch("main.load_tickets", return_value=[])
    @patch("main.run_quiz")
    @patch("builtins.input", side_effect=["8", "0"])
    @patch("builtins.print")
    def test_option_eight_returns_to_main_menu(
        self,
        mock_print,
        mock_input,
        mock_quiz,
        mock_load,
    ):
        """After the quiz finishes, the main menu remains available."""

        main.main()

        mock_quiz.assert_called_once_with()
        mock_load.assert_called_once_with()

        self.assertEqual(mock_input.call_count, 2)

        mock_print.assert_any_call(
            "Thank you for using CampusFlow!"
        )


if __name__ == "__main__":
    unittest.main()