import unittest
from storage import Storage

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.s = Storage(":memory:")

    def tearDown(self):
        self.s.close()

    def test_add_and_get(self):
        id = self.s.add_exp(12.5, "Food", "Lunch", "2026-09-24")
        r = self.s.getExp(id)
        self.assertTrue(r != None)
        self.assertEqual(r["category"], "Food")
        self.assertEqual(r["amount"], 12.5)
        self.assertEqual(r["description"], "Lunch")

    def test_get_nonexistent(self):
        r = self.s.getExp(9999)
        self.assertTrue(r == None)

    def test_list_by_month(self):
        self.s.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.s.add_exp(20, "Food", "Dinner", "2026-08-01")
        rows = self.s.list_all("2026-09")
        self.assertEqual(len(rows), 1)

    def test_budget_upsert(self):
        self.s.setBudget("Food", 500)
        self.s.setBudget("Food", 800)
        b = self.s.all_budgets()
        # should only be 1 row after upsert
        self.assertEqual(len(b), 1)
        self.assertEqual(b[0]["monthly_limit"], 800)

    def test_month_total(self):
        self.s.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.s.add_exp(5, "Food", "Tea", "2026-09-25")
        self.s.add_exp(20, "Food", "Dinner", "2026-08-01")
        t = self.s.month_sum("Food", "2026-09")
        self.assertTrue(t == 15)

    def test_update(self):
        id = self.s.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.s.updExpense(id, 15, "Food", "Big lunch", "2026-09-24")
        r = self.s.getExp(id)
        self.assertTrue(r["amount"] == 15)
        self.assertEqual(r["description"], "Big lunch")

    def test_delete(self):
        id = self.s.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.s.del_exp(id)
        self.assertTrue(self.s.getExp(id) == None)
        # deleting nonexistent should return 0
        n = self.s.del_exp(9999)
        self.assertEqual(n, 0)


if __name__ == "__main__":
    unittest.main()
