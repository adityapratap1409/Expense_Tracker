import unittest
from datetime import datetime
from storage import Storage
from expense_service import ExpenseService, NotFoundError
from validators import ValidationError


class TestExpenseService(unittest.TestCase):
    def setUp(self):
        # setup in-memory test db
        self.db = Storage(":memory:")
        self.svc = ExpenseService(self.db)

    def tearDown(self):
        # cleanup db connection
        if self.db != None:
            self.db.close()

    def test_add_blank_date(self):
        # blank date input should default to today's date
        e_id = self.svc.add_exp("12.5", "Food", "Lunch", " ")
        res = self.db.getExp(e_id)
        curr_dt = datetime.now().strftime("%Y-%m-%d")
        self.assertTrue(res != None)
        self.assertTrue(res["date"] == curr_dt)

    def test_add_bad_amount(self):
        # invalid amount should raise ValidationError
        err_caught = False
        try:
            self.svc.add_exp("abc", "food", "lunch", " ")
        except ValidationError:
            err_caught = True
        self.assertTrue(err_caught == True)

    def test_edit_keeps_old(self):
        # passing blanks should keep previous values
        e_id = self.svc.add_exp("10", "food", "lunch", "24-09-2026")
        self.svc.editExp(e_id, "", "", "", "")
        row = self.db.getExp(e_id)
        self.assertTrue(row != None)
        self.assertEqual(row["amount"], 10.0)
        self.assertTrue(row["category"] == "Food")
        self.assertEqual(row["description"], "lunch")
        self.assertEqual(row["date"], "2026-09-24")

    def test_delete_nonexistent(self):
        # deleting missing id should trigger NotFoundError
        got_err = False
        try:
            self.svc.del_exp(999)
        except NotFoundError:
            got_err = True
        self.assertTrue(got_err == True)


if __name__ == "__main__":
    unittest.main()
