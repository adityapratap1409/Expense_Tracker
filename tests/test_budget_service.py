import unittest
from storage import Storage
from expense_service import ExpenseService, NotFoundError
from validators import ValidationError
from budget_service import BudgetService

class TestBudgetService(unittest.TestCase):
    def setUp(self):
        self.storage = Storage(":memory:")
        self.service = BudgetService(self.storage)

    def tearDown(self):
        self.storage.close()

    def test_check_alert_with_no_budget_returns_none(self):
        result = self.service.check_alert("rent", "2026-09")
        self.assertIsNone(result)
    def test_check_alert_under_threshold_returns_none(self):
     self.service.set_budget("food", "100")
     self.storage.add_expense(50, "Food", "Lunch", "2026-09-24")
     result = self.service.check_alert("food", "2026-09")
     self.assertIn("Happy spending", result)

    def test_check_alert_near_limit_returns_warning(self):
        self.service.set_budget("food", "100")
        self.storage.add_expense(85, "Food", "Groceries", "2026-09-24")
        result = self.service.check_alert("food", "2026-09")
        self.assertIn("approaching", result)

    def test_check_alert_over_limit_returns_exceeded_message(self):
        self.service.set_budget("food", "100")
        self.storage.add_expense(120, "Food", "Dinner", "2026-09-24")
        result = self.service.check_alert("food", "2026-09")
        self.assertIn("exceeded", result)

    def test_get_budget_status_returns_correct_numbers(self):
        self.service.set_budget("food", "100")
        self.storage.add_expense(50, "Food", "Lunch", "2026-09-24")
        status = self.service.get_budget_status("food", "2026-09")
        self.assertEqual(status["percent_used"], 0.5)


if __name__ == "__main__":
    unittest.main()