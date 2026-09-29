import unittest
from storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        # in-memory db so tests don't mess up real data
        self.db = Storage(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_get(self):
        eid = self.db.add_exp(12.5, "Food", "Lunch", "2026-09-24")
        row = self.db.getExp(eid)

        self.assertIsNotNone(row)
        self.assertEqual(row["category"], "Food")
        self.assertEqual(row["amount"], 12.5)
        self.assertEqual(row["description"], "Lunch")
        self.assertEqual(row["date"], "2026-09-24")

    def test_missing_exp(self):
        # missing id should return None
        self.assertIsNone(self.db.getExp(999))

    def test_list_month(self):
        # only return rows matching YYYY-MM
        self.db.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.db.add_exp(20, "Food", "Dinner", "2026-08-01")

        rows = self.db.list_all("2026-09")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["description"], "Lunch")

    def test_set_bgt_upsert(self):
        # setting twice should overwrite, not duplicate
        self.db.setBudget("Food", 500)
        self.db.setBudget("Food", 800)

        bgts = self.db.all_budgets()
        self.assertEqual(len(bgts), 1)
        self.assertEqual(bgts[0]["monthly_limit"], 800)

    def test_month_sum(self):
        # sum only within requested month
        self.db.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.db.add_exp(5, "Food", "Tea", "2026-09-25")
        self.db.add_exp(20, "Food", "Dinner", "2026-08-01")

        tot = self.db.month_sum("Food", "2026-09")
        self.assertEqual(tot, 15)

    def test_upd_exp(self):
        eid = self.db.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.db.updExpense(eid, 15, "Food", "Big lunch", "2026-09-24")

        row = self.db.getExp(eid)
        self.assertEqual(row["amount"], 15)
        self.assertEqual(row["description"], "Big lunch")

    def test_del_exp(self):
        eid = self.db.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.db.del_exp(eid)

        self.assertIsNone(self.db.getExp(eid))
        self.assertEqual(self.db.del_exp(999), 0)


if __name__ == "__main__":
    unittest.main()
