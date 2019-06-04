import unittest
import math
import operator
from pycalc.calculator import Calculator
from pycalc.operator_manager import create_func_dict

function_dict = create_func_dict()


class TestCalculator(unittest.TestCase):

    def test_init_class(self):
        calc = Calculator('42+pi', function_dict)
        self.assertEqual('42+pi', calc.expression_line)
        self.assertEqual(function_dict, calc.function_dict)
        self.assertEqual([42, '+', math.pi], calc.parser)
        self.assertEqual([42, {'operator': operator.add, 'priority': 4}, math.pi],
                         calc.converted_list)
        self.assertEqual("", calc.current_result)
        self.assertTrue(calc.operands.is_empty())
        self.assertTrue(calc.function.is_empty())
        self.assertEqual("", calc.current_operator)
        self.assertEqual([], calc.arg_result_lst)

    def test_calc_on_stack_function_with_one_argument(self):
        calc = Calculator('sin(pi/2)', function_dict)
        calc.function.put_on_stack({'operator': math.sin, 'priority': 0})
        calc.operands.put_on_stack((math.pi/2,))
        calc._calc_on_stack()
        self.assertEqual(1.0, calc.current_result)

    def test_calc_on_stack_function_with_two_arguments(self):
        calc = Calculator('log(16,4)', function_dict)
        calc.function.put_on_stack({'operator': math.log, 'priority': 0})
        calc.operands.put_on_stack((16, 4))
        calc._calc_on_stack()
        self.assertEqual(2.0, calc.current_result)

    def test_calc_on_stack_function_with_iterable_argument(self):
        calc = Calculator('fsum([1,2,3,4])', function_dict)
        calc.function.put_on_stack({'operator': math.fsum, 'priority': 0})
        calc.operands.put_on_stack([1, 2, 3, 4])
        calc._calc_on_stack()
        self.assertEqual(10.0, calc.current_result)

    def test_calculate_too_many_arguments(self):
        calc = Calculator('sin(pi,42)', function_dict)
        calc.function.put_on_stack({'operator': math.sin, 'priority': 0})
        calc.operands.put_on_stack((math.pi, 42))
        with self.assertRaises(SyntaxError):
            calc.calculate()

    def test_calc_on_stack_operator_with_two_operands(self):
        calc = Calculator('42/7', function_dict)
        calc.function.put_on_stack({'operator': operator.truediv, 'priority': 3})
        calc.operands.put_on_stack(42)
        calc.operands.put_on_stack(7)
        calc._calc_on_stack()
        self.assertEqual(6, calc.current_result)

    def test_calc_on_stack_operator_with_one_operand(self):
        calc = Calculator('-42', function_dict)
        calc.function.put_on_stack({'operator': operator.sub, 'priority': 4})
        calc.operands.put_on_stack(42)
        calc._calc_on_stack()
        self.assertEqual(-42, calc.current_result)

    def test_calc_on_stack_unary_operator(self):
        calc = Calculator('-42', function_dict)
        calc.function.put_on_stack({'operator': operator.sub, 'priority': 2})
        calc.operands.put_on_stack(42)
        calc._calc_on_stack()
        self.assertEqual(-42, calc.current_result)

    def test_clack_on_stack_recursion_function(self):
        calc = Calculator('3*2^2+1', function_dict)
        calc.function.stack = [{'operator': operator.mul, 'priority': 3},
                               {'operator': operator.pow, 'priority': 1}]
        calc.operands.stack = [3, 2, 2]
        calc.current_operator = {'operator': operator.add, 'priority': 4}
        calc._calc_on_stack()
        self.assertEqual(12, calc.current_result)

    def test_calculate_one_operand_int(self):
        calc = Calculator('42', function_dict)
        calc.converted_list = [42]
        self.assertEqual(42, calc.calculate())

    def test_calculate_one_operand_float(self):
        calc = Calculator('42.42', function_dict)
        calc.converted_list = [42.42]
        self.assertEqual(42.42, calc.calculate())

    def test_calculate_math_operator(self):
        calc = Calculator('42+8', function_dict)
        calc.converted_list = [42, {'operator': operator.add, 'priority': 4}, 8]
        self.assertEqual(50, calc.calculate())

    def test_calculate_unary_operator(self):
        calc = Calculator('42-8', function_dict)
        calc.converted_list = [42, {'operator': operator.sub, 'priority': 2}, 8]
        self.assertEqual(34, calc.calculate())

    def test_calculate_ad_operator_after_bracket(self):
        calc = Calculator('(42-8)/2', function_dict)
        calc.converted_list = ['(', 42, {'operator': operator.sub, 'priority': 4}, 8, ')',
                               {'operator': operator.truediv, 'priority': 3}, 2]
        self.assertEqual(17, calc.calculate())

    def test_calculate_ad_operator_with_higher_class_priority(self):
        calc = Calculator('42-8/2', function_dict)
        calc.converted_list = [42, {'operator': operator.sub, 'priority': 4}, 8,
                               {'operator': operator.truediv, 'priority': 3}, 2]
        self.assertEqual(38, calc.calculate())

    def test_calculate_ad_operator_power(self):
        calc = Calculator('42-8^2', function_dict)
        calc.converted_list = [42, {'operator': operator.sub, 'priority': 4}, 8,
                               {'operator': operator.pow, 'priority': 1}, 2]
        self.assertEqual(-22, calc.calculate())

    def test_calculate_ad_operator_power_after_power(self):
        calc = Calculator('2^4^2', function_dict)
        calc.converted_list = [2, {'operator': operator.pow, 'priority': 1}, 4,
                               {'operator': operator.pow, 'priority': 1}, 2]
        self.assertEqual(65536, calc.calculate())

    def test_calculate_expression_inside_brackets(self):
        calc = Calculator('1+(1-4/2)*3', function_dict)
        calc.converted_list = [
                                1, {'operator': operator.add, 'priority': 4}, '(', 1,
                                {'operator': operator.sub, 'priority': 4}, 4,
                                {'operator': operator.truediv, 'priority': 3}, 2, ')',
                                {'operator': operator.mul, 'priority': 3}, 3
                               ]
        self.assertEqual(-2, calc.calculate())
