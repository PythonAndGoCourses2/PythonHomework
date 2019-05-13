import unittest
from .parser import parse_query


class TestParserFunction(unittest.TestCase):
    def test_parse_query(self):
        with self.subTest("return currect value"):
            import sys

            sys.argv = ['pycalc.py', 'time()/60', '-m', 'time', 'os', 'math']
            args = parse_query()
            self.assertEqual(args.expr, 'time()/60')
            self.assertEqual(args.modules, ['time', 'os', 'math'])


if __name__ == '__main__':
    unittest.main()
