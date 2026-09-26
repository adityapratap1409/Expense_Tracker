from validators import validate_amount, validate_category

WARN_THRESHOLD = 0.8


class BudgetService:
    def __init__(self, storage):
        self.storage = storage

    def set_budget(self, raw_category, raw_limit):
        category = validate_category(raw_category)
        limit = validate_amount(raw_limit)
        self.storage.set_budget(category, limit)

    def get_budget_status(self, raw_category, month):
        category = validate_category(raw_category)
        budget_by_category = self.storage.get_budget(category)
        if budget_by_category is None:
            return None
        spent_this_month = self.storage.get_month_total(category, month)
        limit = budget_by_category["monthly_limit"]
        remaining = limit - spent_this_month
        percent_used = spent_this_month / limit
       
        return {
                   "limit": limit,
                   "spent": spent_this_month,
                   "remaining": remaining,
                   "percent_used": percent_used,
               }

    def check_alert(self, raw_category, month):
        category=validate_category(raw_category)
        budget_status=self.get_budget_status(raw_category, month)
        if budget_status is None:
            return None
        percent_used=budget_status["percent_used"]
        if percent_used >= 1.0:
            return f"{category} has exceeded its budget limit"
        elif percent_used>= WARN_THRESHOLD:
            return f"{category} is approaching its limit. Please spend responsibly"
        else:
            return f"{category} is yet to reach its limit. Happy spending!"