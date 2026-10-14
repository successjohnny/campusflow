"""Interactive learning quiz for CampusFlow Pro."""


QUESTIONS = [
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
            "SLA means Service Level Agreement. "
            "It defines expected service response or resolution times."
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
        "explanation": (
            "Critical tickets have the shortest SLA deadline."
        ),
    },
    {
        "question": "What is the purpose of an audit log?",
        "options": {
            "A": "To delete resolved tickets",
            "B": "To record actions performed on tickets",
            "C": "To change ticket priorities automatically",
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
            "Duplicate detection helps identify repeated reports "
            "of the same unresolved issue."
        ),
    },
    {
        "question": "What does an overdue ticket mean?",
        "options": {
            "A": "A ticket that has been resolved",
            "B": "A ticket without a title",
            "C": "An unresolved ticket past its SLA deadline",
            "D": "A ticket assigned to two staff members",
        },
        "answer": "C",
        "explanation": (
            "An unresolved ticket becomes overdue "
            "when its SLA deadline has passed."
        ),
    },
]


def check_answer(question, answer):
    """Check a quiz answer and return whether it is correct."""

    if not isinstance(answer, str):
        return False

    return answer.strip().upper() == question["answer"]


def calculate_score(questions, answers):
    """Calculate the total correct answers and percentage."""

    if len(questions) != len(answers):
        raise ValueError(
            "The number of answers must match the questions"
        )

    correct = 0

    for question, answer in zip(questions, answers):
        if check_answer(question, answer):
            correct += 1

    total = len(questions)

    percentage = (
        round(correct / total * 100, 2)
        if total > 0
        else 0.0
    )

    return {
        "correct": correct,
        "total": total,
        "percentage": percentage,
    }


def run_quiz(input_func=input, print_func=print):
    """Run the interactive Knowledge Lab quiz."""

    while True:
        print_func("\n===== CAMPUSFLOW KNOWLEDGE LAB =====")

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

            print_func(
                f"Explanation: {question['explanation']}"
            )

        result = calculate_score(QUESTIONS, answers)

        print_func("\n===== QUIZ RESULTS =====")
        print_func(
            f"Score: {result['correct']}/{result['total']}"
        )
        print_func(
            f"Percentage: {result['percentage']}%"
        )

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