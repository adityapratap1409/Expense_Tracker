import math
from datetime import datetime

class ValidationError(ValueError):
    pass


# validates amount input from user
def val_amt(s):
    s = s.strip()
    try:
        x = float(s)
    except:
        raise ValidationError("Amount spent must be a number.")
    # check for weird edge cases
    if x <= 0:
        raise ValidationError("Amount spent must be finite and greater than zero.")
    if math.isnan(x) or math.isinf(x):
        raise ValidationError("Amount spent must be finite and greater than zero.")
    return round(x, 2)


def valid_date(s):
    s = s.strip()
    # try parsing dd-mm-yyyy
    try:
        d = datetime.strptime(s, "%d-%m-%Y")
    except:
        raise ValidationError("Date must be in DD-MM-YYYY format.")
    result = d.strftime("%Y-%m-%d")
    return result


def valCategory(s):
    s = s.strip()
    if s == "":
        raise ValidationError("Category cannot be empty.")
    # 30 char max
    if len(s) > 30:
        raise ValidationError("Category must be 30 characters or fewer.")
    else:
        return s.title()


# check description length
# max 50 words, blank becomes "-"
def chk_desc(s):
    s = s.strip()
    w = s.split()
    n = len(w)
    if n == 0:
        return "-"  # placeholder
    elif n > 50:
        raise ValidationError("The description cannot be more than 50 words.")
    else:
        return s
