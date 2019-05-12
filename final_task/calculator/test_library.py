import unittest
from library import Library


class TestLibraryClass(unittest.TestCase):
    def test__init__(self):
        with self.subTest("contains around and abs functon by default"):
            lib = Library()

            self.assertTrue('round' in lib)
            self.assertTrue('abs' in lib)

        with self.subTest("can get module names and adds their variables to your own dictionary"):
            lib = Library('math', 'os', 'time')

            self.assertTrue('path' in lib)
            self.assertTrue('clock' in lib)
            self.assertTrue('pi' in lib)

    def test_update(self):
        with self.subTest("get module names and adds their variables to your own dictionary"):
            lib = Library()
            self.assertFalse('path' in lib)

            lib.update('os')
            self.assertTrue('path' in lib)

            lib.update('sys', 'time')
            self.assertTrue('stdin' in lib)
            self.assertTrue('clock' in lib)

        with self.subTest("raises error if veriable is not found"):
            self.assertRaises(ModuleNotFoundError, lambda: lib.update('bad_module'))
            self.assertRaises(ModuleNotFoundError, lambda: lib.update('new_math'))


if __name__ == '__main__':
    unittest.main()
