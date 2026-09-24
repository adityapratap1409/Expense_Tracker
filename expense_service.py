from datetime import datetime

from validators import (
    validate_amount,
    validate_category,
    validate_date,
    validate_description,
)


class ExpenseService:
    def __init__(self, storage):
        self.storage = storage

    def add_expense(self, raw_amount, raw_category, raw_description, raw_date):
        amount = validate_amount(raw_amount)
        category = validate_category(raw_category)  
        description = validate_description(raw_description)
        if raw_date.strip():
            date = validate_date(raw_date)
        else:
            date = datetime.now().strftime("%Y-%m-%d")
        return self.storage.add_expense(amount, category, description, date)