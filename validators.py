import math
from datetime import datetime
class ValidationError(ValueError):
    pass

def validate_amount(raw):
    raw=raw.strip()
    try:
            amt=float(raw)
    except ValueError:
         raise ValidationError("Amount spent must be a number.")
    if amt<=0 or not math.isfinite(amt):
         raise ValidationError("Amount spent must be finite and greater than zero.")
    return round(amt,2)

def validate_date(raw):
    raw=raw.strip()
    try:
       parsed=datetime.strptime(raw, "%d-%m-%Y")
    except ValueError:
        raise ValidationError("Date must be in DD-MM-YYYY format.")
    return parsed.strftime("%Y-%m-%d")

def validate_category(raw):
    raw=raw.strip()
    if not raw:
        raise ValidationError("Category cannot be empty.")
    elif len(raw)>30:
        raise ValidationError("Category must be 30 characters or fewer.")
    return raw.title()

def validate_description(raw):
    raw = raw.strip()
    if len(raw.split())==0:
        return "-"
    if len(raw.split())>50:
        raise ValidationError("The description cannot be more than 50 words.") 
    return raw
