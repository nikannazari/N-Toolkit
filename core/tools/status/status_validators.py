"""
status_validators.py - Validation utilities for Status tool.
"""
def validate_interval(val: str) -> tuple[bool, int]:
    if not val:
        return True, 2  # Default to 2 seconds
    try:
        v = int(val)
        if v < 1:
            return False, "Interval must be at least 1 second."
        return True, v
    except ValueError:
        return False, "Interval must be a number."