from datetime import date


def positive_integer(value, field_name):
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a positive whole number.")

    try:
        parsed_value = int(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"{field_name} must be a positive whole number."
        ) from None

    if parsed_value <= 0:
        raise ValueError(f"{field_name} must be a positive whole number.")

    if isinstance(value, float) and not value.is_integer():
        raise ValueError(f"{field_name} must be a positive whole number.")

    return parsed_value


def iso_date(value, field_name):
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a valid date.")

    try:
        parsed_date = date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a valid date.") from None

    if parsed_date.isoformat() != value:
        raise ValueError(f"{field_name} must be a valid date.")

    return parsed_date.isoformat()
