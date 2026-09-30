import unittest
from storage import Storage
from budget_service import BudgetService


class TestBudgetService(unittest.TestCase):
    def setUp(self):
        # init in-memory database
        self.db = Storage(":memory:")
        self.svc = BudgetService(self.db)

    def tearDown(self):
        if self.db != None:
            self.db.close()

    def test_no_budget(self):
        # category without budget should return None
        res_msg = self.svc.chk_alert("rent", "2026-09")
        self.assertTrue(res_msg == None)

    def test_under(self):
        # under warning threshold
        self.svc.set_bgt("food", "100")
        self.db.add_exp(50, "Food", "Lunch", "2026-09-24")
        res_msg = self.svc.chk_alert("food", "2026-09")
        # should say happy spending
        self.assertTrue("Happy spending" in res_msg)

    def test_near(self):
        # approaching limit threshold (80%+)
        self.svc.set_bgt("food", "100")
        self.db.add_exp(85, "Food", "Groceries", "2026-09-24")
        res_msg = self.svc.chk_alert("food", "2026-09")
        self.assertTrue(res_msg.find("approaching") >= 0)

    def test_over(self):
        # exceeding 100% budget limit
        self.svc.set_bgt("food", "100")
        self.db.add_exp(120, "Food", "Dinner", "2026-09-24")
        res_msg = self.svc.chk_alert("food", "2026-09")
        self.assertTrue("exceeded" in res_msg)

    def test_status_vals(self):
        # verify calculated fields in getStatus
        self.svc.set_bgt("food", "100")
        self.db.add_exp(50, "Food", "Lunch", "2026-09-24")
        st_dict = self.svc.getStatus("food", "2026-09")
        self.assertTrue(st_dict != None)
        self.assertEqual(st_dict["percent_used"], 0.5)
        self.assertTrue(st_dict["limit"] == 100.0)
        self.assertTrue(st_dict["spent"] == 50.0)
        self.assertTrue(st_dict["remaining"] == 50.0)


if __name__ == "__main__":
    unittest.main()
