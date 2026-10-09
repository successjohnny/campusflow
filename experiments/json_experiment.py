
import json
from pathlib import Path

# Temporary file used only for this experiment
file_path = Path("experiments/sample_tickets.json")

# A Python list containing a dictionary
tickets = [
    {
        "id": "T001",
        "title": "Campus Wi-Fi is down",
        "priority": "critical"
    }
]

# EXPERIMENT A: Save Python data to JSON
with file_path.open("w", encoding="utf-8") as file:
    json.dump(tickets, file, indent=4)

print("1. Tickets saved successfully.")

# EXPERIMENT B: Load JSON data into Python
with file_path.open("r", encoding="utf-8") as file:
    loaded_tickets = json.load(file)

print("2. Loaded tickets:", loaded_tickets)

# EXPERIMENT C: Verify data integrity
print("3. Data matches:", tickets == loaded_tickets)

# EXPERIMENT D: Verify data type
print("4. Loaded data type:", type(loaded_tickets).__name__)