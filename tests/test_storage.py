import unittest
from storage import Storage

class TestStorage(unittest.TestCase):
    def setUp(self):
        # in-memory db setup
        self.s = Storage(":memory:")

    def tearDown(self):
        if self.s != None:
            self.s.close()

    def test_add_and_get(self):
        # insert row and fetch back
        e_id = self.s.add_exp(12.5, "Food", "Lunch", "2026-09-24")
        r_row = self.s.getExp(e_id)
        self.assertTrue(r_row != None)
        self.assertEqual(r_row["category"], "Food")
        self.assertEqual(r_row["amount"], 12.5)
        self.assertEqual(r_row["description"], "Lunch")

    def test_get_nonexistent(self):
        # nonexistent id returns None
        r_row = self.s.getExp(9999)
        self.assertTrue(r_row == None)

    def test_list_by_month(self):
        # filter records by yyyy-mm
        self.s.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.s.add_exp(20, "Food", "Dinner", "2026-08-01")
        rows_list = self.s.list_all("2026-09")
        self.assertEqual(len(rows_list), 1)

    def test_budget_upsert(self):
        # setting limit again should update existing
        self.s.setBudget("Food", 500)
        self.s.setBudget("Food", 800)
        b_list = self.s.all_budgets()
        # should only have 1 row after conflict update
        self.assertEqual(len(b_list), 1)
        self.assertEqual(b_list[0]["monthly_limit"], 800)

    def test_month_total(self):
        # aggregate monthly sum for category
        self.s.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.s.add_exp(5, "Food", "Tea", "2026-09-25")
        self.s.add_exp(20, "Food", "Dinner", "2026-08-01")
        t_sum = self.s.month_sum("Food", "2026-09")
        self.assertTrue(t_sum == 15)

    def test_update(self):
        # update fields of existing expense
        e_id = self.s.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.s.updExpense(e_id, 15, "Food", "Big lunch", "2026-09-24")
        r_row = self.s.getExp(e_id)
        self.assertTrue(r_row != None)
        self.assertTrue(r_row["amount"] == 15)
        self.assertEqual(r_row["description"], "Big lunch")

    def test_delete(self):
        # delete record by id
        e_id = self.s.add_exp(10, "Food", "Lunch", "2026-09-24")
        self.s.del_exp(e_id)
        self.assertTrue(self.s.getExp(e_id) == None)
        # deleting nonexistent returns 0
        cnt_del = self.s.del_exp(9999)
        self.assertEqual(cnt_del, 0)


if __name__ == "__main__":
    unittest.main()
