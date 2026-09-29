from datetime import datetime
from validators import val_amt, valid_date, valCategory, chk_desc

class NotFoundError(Exception):
    pass

class ExpenseService:
    def __init__(self, storage):
        self.storage = storage

    def add_exp(self, amt, cat, desc, dt):
        clean_a = val_amt(amt)
        clean_c = valCategory(cat)
        clean_d = chk_desc(desc)

        # fallback to current date if user gave blank
        if len(dt.strip()) > 0:
            clean_dt = valid_date(dt)
        else:
            clean_dt = datetime.now().strftime("%Y-%m-%d")

        return self.storage.add_exp(clean_a, clean_c, clean_d, clean_dt)

    def editExp(self, exp_id, amt, cat, desc, dt):
        old = self.storage.getExp(exp_id)
        if old is not None:
            # check each field, keep old value if blank
            if len(amt.strip()) > 0:
                new_a = val_amt(amt)
            else:
                new_a = old["amount"]

            if len(cat.strip()) > 0:
                new_c = valCategory(cat)
            else:
                new_c = old["category"]

            if len(desc.strip()) > 0:
                new_d = chk_desc(desc)
            else:
                new_d = old["description"]

            if len(dt.strip()) > 0:
                new_dt = valid_date(dt)
            else:
                new_dt = old["date"]

            self.storage.updExpense(exp_id, new_a, new_c, new_d, new_dt)
        else:
            raise NotFoundError("No expense found with id %s." % exp_id)

    def del_exp(self, exp_id):
        deleted = self.storage.del_exp(exp_id)
        if deleted == 0:
            raise NotFoundError("No expense found with id %s." % exp_id)

    def list_exp(self, mth=None):
        return self.storage.list_all(mth)

    def findByCat(self, cat):
        c = valCategory(cat)
        all_rows = self.storage.list_all()
        res = []
        for r in all_rows:
            if r["category"] == c:
                res.append(r)
        return res
