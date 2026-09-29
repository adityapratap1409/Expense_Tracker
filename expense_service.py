from datetime import datetime

from validators import (
    val_amt,
    valid_date,
    valCategory,
    chk_desc,
)


class NotFoundError(Exception):
    pass


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage

    def add_exp(self, amt, cat, desc, dt):
        # validate inputs before saving
        clean_amt = val_amt(amt)
        clean_cat = valCategory(cat)
        clean_desc = chk_desc(desc)

        # blank date? just use today
        if dt.strip():
            clean_dt = valid_date(dt)
        else:
            clean_dt = datetime.now().strftime("%Y-%m-%d")

        return self.storage.add_exp(clean_amt, clean_cat, clean_desc, clean_dt)

    def editExp(self, exp_id, amt, cat, desc, dt):
        old = self.storage.getExp(exp_id)
        if old is None:
            raise NotFoundError(f"No expense found with id {exp_id}.")

        # keep existing val if user left field blank
        new_amt = val_amt(amt) if amt.strip() else old["amount"]
        new_cat = valCategory(cat) if cat.strip() else old["category"]
        new_desc = chk_desc(desc) if desc.strip() else old["description"]
        new_dt = valid_date(dt) if dt.strip() else old["date"]

        self.storage.updExpense(exp_id, new_amt, new_cat, new_desc, new_dt)

    def del_exp(self, exp_id):
        deleted = self.storage.del_exp(exp_id)
        if deleted == 0:
            raise NotFoundError(f"No expense found with id {exp_id}.")

    def list_exp(self, mth=None):
        return self.storage.list_all(mth)

    def findByCat(self, cat):
        # normalize category before matching
        c = valCategory(cat)
        return [r for r in self.storage.list_all() if r["category"] == c]
