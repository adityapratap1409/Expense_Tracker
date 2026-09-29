import unittest
from storage import Storage
from budget_service import BudgetService


class TestBudgetService(unittest.TestCase):
    def setUp(self):
        self.db = Storage(":memory:")
        self.svc = BudgetService(self.db)

    def tearDown(self):
        self.db.close()

    def test_no_bgt_alert(self):
        # no budget set returns None
        res = self.svc.chk_alert("rent", "2026-09")
        self.assertIsNone(res)

    def test_under_threshold(self):
        # 50/100 -> well under 80%
        self.svc.set_bgt("food", "100")
        self.db.add_exp(50, "Food", "Lunch", "2026-09-24")
        res = self.svc.chk_alert("food", "2026-09")
        self.assertIn("Happy spending", res)

    def test_near_limit(self):
        # 85/100 -> >=80% warning
        self.svc.set_bgt("food", "100")
        self.db.add_exp(85, "Food", "Groceries", "2026-09-24")
        res = self.svc.chk_alert("food", "2026-09")
        self.assertIn("approaching", res)

    def test_over_limit(self):
        # 120/100 -> exceeded
        self.svc.set_bgt("food", "100")
        self.db.add_exp(120, "Food", "Dinner", "2026-09-24")
        res = self.svc.chk_alert("food", "2026-09")
        self.assertIn("exceeded", res)

    def test_status_numbers(self):
        # check stats dict calculations
        self.svc.set_bgt("food", "100")
        self.db.add_exp(50, "Food", "Lunch", "2026-09-24")
        stat = self.svc.getStatus("food", "2026-09")

        self.assertEqual(stat["percent_used"], 0.5)
        self.assertEqual(stat["limit"], 100.0)
        self.assertEqual(stat["spent"], 50.0)
        self.assertEqual(stat["remaining"], 50.0)


if __name__ == "__main__":
    unittest.main()
