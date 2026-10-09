
from tickets import create_ticket

tickets = []

print("Before:", tickets)

try:
    create_ticket(
        tickets,
        "Wi-Fi is down",
        "Network",
        "high",
        0
    )

except ValueError as error:
    print("Caught error:", error)

print("After:", tickets)
print("List unchanged:", tickets == [])