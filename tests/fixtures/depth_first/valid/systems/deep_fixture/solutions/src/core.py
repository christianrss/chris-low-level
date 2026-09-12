def run(value: int) -> int:
    if value < 0:
        raise ValueError("value must be non-negative")
    return value
