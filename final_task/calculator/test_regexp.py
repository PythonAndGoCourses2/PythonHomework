import unittest
from regexp import has_comparator, has_non_zero_fraction_part

class TestRegexpFunction(unittest.TestCase):
    def test_has_comparator(self):
        with self.subTest("returns correct answer"):
            self.assertFalse(has_comparator('1'))
            self.assertFalse(has_comparator('1+1', ))
            self.assertTrue(has_comparator('1==1'))
            self.assertTrue(has_comparator('1>=1'))

    def test_has_non_zero_fraction_part(self):
        with self.subTest("returns correct answer"):
            self.assertFalse(has_non_zero_fraction_part('1'))
            self.assertFalse(has_non_zero_fraction_part('1.0'))
            self.assertTrue(has_non_zero_fraction_part('1.9'))
            self.assertTrue(has_non_zero_fraction_part('1.09'))
            self.assertTrue(has_non_zero_fraction_part('1.00000000000001'))

if __name__ == '__main__':
    unittest.main()
