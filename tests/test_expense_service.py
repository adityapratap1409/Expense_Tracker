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

    def test_add_blank_date(self):
        id = self.svc.add_exp("12.5", "Food", "Lunch", " ")
        r = self.db.getExp(id)
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertTrue(r["date"] == today)

    def test_add_bad_amount(self):
        ok = False
        try:
            self.svc.add_exp("abc", "food", "lunch", " ")
        except ValidationError:
            ok = True
        self.assertTrue(ok)

    def test_edit_keeps_old(self):
        id = self.svc.add_exp("10", "food", "lunch", "24-09-2026")
        self.svc.editExp(id, "", "", "", "")
        r = self.db.getExp(id)
        self.assertEqual(r["amount"], 10.0)
        self.assertTrue(r["category"] == "Food")
        self.assertEqual(r["description"], "lunch")
        self.assertEqual(r["date"], "2026-09-24")

    def test_delete_nonexistent(self):
        gotError = False
        try:
            self.svc.del_exp(999)
        except NotFoundError:
            gotError = True
        self.assertTrue(gotError == True)

if __name__ == "__main__":
    unittest.main()
