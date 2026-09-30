from validators import val_amt, valCategory

WARN_PCT = 0.8
# ALERT_EMAIL = False  # maybe add email alerts later?

class BudgetService:
    def __init__(self, storage):
        self.storage = storage

    def set_bgt(self, cat, lim):
        # sanitize category and amount limit
        c_val = valCategory(cat)
        l_val = val_amt(lim)
        self.storage.setBudget(c_val, l_val)

    def getStatus(self, cat, mth):
        # check category budget status
        c_val = valCategory(cat)
        bgt_row = self.storage.get_bgt(c_val)
        if bgt_row == None:
            return None
        
        # compute limits and spent totals
        lim = float(bgt_row["monthly_limit"])
        spent = self.storage.month_sum(c_val, mth)
        if spent == None:
            spent = 0.0
        else:
            spent = float(spent)

        rem = lim - spent
        pct = 0.0
        if lim > 0:
            pct = spent / lim
        
        # assemble status map
        out_dict = {}
        out_dict["limit"] = lim
        out_dict["spent"] = spent
        out_dict["remaining"] = rem
        out_dict["percent_used"] = pct
        return out_dict

    def chk_alert(self, cat, mth):
        c_val = valCategory(cat)
        stat = self.getStatus(cat, mth)
        if stat == None:
            # no budget found
            return None
        
        pct = stat["percent_used"]
        # check warning thresholds
        if pct >= 1.0:
            msg = "%s has exceeded its budget limit" % c_val
        elif pct >= WARN_PCT:
            msg = "%s is approaching its limit. Please spend responsibly" % c_val
        else:
            msg = "%s is yet to reach its limit. Happy spending!" % c_val
        return msg
