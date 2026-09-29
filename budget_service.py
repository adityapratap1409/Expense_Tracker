from validators import val_amt, valCategory

WARN_PCT = 0.8

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
        if bgt is not None:
            spent = self.storage.month_sum(c, mth)
            lim = bgt["monthly_limit"]
            rem = lim - spent
            if lim > 0:
                pct = spent / lim
            else:
                pct = 0.0
            return {
                "limit": lim,
                "spent": spent,
                "remaining": rem,
                "percent_used": pct,
            }
        else:
            return None

    def chk_alert(self, cat, mth):
        c = valCategory(cat)
        stat = self.getStatus(cat, mth)
        if stat is not None:
            pct = stat["percent_used"]
            if pct >= 1.0:
                return c + " has exceeded its budget limit"
            else:
                if pct >= WARN_PCT:
                    return c + " is approaching its limit. Please spend responsibly"
                else:
                    return c + " is yet to reach its limit. Happy spending!"
        else:
            return None
