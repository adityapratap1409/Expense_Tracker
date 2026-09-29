from validators import val_amt, valCategory

# warn at 80% mark before user blows their budget
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
        if bgt is None:
            return None

        spent = self.storage.month_sum(c, mth)
        lim = bgt["monthly_limit"]
        rem = lim - spent
        pct = spent / lim if lim > 0 else 0.0

        return {
            "limit": lim,
            "spent": spent,
            "remaining": rem,
            "percent_used": pct,
        }

    def chk_alert(self, cat, mth):
        c = valCategory(cat)
        stat = self.getStatus(cat, mth)
        if stat is None:
            return None

        pct = stat["percent_used"]

        # 3 levels: over budget, close to limit, or under
        if pct >= 1.0:
            return f"{c} has exceeded its budget limit"
        elif pct >= WARN_PCT:
            return f"{c} is approaching its limit. Please spend responsibly"
        else:
            return f"{c} is yet to reach its limit. Happy spending!"
