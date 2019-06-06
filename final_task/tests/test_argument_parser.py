#!/usr/bin/env python3


import sys
import unittest

from pycalc import argument_parser


class TestArgumentParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.argv_static = sys.argv.copy()

    def test_parse_expression(self):
        sys.argv[:] = self.argv_static
        sys.argv.append("10.0*-50+sin(2*pi)")
        expression, arg_modules = argument_parser.parse()
        self.assertEqual(expression, "10.0*-50+sin(2*pi)")
        self.assertEqual(arg_modules, [])

    def test_parse_expression_and_modules(self):
        sys.argv[:] = self.argv_static
        sys.argv.extend(("11+62/2", "-m", "time"))
        expression, arg_modules = argument_parser.parse()
        self.assertEqual(expression, "11+62/2")
        self.assertEqual(arg_modules, ["time"])

        sys.argv[:] = self.argv_static
        sys.argv.extend("sin(pi)+1 -m time random test_lib".split())
        expression, arg_modules = argument_parser.parse()
        self.assertEqual(expression, "sin(pi)+1")
        self.assertEqual(arg_modules, ["time", "random", "test_lib"])

        sys.argv[:] = self.argv_static
        sys.argv.extend(("21 +21+ sin(pi )", "--use-modules", "random", "test_lib"))
        expression, arg_modules = argument_parser.parse()
        self.assertEqual(expression, "21 +21+ sin(pi )")
        self.assertEqual(arg_modules, ["random", "test_lib"])


if __name__ == "__main__":
    unittest.main()
