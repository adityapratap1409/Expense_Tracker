import unittest

from storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = Storage(":memory:")

    def tearDown(self):
        self.storage.close()

    def test_add_then_get_expense(self):
        new_id = self.storage.add_expense(12.5, "Food", "Lunch", "2026-09-24")
        row = self.storage.get_expense(new_id)
        self.assertEqual(row["category"], "Food")
        self.assertEqual(row["amount"], 12.5)

    def test_get_missing_expense_returns_none(self):
        self.assertIsNone(self.storage.get_expense(999))


if __name__ == "__main__":
    unittest.main()