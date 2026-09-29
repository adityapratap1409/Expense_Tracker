import unittest
from storage import Storage
from budget_service import BudgetService


class TestBudgetService(unittest.TestCase):
    def setUp(self):
        self.db = Storage(":memory:")
        self.svc = BudgetService(self.db)

    def tearDown(self):
        self.db.close()

    def test_no_budget(self):
        r = self.svc.chk_alert("rent", "2026-09")
        self.assertTrue(r == None)

    def test_under(self):
        self.svc.set_bgt("food", "100")
        self.db.add_exp(50, "Food", "Lunch", "2026-09-24")
        r = self.svc.chk_alert("food", "2026-09")
        # should say happy spending
        self.assertTrue("Happy spending" in r)

    def test_near(self):
        self.svc.set_bgt("food", "100")
        self.db.add_exp(85, "Food", "Groceries", "2026-09-24")
        r = self.svc.chk_alert("food", "2026-09")
        self.assertTrue(r.find("approaching") >= 0)

    def test_over(self):
        self.svc.set_bgt("food", "100")
        self.db.add_exp(120, "Food", "Dinner", "2026-09-24")
        r = self.svc.chk_alert("food", "2026-09")
        self.assertTrue("exceeded" in r)

    def test_status_vals(self):
        self.svc.set_bgt("food", "100")
        self.db.add_exp(50, "Food", "Lunch", "2026-09-24")
        s = self.svc.getStatus("food", "2026-09")
        self.assertTrue(s != None)
        self.assertEqual(s["percent_used"], 0.5)
        self.assertTrue(s["limit"] == 100.0)
        self.assertTrue(s["spent"] == 50.0)
        self.assertTrue(s["remaining"] == 50.0)


if __name__ == "__main__":
    unittest.main()
