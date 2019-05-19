import unittest
import operator
import math
from pycalc.check_manager import check_expression, number_check, operator_check, function_check


class TestCheckManager(unittest.TestCase):

    def test_check_expression_empty(self):
        with self.assertRaises(SyntaxError):
            check_expression('')

    def test_check_expression_extra_close_bracket(self):
        with self.assertRaises(SyntaxError):
            check_expression('())')

    def test_check_expression_extra_open_bracket(self):
        with self.assertRaises(SyntaxError):
            check_expression('(()')

    def test_check_expression_return_expression(self):
        expression_line = check_expression('2+3')
        self.assertEqual('2+3', expression_line)

    def test_check_parsing_list_start_with_operator_add(self):
        parsing_list = check_parsing_list(['+', 42])
        self.assertEqual(['+', 42], parsing_list)

    def test_check_parsing_list_start_with_operator_sub(self):
        parsing_list = check_parsing_list(['-', 42])
        self.assertEqual(['-', 42], parsing_list)

    def test_check_parsing_list_start_with_operator_not_add_not_sub(self):
        with self.assertRaises(SyntaxError):
            check_parsing_list(['*', 2])

    def test_check_parsing_list_len_is_one_number(self):
        parsing_list = check_parsing_list([42])
        self.assertEqual([42], parsing_list)

    def test_check_parsing_list_len_is_one_str(self):
        with self.assertRaises(SyntaxError):
            check_parsing_list(['+'])

    def test_check_parsing_list_ends_with_operator(self):
        with self.assertRaises(SyntaxError):
            check_parsing_list([2, '+'])

    def test_check_parsing_list_ends_with_function(self):
        with self.assertRaises(SyntaxError):
            check_parsing_list([2, 'sin'])

    def test_check_parsing_list_positive(self):
        parsing_list = check_parsing_list([42, 'sin', '(', 2, '+', 3.2, ')'])
        self.assertEqual([42, 'sin', '(', 2, '+', 3.2, ')'], parsing_list)

    def test_operator_check_opertors_name(self):
        operator_str = ['+', '-', '/', '*', '**', '//', '%', '^', '==', '!=', '>', '>=', '<', '<=']
        operator_func = [
            operator.add,
            operator.sub,
            operator.truediv,
            operator.mul,
            operator.pow,
            operator.floordiv,
            operator.mod,
            operator.pow,
            operator.eq,
            operator.ne,
            operator.gt,
            operator.ge,
            operator.lt,
            operator.le
        ]
        for i in range(len(operator_str)):
            self.assertEqual(operator_str[i], operator_check(operator_str[i]))
            self.assertEqual(operator_func[i], operator_dict[operator_str[i]]['operator'])

    def test_operetor_check_negative(self):
        with self.assertRaises(SyntaxError):
            operator_check('/+')

    def test_numbert_check_int(self):
        self.assertTrue(isinstance(number_check('42'), int))

    def test_number_check_float(self):
        self.assertTrue(isinstance(number_check('42.0'), float))

    def test_function_check_constanta_e(self):
        self.assertEqual(math.e, function_check('e'))

    def test_function_check_constanta_pi(self):
        self.assertEqual(math.pi, function_check('pi'))

    def test_function_check_constanta_tau(self):
        self.assertEqual(math.pi*2, function_check('tau'))

    def test_function_check_function_dict(self):
        function_lst = ['abs', 'round']
        for key in math.__dict__.keys():
            if key.startswith('_') or key == 'e' or key == 'pi':
                continue
            function_lst.append(k)
        for i in range(len(function_lst)):
            self.assertEqual(function_lst[i], function_check(function_lst[i]))

    def test_function_chekc_not_function(self):
        with self.assertRaises(SyntaxError):
            function_check('log100')
