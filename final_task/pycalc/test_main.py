import pycalc.main as mn
import unittest
from pycalc.check_mistakes import check_mistakes
import math as m


class TestFunctions(unittest.TestCase):

    def test_check_mistakes(self):
        self.assertEqual(check_mistakes([]), "ERROR: empty expression")
        self.assertEqual(check_mistakes(['123', '-']), "ERROR: no number after operator")
        self.assertEqual(check_mistakes(['123', '-', '(', ')']), "ERROR: empty brackets")
        self.assertEqual(check_mistakes(['123', '-', '(', '-', ')']), "ERROR: no number after operator")
        self.assertEqual(check_mistakes(['func', '(', ')']), "ERROR: function does not exist")
        self.assertEqual(check_mistakes(['123', '+', '23', '*', '(', '12', '-', '23', '+', '12', ')', ')']),
                         "ERROR: brackets are not paired")
        self.assertEqual(check_mistakes(['123', '+', '23', '*', '(', '12', '-', '23', '(', '12', ')', ')']),
                         "ERROR: no sign or function before brackets")
        self.assertEqual(check_mistakes(['123', '+', '23', '/', ' ', '/', '(', '12', '-', '3', ')']),
                         "ERROR: duplicate multiply or div sign")

    def test_get_args(self):
        self.assertEqual(mn.get_args(['12', ',', 'pi', ',', '12', '+', '32', ',', '43', '*', '2']), [12, m.pi, 44, 86])

    def test_separate(self):
        self.assertEqual(mn.separate(''), [])
        self.assertEqual(mn.separate("123-5"), ['123', '-', '5'])
        self.assertEqual(mn.separate("123-(7)"), ['123', '-', '(', '7', ')'])
        self.assertEqual(mn.separate("12-(-)"), ['12', '-', '(', '-', ')'])
        self.assertEqual(mn.separate("func()"), ['func', '(', ')'])
        self.assertEqual(mn.separate("123+23*(12-23+12)"),
                         ['123', '+', '23', '*', '(', '12', '-', '23', '+', '12', ')'])
        self.assertEqual(mn.separate("123+23*(12-23(12))"),
                         ['123', '+', '23', '*', '(', '12', '-', '23', '(', '12', ')', ')'])
        self.assertEqual(mn.separate("123+23/ /(12^3)"),
                         ['123', '+', '23', '/', '/', '(', '12', '^', '3', ')'])
        self.assertEqual(mn.separate("log10(123) + --- 23"),
                         ['log10', '(', '123', ')', '+', '---', '23'])

    def test_calc(self):
        self.assertEqual(mn.calc(["10"]), '10.0')
        self.assertEqual(mn.calc(['123', '-', '10']), '113.0')
        self.assertEqual(mn.calc(['123', '-', '(', '10', '+', '7', ')']), '106.0')
        self.assertEqual(mn.calc(['2', '^', '(', '5', '-', '7', ')']), '0.25')
        self.assertEqual(mn.calc(['123', '/', '23', '*', '(', '12', '-', '23', '^', '2', ')']),
                         "-2764.8260869565215")
        self.assertEqual(mn.calc(['15', '+', '23', '//', '(', '17', '-', '23', ')']),
                         "11.0")

    def test_pycalc(self):
        self.assertAlmostEqual(float(mn.pycalc('15+23*cos(17-23)')), 37.08391659295842)
        self.assertEqual(mn.pycalc('round(3.6675)'), '4.0')
