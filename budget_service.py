from validators import val_amt, valCategory

WARN_PCT = 0.8
# ALERT_EMAIL = False  # maybe add email alerts later?

class BudgetService:
    def __init__(self, storage):
        self.storage = storage

    def set_bgt(self, cat, lim):
        c = valCategory(cat)
        l = val_amt(lim)
        self.storage.setBudget(c, l)

    def getStatus(self, cat, mth):
        c = valCategory(cat)
        bgt = self.storage.get_bgt(c)
        if bgt == None:
            return None

        # calc everything
        lim = bgt["monthly_limit"]
        spent = self.storage.month_sum(c, mth)
        rem = lim - spent
        pct = 0.0
        if lim > 0:
            pct = spent / lim

        result = {}
        result["limit"] = lim
        result["spent"] = spent
        result["remaining"] = rem
        result["percent_used"] = pct
        return result

    def chk_alert(self, cat, mth):
        c = valCategory(cat)
        s = self.getStatus(cat, mth)
        if s == None:
            return None
        pct = s["percent_used"]
        # check thresholds
        msg = ""
        if pct >= 1.0:
            msg = c + " has exceeded its budget limit"
        elif pct >= WARN_PCT:
            msg = c + " is approaching its limit. Please spend responsibly"
        else:
            msg = c + " is yet to reach its limit. Happy spending!"
        return msg
