import unittest

from validators import (
    ValidationError,
    validate_amount,
    validate_date,
    validate_category,
    validate_description,
)


class TestValidateAmount(unittest.TestCase):
    def test_valid_amount(self):
        self.assertEqual(validate_amount("12.5"), 12.5)

    def test_rounds_to_two_decimals(self):
        self.assertEqual(validate_amount("12.346"), 12.35)

    def test_zero_rejected(self):
        with self.assertRaises(ValidationError):
            validate_amount("0")
            
    def test_negative_rejected(self):
        with self.assertRaises(ValidationError):
            validate_amount("-5")
        
    def test_text_rejected(self):
        with self.assertRaises(ValidationError):
            validate_amount("abc")
        
    def test_nan_rejected(self):
        with self.assertRaises(ValidationError):
            validate_amount("nan")

class TestValidateDate(unittest.TestCase):
    def test_valid_date_is_converted(self):
        self.assertEqual(validate_date("23-09-2026"), "2026-09-23")
        
    def test_single_digit_date_is_padded(self):
        self.assertEqual(validate_date("5-9-2026"), "2026-09-05")

    def test_impossible_date_rejected(self):
         with self.assertRaises(ValidationError):
            validate_date("30-02-2026")

    def test_text_rejected(self):
        with self.assertRaises(ValidationError):
            validate_date("hello")
if __name__ == "__main__":
    unittest.main()