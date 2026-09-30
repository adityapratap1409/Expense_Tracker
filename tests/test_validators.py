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
        # test valid float conversion
        res = val_amt("12.5")
        self.assertEqual(res, 12.5)

    def test_round_cents(self):
        # verify round to two decimals
        res = val_amt("12.346")
        self.assertEqual(res, 12.35)

    def test_zero_amt(self):
        # zero should fail validation
        failed = False
        try:
            val_amt("0")
        except ValidationError:
            failed = True
        self.assertTrue(failed == True)

    def test_neg_amt(self):
        # negative number not allowed
        failed = False
        try:
            val_amt("-5")
        except ValidationError:
            failed = True
        self.assertTrue(failed == True)

    def test_bad_text(self):
        # non-numeric string fails
        with self.assertRaises(ValidationError):
            val_amt("abc")

    def test_nan_val(self):
        # nan not allowed
        with self.assertRaises(ValidationError):
            val_amt("nan")


class TestValidateDate(unittest.TestCase):
    def test_valid_date(self):
        # standard date parsing
        res = valid_date("23-09-2026")
        self.assertEqual(res, "2026-09-23")

    def test_pad_date(self):
        # single digit day/month padded with 0
        res = valid_date("5-9-2026")
        self.assertEqual(res, "2026-09-05")

    def test_bad_date(self):
        # invalid calendar date fails
        failed = False
        try:
            valid_date("30-02-2026")
        except ValidationError:
            failed = True
        self.assertTrue(failed == True)

    def test_not_date(self):
        # random string fails
        with self.assertRaises(ValidationError):
            valid_date("hello")


class TestValidateCategory(unittest.TestCase):
    def test_val_cat(self):
        # title-cased output
        res = valCategory("food")
        self.assertEqual(res, "Food")

    def test_blank_cat(self):
        # empty category rejected
        failed = False
        try:
            valCategory(" ")
        except ValidationError:
            failed = True
        self.assertTrue(failed == True)

    def test_cat_limit(self):
        # 30 chars is allowed
        s_in = "a" * 30
        res = valCategory(s_in)
        self.assertEqual(res, "A" + "a" * 29)

    def test_long_cat(self):
        # over 30 chars rejected
        with self.assertRaises(ValidationError):
            valCategory("a" * 31)


class TestValidateDescription(unittest.TestCase):
    def test_val_desc(self):
        # normal description passes
        desc = "Outing with Friends"
        self.assertEqual(chk_desc(desc), desc)

    def test_blank_desc(self):
        # empty falls back to '-'
        res = chk_desc(" ")
        self.assertEqual(res, "-")

    def test_desc_limit(self):
        # 50 words max
        txt_val = " ".join(["word"] * 50)
        self.assertEqual(chk_desc(txt_val), txt_val)

    def test_long_desc(self):
        # 51 words should fail
        over_limit = " ".join(["word"] * 51)
        with self.assertRaises(ValidationError):
            chk_desc(over_limit)


if __name__ == "__main__":
    unittest.main()
