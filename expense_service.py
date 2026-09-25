from datetime import datetime

from validators import (
    validate_amount,
    validate_category,
    validate_date,
    validate_description,
)


class NotFoundError(Exception):
    pass


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage

    def delete_expense(self, expense_id):
     deleted=self.storage.delete_expense(expense_id)
     if deleted==0:
        raise NotFoundError(f"No expense found with id {expense_id}. ")

    def edit_expense(self, expense_id, raw_amount, raw_category,raw_description, raw_date):
     old = self.storage.get_expense(expense_id)
     if old is None:
        raise NotFoundError(f"No expense found with id {expense_id}.")

     amount = validate_amount(raw_amount) if raw_amount.strip() else old["amount"]
     category = validate_category(raw_category) if raw_category.strip() else old["category"]
     description =validate_description(raw_description) if raw_description.strip() else old["description"]
     date =validate_date(raw_date) if raw_date.strip() else old["date"]

     self.storage.update_expense(expense_id, amount, category, description, date)
    
    def add_expense(self, raw_amount, raw_category, raw_description, raw_date):
        amount = validate_amount(raw_amount)
        category = validate_category(raw_category)  
        description = validate_description(raw_description)
        if raw_date.strip():
            date = validate_date(raw_date)
        else:
            date = datetime.now().strftime("%Y-%m-%d")
        return self.storage.add_expense(amount, category, description, date)