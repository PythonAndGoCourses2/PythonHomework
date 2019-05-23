import pycalc.main as mn
import unittest
import math as m


class TestFunctions(unittest.TestCase):

    def test_error(self):
        self.assertEqual(mn.pycalc(''), "ERROR: empty expression")
        self.assertEqual(mn.pycalc('123-'), "ERROR: no number after operator")
        self.assertEqual(mn.pycalc('123-()'), "ERROR: empty brackets")
        self.assertEqual(mn.pycalc('123-(-)'), "ERROR: no number after operator")
        self.assertEqual(mn.pycalc('func()'), "ERROR: function does not exist")
        self.assertEqual(mn.pycalc('pow(12, 12, 3)'), "ERROR: wrong amount of arguments for pow(..)")
        self.assertEqual(mn.pycalc('123+23*(12 - 23 + 12))'), "ERROR: brackets are not paired")
        self.assertEqual(mn.pycalc('123+23*(12 - 23(12))'), "ERROR: no sign or function before brackets")

    def test_solve_equality(self):
        pass

    def test_add_math_objects(self):
        pass

    def test_multiply(self):
        pass

    def test_get_degree(self):
        pass

    def test_number_sign(self):
        pass

    def test_search_float(self):
        pass

    def test_skip_space(self):
        pass

    def test_get_bracket(self):
        pass

    def test_get_func_arguments(self):
        pass
