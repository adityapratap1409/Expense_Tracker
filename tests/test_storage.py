import unittest

from storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = Storage(":memory:")

    def tearDown(self):
        self.storage.close()

    def test_add_then_get_expense(self):
        new_id = self.storage.add_expense(12.5, "Food", "Lunch", "2026-09-24")
        row = self.storage.get_expense(new_id)
        self.assertEqual(row["category"], "Food")
        self.assertEqual(row["amount"], 12.5)

    def test_get_missing_expense_returns_none(self):
        self.assertIsNone(self.storage.get_expense(999))
    
    def test_list_expenses_filters_by_month(self):
       self.storage.add_expense(10, "Food", "Lunch", "2026-09-24")
       self.storage.add_expense(20, "Food", "Dinner", "2026-08-01")
       rows = self.storage.list_expenses("2026-09")
       self.assertEqual(len(rows), 1)
    def test_set_budget_twice_keeps_one_row(self):
        self.storage.set_budget("Food", 500)
        self.storage.set_budget("Food", 800)
        budgets = self.storage.list_budgets()
        self.assertEqual(len(budgets), 1)
        self.assertEqual(budgets[0]["monthly_limit"], 800)

    def test_month_total_sums_only_that_month(self):
        self.storage.add_expense(10, "Food", "Lunch", "2026-09-24")
        self.storage.add_expense(5, "Food", "Tea", "2026-09-25")
        self.storage.add_expense(20, "Food", "Dinner", "2026-08-01")
        total = self.storage.get_month_total("Food", "2026-09")
        self.assertEqual(total,15)


    def test_update_expense_changes_row(self):
     new_id = self.storage.add_expense(10, "Food", "Lunch", "2026-09-24")
     self.storage.update_expense(new_id, 15, "Food", "Big lunch", "2026-09-24")
     row = self.storage.get_expense(new_id)
     self.assertEqual(row["amount"], 15)


    def test_delete_expense(self):
     new_id = self.storage.add_expense(10, "Food", "Lunch", "2026-09-24")
     self.storage.delete_expense(new_id)
     self.assertIsNone(self.storage.get_expense(new_id))
     self.assertEqual(self.storage.delete_expense(999), 0)


if __name__ == "__main__":
    unittest.main()