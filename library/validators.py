from datetime import datetime

from .exceptions import ValidationError


def required_text(value, field_name):
    value = value.strip()

    if not value:
        raise ValidationError(
            f"{field_name} cannot be empty."
        )

    return value


def positive_int(value, field_name):

    try:
        number = int(value)

    except (TypeError, ValueError) as error:

        raise ValidationError(
            f"{field_name} must be a number."
        ) from error

    if number <= 0:

        raise ValidationError(
            f"{field_name} must be greater than 0."
        )

    return number


def date_dd_mm_yyyy(value, field_name):

    value = value.strip()

    try:

        datetime.strptime(
            value,
            "%d-%m-%Y"
        )

    except ValueError as error:

        raise ValidationError(
            f"{field_name} must be in DD-MM-YYYY format."
        ) from error

    return value