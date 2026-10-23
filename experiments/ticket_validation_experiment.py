
from typing import Any

from tickets import create_ticket


def main() -> None:
    """Verify that invalid ticket creation does not change data."""

    tickets: list[dict[str, Any]] = []

    print("Before:", tickets)

    try:
        create_ticket(
            tickets,
            "Wi-Fi is down",
            "Network",
            "high",
            0,
        )

    except ValueError as error:
        print("Caught error:", error)

    print("After:", tickets)
    print("List unchanged:", tickets == [])


if __name__ == "__main__":
    main()