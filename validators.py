import math
from datetime import datetime

class ValidationError(ValueError):
    pass

def val_amt(s):
    # strip whitespace first
    s = s.strip()
    try:
        amt = float(s)
        if math.isfinite(amt):
            if amt > 0:
                return round(amt, 2)
            else:
                raise ValidationError("Amount spent must be finite and greater than zero.")
        else:
            raise ValidationError("Amount spent must be finite and greater than zero.")
    except ValueError:
        raise ValidationError("Amount spent must be a number.")

def valid_date(s):
    s = s.strip()
    try:
        # parse dd-mm-yyyy
        d = datetime.strptime(s, "%d-%m-%Y")
        return d.strftime("%Y-%m-%d")
    except ValueError:
        raise ValidationError("Date must be in DD-MM-YYYY format.")

def valCategory(s):
    s = s.strip()
    if len(s) == 0:
        raise ValidationError("Category cannot be empty.")
    else:
        if len(s) > 30:
            raise ValidationError("Category must be 30 characters or fewer.")
        return s.title()

def chk_desc(s):
    s = s.strip()
    words = s.split()
    if len(words) == 0:
        return "-"
    else:
        if len(words) > 50:
            raise ValidationError("The description cannot be more than 50 words.")
        return s
