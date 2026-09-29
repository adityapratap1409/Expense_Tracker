# input validators and cleanup helpers
import math
from datetime import datetime


class ValidationError(ValueError):
    pass


def val_amt(val):
    val = val.strip()
    try:
        amt = float(val)
    except ValueError:
        raise ValidationError("Amount spent must be a number.")

    # sanity checks: positive & not inf/nan
    if amt <= 0 or not math.isfinite(amt):
        raise ValidationError("Amount spent must be finite and greater than zero.")

    # 2 decimal places for cents
    return round(amt, 2)


def valid_date(val):
    val = val.strip()
    try:
        # expect dd-mm-yyyy from user prompt
        d = datetime.strptime(val, "%d-%m-%Y")
    except ValueError:
        raise ValidationError("Date must be in DD-MM-YYYY format.")

    # sqlite sorts standard ISO strings (yyyy-mm-dd) much easier
    return d.strftime("%Y-%m-%d")


def valCategory(val):
    cat = val.strip()
    if not cat:
        raise ValidationError("Category cannot be empty.")
    if len(cat) > 30:
        raise ValidationError("Category must be 30 characters or fewer.")

    # title-case so 'food' and 'Food' don't become two separate categories
    return cat.title()


def chk_desc(val):
    txt = val.strip()
    words = txt.split()

    # dash placeholder keeps table alignment neat
    if not words:
        return "-"

    if len(words) > 50:
        raise ValidationError("The description cannot be more than 50 words.")

    return txt
