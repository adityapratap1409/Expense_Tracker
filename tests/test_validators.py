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


class TestValidateCategory(unittest.TestCase):

    def test_valid_category_sample_output(self):
         self.assertEqual(validate_category("food"),"Food")

    def test_blank_category(self):
        with self.assertRaises(ValidationError):
             validate_category(" ")

    def test_valid_Category_at_limit_accepted(self):
            self.assertEqual(validate_category("a"*30), "A"+"a"*29)
            
    def test_category_too_long_rejected(self):
        with self.assertRaises(ValidationError):
         validate_category("a" * 31)


class TestValidateDescription(unittest.TestCase):
    
    def test_valid_description_sample_output(self):
         self.assertEqual(validate_description("Outing with Friends"),"Outing with Friends")

    def test_blank_description(self):
        self.assertEqual(validate_description(" "),"-")

    def test_valid_description_at_limit_accepted(self):
        text = " ".join(["word"] * 50)
        self.assertEqual(validate_description(text), text)
            
    def test_description_too_long_rejected(self):
        with self.assertRaises(ValidationError):
         validate_description(" ".join(["word"] * 51))


if __name__ == "__main__":
    unittest.main()