import unittest

from validators import (
    ValidationError,
    val_amt,
    valid_date,
    valCategory,
    chk_desc,
)


class TestValidateAmount(unittest.TestCase):
    def test_val_amt(self):
        self.assertEqual(val_amt("12.5"), 12.5)

    def test_round_cents(self):
        self.assertEqual(val_amt("12.346"), 12.35)

    def test_zero_amt(self):
        with self.assertRaises(ValidationError):
            val_amt("0")

    def test_neg_amt(self):
        with self.assertRaises(ValidationError):
            val_amt("-5")

    def test_bad_text(self):
        with self.assertRaises(ValidationError):
            val_amt("abc")

    def test_nan_val(self):
        with self.assertRaises(ValidationError):
            val_amt("nan")


class TestValidateDate(unittest.TestCase):
    def test_valid_date(self):
        self.assertEqual(valid_date("23-09-2026"), "2026-09-23")

    def test_pad_date(self):
        # single digit day/month padded with 0
        self.assertEqual(valid_date("5-9-2026"), "2026-09-05")

    def test_bad_date(self):
        with self.assertRaises(ValidationError):
            valid_date("30-02-2026")

    def test_not_date(self):
        with self.assertRaises(ValidationError):
            valid_date("hello")


class TestValidateCategory(unittest.TestCase):
    def test_val_cat(self):
        self.assertEqual(valCategory("food"), "Food")

    def test_blank_cat(self):
        with self.assertRaises(ValidationError):
            valCategory(" ")

    def test_cat_limit(self):
        self.assertEqual(valCategory("a" * 30), "A" + "a" * 29)

    def test_long_cat(self):
        with self.assertRaises(ValidationError):
            valCategory("a" * 31)


class TestValidateDescription(unittest.TestCase):
    def test_val_desc(self):
        self.assertEqual(chk_desc("Outing with Friends"), "Outing with Friends")

    def test_blank_desc(self):
        # empty falls back to '-'
        self.assertEqual(chk_desc(" "), "-")

    def test_desc_limit(self):
        txt = " ".join(["word"] * 50)
        self.assertEqual(chk_desc(txt), txt)

    def test_long_desc(self):
        with self.assertRaises(ValidationError):
            chk_desc(" ".join(["word"] * 51))


if __name__ == "__main__":
    unittest.main()
