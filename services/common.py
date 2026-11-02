"""Shared validation helpers and exceptions used by all service modules."""
import re
from datetime import date, datetime

NEAR_EXPIRY_DAYS = 30  # a batch expiring within this many days is "Near Expiry"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ServiceError(Exception):
    """Base class. The message is safe to show to the user."""


class ValidationError(ServiceError):
    """Input or business-rule problem (bad quantity, expired batch, ...)."""


def today():
    return date.today()


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(value, field, required=True, max_len=100):
    value = "" if value is None else str(value).strip()
    if required and not value:
        raise ValidationError(f"{field} is required.")
    if len(value) > max_len:
        raise ValidationError(f"{field} must be at most {max_len} characters.")
    return value or None


def parse_int(value, field, minimum=1):
    """Whole number >= minimum. Rejects '', 'abc', '2.5', and negatives."""
    try:
        number = int(str(value).strip())
    except (TypeError, ValueError):
        raise ValidationError(f"{field} must be a whole number.")
    if number < minimum:
        raise ValidationError(f"{field} must be at least {minimum}.")
    return number


def parse_price(value, field):
    """Non-negative number. Rejects text, NaN, infinity and negatives."""
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        raise ValidationError(f"{field} must be a valid number.")
    if number != number or number in (float("inf"), float("-inf")):
        raise ValidationError(f"{field} must be a valid number.")
    if number < 0:
        raise ValidationError(f"{field} cannot be negative.")
    return round(number, 2)


def parse_date(value, field, required=True):
    """Return an ISO date string 'YYYY-MM-DD', or None if optional and blank."""
    value = "" if value is None else str(value).strip()
    if not value:
        if required:
            raise ValidationError(f"{field} is required.")
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        raise ValidationError(f"{field} must be a valid date (YYYY-MM-DD).")


def is_expired(expiry_date, on=None):
    return expiry_date < (on or today()).isoformat()
