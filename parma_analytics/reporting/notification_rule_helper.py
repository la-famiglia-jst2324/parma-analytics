"""This file contains a helper function for comparing values to a threshold.

The function is used in the notification rule comparison engine.
"""


def compare_to_threshold(
    previous_value: int | float, new_value: int | float, threshold: float
) -> bool:
    """Compares the previous value to the new value.

    Args:
        previous_value (any): The previous value.
        new_value (any): The new value.
        threshold (float): The threshold.

    Returns:
        bool: True if the difference between the previous value
        and the new value is greater than the threshold, False otherwise.
    """
    print(
        "inside compare_to_threshold: ",
        abs(new_value - previous_value) / previous_value * 100,
    )
    return abs(new_value - previous_value) / previous_value * 100 >= threshold
