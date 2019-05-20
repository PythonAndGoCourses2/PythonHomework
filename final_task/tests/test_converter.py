import math
import operator
import unittest
from pycalc.converter import Converter


class TestConverter(unittest.TestCase):

    def test_init_class(self):
        converter = Converter([42, '+', 3])
        self.assertEqual([42, '+', 3], converter.parsing_list)
        self.assertEqual("", converter.last_item)
        self.assertEqual([], converter.converted_list)

    def test_clean_add_sub_operators_minus_into_plus_after_bracket(self):
        converter = Converter([42])
        converter.last_item = '--'
        converter.converted_list.append('(')
        converter._clean_add_sub_operators()
        self.assertEqual("", converter.last_item)

    def test_clean_add_sub_operators_minus_into_plus(self):
        converter = Converter([42])
        converter.last_item = '--'
        converter.converted_list.append(42)
        converter._clean_add_sub_operators()
        self.assertEqual('+', converter.last_item)

    def test_clean_add_sub_operators_minus_into_minus(self):
        converter = Converter([42])
        converter.last_item = '---'
        converter.converted_list.append(42)
        converter._clean_add_sub_operators()
        self.assertEqual('-', converter.last_item)

    def test_append_to_converted_list(self):
        converter = Converter([42])
        converter.last_item = '+'
        converter._append_to_converted_list(42, '+', 8)
        self.assertEqual([42, '+', 8], converter.converted_list)
        self.assertEqual("", converter.last_item)

    def test_number_converter_with_minus_after_zero(self):
        converter = Converter([42])
        converter.last_item = '-'
        converter.converted_list.append(0)
        test_number = 42
        converter._number_converter(test_number)
        self.assertEqual([0, {'operator': operator.sub, 'priority': 2}, 42], converter.converted_list)

    def test_number_converter_with_minus_after_close_bracket(self):
        converter = Converter([42])
        converter.last_item = '-'
        converter.converted_list.append(')')
        test_number = 42
        converter._number_converter(test_number)
        self.assertEqual([')',
                          {'operator': operator.sub,
                           'priority': 4},
                          42],
                         converter.converted_list)

    def test_number_converter_with_minus_after_operand(self):
        converter = Converter([42])
        converter.last_item = '-'
        converter.converted_list.append('(')
        test_number = 42
        converter._number_converter(test_number)
        self.assertEqual(['(', -42], converter.converted_list)

    def test_number_converter_without_minus(self):
        converter = Converter([42])
        converter.last_item = '+'
        test_number = 42
        converter._number_converter(test_number)
        self.assertEqual([42], converter.converted_list)

    def test_operator_converter_collect_all_plus_minus(self):
        converter = Converter([42])
        operator_str = '-'
        converter._operator_converter(operator_str)
        self.assertEqual('-', converter.last_item)
        operator_str = '+'
        converter._operator_converter(operator_str)
        self.assertEqual('-+', converter.last_item)

    def test_operator_converter_add_to_converted_list(self):
        converter = Converter([42])
        operator_str = ['/', '*', '**', '//', '%', '^', '==', '!=', '>', '>=', '<', '<=']
        operator_func = [
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
        converter.converted_list.append([42])
        for i in range(len(operator_str)):
            converter._operator_converter(operator_str[i])
            self.assertEqual(operator_func[i], converter.converted_list[1]['operator'])
            converter.converted_list.pop()

    def test_operator_converter_raise_exception_after_operator(self):
        converter = Converter([42])
        converter.converted_list.append({'operator': operator.truediv})
        operator_str = '/'
        with self.assertRaises(SyntaxError):
            converter._operator_converter(operator_str)

    def test_function_converter_add_negative_function_after_operand(self):
        converter = Converter([42])
        converter.last_item = '-'
        converter.converted_list.append(42)
        function_str = 'sin'
        converter._function_converter(function_str)
        self.assertEqual([42,
                          {'operator': operator.add, 'priority': 4},
                          -1,
                          {'operator': operator.mul, 'priority': 3},
                          {'operator': math.sin, 'priority': 0}],
                         converter.converted_list)

    def test_function_converter_add_negative_function_after_open_bracket(self):
        converter = Converter(42)
        converter.last_item = '-'
        converter.converted_list.append('(')
        function_str = 'sin'
        converter._function_converter(function_str)
        self.assertEqual(['(',
                          -1,
                          {'operator': operator.mul, 'priority': 3},
                          {'operator': math.sin, 'priority': 0}],
                         converter.converted_list)

    def test_function_converter_add_negative_function_after_close_bracket(self):
        converter = Converter([42])
        converter.last_item = '-'
        converter.converted_list.append(')')
        function_str = 'sin'
        converter._function_converter(function_str)
        self.assertEqual([')',
                          -1,
                          {'operator': operator.mul, 'priority': 3},
                          {'operator': math.sin, 'priority': 0}],
                         converter.converted_list)

    def test_function_converter_add_positive_function(self):
        converter = Converter([42])
        function_str = 'sin'
        converter._function_converter(function_str)
        self.assertEqual([{'operator': math.sin, 'priority': 0}], converter.converted_list)

    def test_converter_add_zero_into_beginning_with_unary_sub(self):
        converter = Converter(['-', 42])
        converter.converter()
        self.assertEqual([0, {'operator': operator.sub, 'priority': 2}, 42],
                         converter.converted_list)

    def test_converter_remove_space(self):
        converter = Converter([42,' '])
        converter.converter()
        self.assertEqual([42], converter.converted_list)

    def test_converter_append_append_clean_add_operator(self):
        converter = Converter([42, '+', '-', '-', 8])
        converter.converter()
        self.assertEqual([42, {'operator': operator.add, 'priority': 4}, 8],
                         converter.converted_list)

    def test_converter_append_int(self):
        converter = Converter([42])
        converter.converter()
        self.assertEqual([42], converter.converted_list)

    def test_converter_append_float(self):
        converter = Converter([42.8])
        converter.converter()
        self.assertEqual([42.8], converter.converted_list)

    def test_converter_append_operator(self):
        converter = Converter([42, '*', 8])
        converter.converter()
        self.assertEqual([42, {'operator': operator.mul, 'priority': 3}, 8],
                         converter.converted_list)

    def test_converter_append_function(self):
        converter = Converter(['sin', '(', 42, ')'])
        converter.converter()
        self.assertEqual([{'operator': math.sin, 'priority': 0}, '(', 42, ')'],
                         converter.converted_list)

    def test_converter_append_bracket_with_minus(self):
        converter = Converter(['(', '-', 42, ')'])
        converter.converter()
        self.assertEqual(['(', -42, ')'],
                         converter.converted_list)
