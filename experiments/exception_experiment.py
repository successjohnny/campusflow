
def borrow_resource(available, requested):
    """Validate a request before changing stock."""

    if type(requested) is not int or requested <= 0:
        raise ValueError(
            "Requested quantity must be a positive integer"
        )

    if requested > available:
        raise ValueError(
            "Not enough resources available"
        )

    return available - requested


def run_experiment(available, requested):
    print(f"\nAvailable: {available}")
    print(f"Requested: {requested}")

    try:
        remaining = borrow_resource(available, requested)

    except ValueError as error:
        print("Error caught:", error)
        print("Stock remains:", available)

    else:
        print("Request successful.")
        print("Remaining stock:", remaining)


# Experiment A: Valid request
run_experiment(5, 2)

# Experiment B: Request exceeds stock
run_experiment(5, 8)

# Experiment C: Zero quantity
run_experiment(5, 0)

# Experiment D: Invalid data type
run_experiment(5, "two")