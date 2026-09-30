import math
from datetime import datetime

class ValidationError(ValueError):
    pass


# validates amount input from user
def val_amt(s):
    s_raw = s.strip()
    try:
        x_num = float(s_raw)
    except:
        raise ValidationError("Amount spent must be a number.")
    # check for weird edge cases
    if x_num <= 0:
        raise ValidationError("Amount spent must be finite and greater than zero.")
    if math.isnan(x_num) or math.isinf(x_num):
        raise ValidationError("Amount spent must be finite and greater than zero.")
    return round(x_num, 2)


def valid_date(s):
    s_raw = s.strip()
    # try parsing dd-mm-yyyy
    try:
        d_obj = datetime.strptime(s_raw, "%d-%m-%Y")
    except:
        raise ValidationError("Date must be in DD-MM-YYYY format.")
    dt_out = d_obj.strftime("%Y-%m-%d")
    return dt_out


def valCategory(s):
    c_str = s.strip()
    if c_str == "":
        raise ValidationError("Category cannot be empty.")
    # 30 char max
    if len(c_str) > 30:
        raise ValidationError("Category must be 30 characters or fewer.")
    else:
        return c_str.title()


# check description length
# max 50 words, blank becomes "-"
def chk_desc(s):
    desc_str = s.strip()
    w_arr = desc_str.split()
    w_cnt = len(w_arr)
    if w_cnt == 0:
        return "-"  # placeholder
    elif w_cnt > 50:
        raise ValidationError("The description cannot be more than 50 words.")
    else:
        return desc_str
