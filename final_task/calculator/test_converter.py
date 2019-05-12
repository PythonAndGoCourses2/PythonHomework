import unittest
from converter import convert_answer


class TestConverterFunction(unittest.TestCase):
    def test_convert_answer(self):
        with self.subTest("returns correct answer"):
            self.assertEqual(convert_answer('-1', False), '-1')
            self.assertEqual(convert_answer('0', False), '0')
            self.assertEqual(convert_answer('-1', True), 'True')
            self.assertEqual(convert_answer('0', True), 'False')


if __name__ == '__main__':
    unittest.main()
