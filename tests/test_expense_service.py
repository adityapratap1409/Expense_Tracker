import unittest
from datetime import datetime
from storage import Storage
from expense_service import ExpenseService, NotFoundError
from validators import ValidationError


class TestExpenseService(unittest.TestCase):
    def setUp(self):
        self.storage = Storage(":memory:")
        self.service = ExpenseService(self.storage)

    def tearDown(self):
        self.storage.close()    

    def test_add_expense_with_blank_date_uses_today(self):
        new_id = self.service.add_expense("12.5", "Food", "Lunch", " ")
        row = self.storage.get_expense(new_id)
        self.assertEqual(row["date"], datetime.now().strftime("%Y-%m-%d"))

    def test_add_expense_with_bad_amount_raises(self):
        with self.assertRaises(ValidationError):
            self.service.add_expense("abc", "food", "lunch", " ")

    def test_edit_expense_blank_fields_keep_old_values(self):
     new_id = self.service.add_expense("10", "food", "lunch", "24-09-2026")
     self.service.edit_expense(new_id, "", "", "", "")
     row = self.storage.get_expense(new_id)
     self.assertEqual(row["amount"], 10.0)
     self.assertEqual(row["category"], "Food")
     self.assertEqual(row["description"], "lunch")
     self.assertEqual(row["date"], "2026-09-24")

    def test_delete_missing_expense_raises_not_found(self):
       with self.assertRaises(NotFoundError): 
           self.service.delete_expense(999)


if __name__ == "__main__":
    unittest.main()