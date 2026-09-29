import unittest
from datetime import datetime
from storage import Storage
from expense_service import ExpenseService, NotFoundError
from validators import ValidationError


class TestExpenseService(unittest.TestCase):
    def setUp(self):
        self.db = Storage(":memory:")
        self.svc = ExpenseService(self.db)

    def tearDown(self):
        self.db.close()

    def test_blank_date(self):
        # blank date defaults to today
        eid = self.svc.add_exp("12.5", "Food", "Lunch", " ")
        r = self.db.getExp(eid)
        self.assertEqual(r["date"], datetime.now().strftime("%Y-%m-%d"))

    def test_bad_amt(self):
        # garbage text should raise
        with self.assertRaises(ValidationError):
            self.svc.add_exp("abc", "food", "lunch", " ")

    def test_edit_blank(self):
        # blank string keeps old value
        eid = self.svc.add_exp("10", "food", "lunch", "24-09-2026")
        self.svc.editExp(eid, "", "", "", "")
        r = self.db.getExp(eid)

        self.assertEqual(r["amount"], 10.0)
        self.assertEqual(r["category"], "Food")
        self.assertEqual(r["description"], "lunch")
        self.assertEqual(r["date"], "2026-09-24")

    def test_del_missing(self):
        # non-existent id raises NotFoundError
        with self.assertRaises(NotFoundError):
            self.svc.del_exp(999)


if __name__ == "__main__":
    unittest.main()
