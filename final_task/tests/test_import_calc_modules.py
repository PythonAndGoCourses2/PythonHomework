#!/usr/bin/env python3


import os
import sys
import unittest
import importlib.util
import math
import time

from pycalc import import_calc_modules
from tests import module_for_tests


class TestImportCalcModules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.append(os.getcwd())

    def test_check_module(self):
        tested_module = import_calc_modules._check_module

        with self.assertRaises(import_calc_modules.ImportCalculatorModulesError):
            tested_module("nonexistent_module")

        self.assertIsNotNone(tested_module("math"))
        self.assertIsNotNone(tested_module("time"))
        self.assertIsNotNone(tested_module("datetime"))

        self.assertIsNotNone(tested_module("module_for_tests"))

    def test_import_module_from_spec(self):
        tested_module = import_calc_modules._import_module_from_spec

        module_spec = importlib.util.find_spec("math")
        imported_module = tested_module(module_spec)
        self.assertAlmostEqual(imported_module.pi, math.pi)
        self.assertAlmostEqual(imported_module.sin(3.141592), math.sin(3.141592))

        module_spec = importlib.util.find_spec("time")
        imported_module = tested_module(module_spec)
        self.assertAlmostEqual(imported_module.timezone, time.timezone)
        self.assertAlmostEqual(imported_module.tzname, time.tzname)

        module_spec = importlib.util.find_spec("module_for_tests")
        imported_module = tested_module(module_spec)
        self.assertAlmostEqual(imported_module.pi, module_for_tests.pi)
        self.assertAlmostEqual(imported_module.time(), module_for_tests.time())
        self.assertAlmostEqual(imported_module.sin(10), module_for_tests.sin(10))

    def test_parse_module(self):
        tested_module = import_calc_modules._parse_module

        import math
        attrs_dir = tested_module(math)

        self.assertIs(attrs_dir["pi"], math.pi)
        self.assertIs(attrs_dir["tau"], math.tau)
        self.assertIs(attrs_dir["sin"], math.sin)
        self.assertIs(attrs_dir["log"], math.log)

        with self.assertRaises(KeyError):
            attrs_dir["__doc__"]
        with self.assertRaises(KeyError):
            attrs_dir["__name__"]

    def test_import_modules(self):
        tested_module = import_calc_modules.import_modules

        math_funcs, math_consts = tested_module(["time", "module_for_tests"])

        self.assertIs(math_consts["pi"], module_for_tests.pi)
        self.assertIs(math_consts["tau"], math.tau)
        self.assertIs(math_consts["timezone"], time.timezone)

        self.assertAlmostEqual(math_funcs["sin"](math.pi), module_for_tests.sin(math.pi))
        self.assertAlmostEqual(math_funcs["cos"](math.pi), math.cos(math.pi))
        self.assertAlmostEqual(math_funcs["time"](), module_for_tests.time())


if __name__ == "__main__":
    unittest.main()
