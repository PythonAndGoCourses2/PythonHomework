"""
Test a calculator for calculation operation and calculation errors.
"""

import unittest
from math import *

from pycalc.calculator import calculator
from pycalc.calculator.messages import ERROR_MSG_PREFIX


UNARY_OPERATORS = (
    "-13",
    "6-(-13)",
    "1---1",
    "-+---+-1"
)

OPERATION_PRIORITY = (
    "1+2*2",
    "1+(2+3*2)*3",
    "10*(2+1)",
    "10^(2+1)",
    "100/3^2",
    "100/3%2^2")

FUNCTIONS_AND_CONSTANTS = (
    "pi+e",
    "log(e)",
    "sin(pi/2)",
    "log10(100)",
    "sin(pi/2)*111*6",
    "2*sin(pi/2)",
    "abs(-5)",
    "round(123.456789)"
)

ASSOCIATIVE = (
    "102%12%7",
    "100/4/3",
    "2^3^4",
)

COMPARISON_OPERATORS = (
    "1+2*3==1+2*3",
    "e^5>=e^5+1",
    "1+2*4/3+1!=1+2*4/3+2",
)

COMMON_TESTS = (
    "(100)",
    "666",
    "-.1",
    "1/3",
    "1.0/3.0",
    ".1 * 2.0^56.0",
    "e^34",
    "(2.0^(pi/pi+e/e+2.0^0.0))",
    "(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)",
    "sin(pi/2^1) + log(1*4+2^2+1, 3^2)",
    "10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5",
    # a long expression splitted into two lines
    "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+"
    "cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)",
    "2.0^(2.0^2.0*2.0^2.0)",
    "sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))",
)

ERROR_CASES = (
    "",
    "+",
    "1-",
    "1 2",
    "ee",
    "==7",
    "1 + 2(3 * 4))",
    "((1+2)",
    "1 + 1 2 3 4 5 6 ",
    "log100(100)",
    "------",
    "5 > = 6",
    "5 / / 6",
    "6 < = 6",
    "6 * * 6",
    "(((((",
    "pow(2, 3, 4)",
)


CALCULATION_CASES = (
    UNARY_OPERATORS,
    OPERATION_PRIORITY,
    FUNCTIONS_AND_CONSTANTS,
    ASSOCIATIVE,
    COMPARISON_OPERATORS,
    COMMON_TESTS
)


def replace_power_sign(string):
    """Replace the power sign in a string to the python’s power sign."""

    return string.replace('^', '**')


def is_error_message(string):
    """Check if a string is an error message."""

    return string.startswith(ERROR_MSG_PREFIX)


class CalculatorTestCase(unittest.TestCase):
    """Test a calculator."""

    @classmethod
    def setUpClass(cls):
        cls.calculator = calculator()

    def test_calculation(self):
        """Test calculation of a calculator."""

        for cases in CALCULATION_CASES:
            for case in cases:
                with self.subTest(case=case):
                    case_ = replace_power_sign(case)
                    self.assertEqual(self.calculator.calculate(
                        case), eval(case_), case)

    def test_errors(self):
        """Test a calculator returns errors."""

        for case in ERROR_CASES:
            with self.subTest(case=case):
                result = str(self.calculator.calculate(case))
                self.assertTrue(is_error_message(result), case)
