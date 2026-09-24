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


if __name__ == "__main__":
    unittest.main()