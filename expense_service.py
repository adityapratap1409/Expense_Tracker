from datetime import datetime
from validators import val_amt, valid_date, valCategory, chk_desc

class NotFoundError(Exception):
    pass


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage
        # self.cache = {}  # maybe add caching later

    def add_exp(self, amt, cat, desc, dt):
        a = val_amt(amt)
        c = valCategory(cat)
        d = chk_desc(desc)
        dt2 = dt.strip()
        if dt2 != "":
            dt_clean = valid_date(dt)
        else:
            dt_clean = datetime.now().strftime("%Y-%m-%d")
        eid = self.storage.add_exp(a, c, d, dt_clean)
        return eid

    def editExp(self, eid, amt, cat, desc, dt):
        # get existing record first
        old = self.storage.getExp(eid)
        if old == None:
            raise NotFoundError("No expense found with id %s." % str(eid))

        # update amount
        tmp = amt.strip()
        if tmp != "":
            new_amt = val_amt(amt)
        else:
            new_amt = old["amount"]

        # update category
        tmp = cat.strip()
        if tmp != "":
            new_cat = valCategory(cat)
        else:
            new_cat = old["category"]

        # update desc
        tmp = desc.strip()
        if tmp != "":
            new_desc = chk_desc(desc)
        else:
            new_desc = old["description"]

        # update date
        tmp = dt.strip()
        if tmp != "":
            new_dt = valid_date(dt)
        else:
            new_dt = old["date"]

        self.storage.updExpense(eid, new_amt, new_cat, new_desc, new_dt)
        return True

    def del_exp(self, eid):
        n = self.storage.del_exp(eid)
        if n == 0:
            raise NotFoundError("No expense found with id %s." % str(eid))
        return True

    def list_exp(self, mth=None):
        data = self.storage.list_all(mth)
        return data

    def findByCat(self, cat):
        c = valCategory(cat)
        alldata = self.storage.list_all()
        # filter manually
        out = []
        i = 0
        while i < len(alldata):
            r = alldata[i]
            if r["category"] == c:
                out.append(r)
            i = i + 1
        return out
