import unittest
import math
from pycalc.split_operators import SplitOperators
from pycalc.operator_manager import create_func_dict


function_dict = create_func_dict()


class TestSplitOperators(unittest.TestCase):

    def test_init_class_method(self):
        expression = SplitOperators('1', {'tan': {'operator': math.tan, 'priority': 0}})
        self.assertEqual('1', expression.expression_line)
        self.assertEqual({'tan': {'operator': math.tan, 'priority': 0}}, expression.function_dict)
        self.assertEqual([], expression.parsing_list)
        self.assertEqual("", expression.last_number)
        self.assertEqual("", expression.last_letter)
        self.assertEqual("", expression.last_symbol)
        self.assertEqual(False, expression.blank_item)
        self.assertEqual("", expression.brackets)
        self.assertEqual(False, expression.arguments_needs)
        self.assertEqual("", expression.function_arguments)
        self.assertEqual("", expression.brackets_in_arguments)

    def test_symbol_append_to_parsing_list(self):
        expression = SplitOperators('', function_dict)
        expression.last_symbol = '*'
        expression._append_to_parsing_list()
        self.assertEqual(['*'], expression.parsing_list)
        self.assertEqual('', expression.last_symbol)

    def test_number_append_to_parsing_list(self):
        expression = SplitOperators('42', function_dict)
        expression.last_number = '42'
        expression._append_to_parsing_list()
        self.assertEqual([42], expression.parsing_list)
        self.assertEqual('', expression.last_number)

    def test_letter_append_to_parsing_list(self):
        expression = SplitOperators('42', function_dict)
        expression.last_letter = 'sin'
        expression._append_to_parsing_list()
        self.assertEqual(['sin'], expression.parsing_list)
        self.assertEqual('', expression.last_letter)
        self.assertEqual(True, expression.arguments_needs)

    def test_number_parser_with_symbol(self):
        expression = SplitOperators('42', function_dict)
        expression.last_symbol = '+'
        expression._number_parser('2')
        self.assertEqual(['+'], expression.parsing_list)
        self.assertEqual('2', expression.last_number)

    def test_number_parser_with_letter(self):
        expression = SplitOperators('42', function_dict)
        expression.last_letter = 'log'
        expression._number_parser('10')
        self.assertEqual('log10', expression.last_letter)
        self.assertEqual('', expression.last_number)

    def test_number_parser_with_first_number(self):
        expression = SplitOperators('42', function_dict)
        expression._number_parser('1')
        self.assertEqual('1', expression.last_number)
        self.assertEqual([], expression.parsing_list)

    def test_number_parser_with_second_number(self):
        expression = SplitOperators('42', function_dict)
        expression.last_number = '4'
        expression._number_parser('2')
        self.assertEqual('42', expression.last_number)
        self.assertEqual([], expression.parsing_list)

    def test_number_parser_two_comma(self):
        expression = SplitOperators('42', function_dict)
        expression.last_number = '1.0'
        with self.assertRaises(SyntaxError):
            expression._number_parser('.')

    def test_number_parser_space_into_operand(self):
        expression = SplitOperators('42', function_dict)
        expression.blank_item = True
        expression.parsing_list.append(1)
        with self.assertRaises(SyntaxError):
            expression._number_parser(2)

    def test_number_parser_blank_item_from_true_to_false(self):
        expression = SplitOperators('42', function_dict)
        expression.blank_item = True
        expression.parsing_list.append('+')
        expression._number_parser('2')
        self.assertEqual(False, expression.blank_item)
        self.assertEqual(['+'], expression.parsing_list)

    def test_function_parser_with_symbol(self):
        expression = SplitOperators('42', function_dict)
        expression.last_symbol = '+'
        expression._function_parser('s')
        self.assertEqual(['+'], expression.parsing_list)
        self.assertEqual('s', expression.last_letter)

    def test_function_parser_second_letter(self):
        expression = SplitOperators('42', function_dict)
        expression.last_letter = 's'
        expression._function_parser('i')
        self.assertEqual([], expression.parsing_list)
        self.assertEqual('si', expression.last_letter)

    def test_twice_operator_parser_blank_item_from_true_to_false(self):
        expression = SplitOperators('42', function_dict)
        expression.blank_item = True
        expression.parsing_list.append(1)
        expression._twice_operator_parser('*')
        self.assertEqual(False, expression.blank_item)
        self.assertEqual('*', expression.last_symbol)
        self.assertEqual([1], expression.parsing_list)

    def test_twice_operator_add_second_symbol(self):
        expression = SplitOperators('42', function_dict)
        expression.last_symbol = '*'
        expression._twice_operator_parser('*')
        self.assertEqual('**', expression.last_symbol)
        self.assertEqual([], expression.parsing_list)

    def test_twice_operator_parser_wrong_duble_operator(self):
        expression = SplitOperators('42', function_dict)
        expression.last_symbol = '**'
        with self.assertRaises(SyntaxError):
            expression._twice_operator_parser('*')

    def test_twice_operator_parser_space_into_operator(self):
        expression = SplitOperators('42', function_dict)
        expression.blank_item = True
        expression.parsing_list.append('*')
        with self.assertRaises(SyntaxError):
            expression._twice_operator_parser('*')

    def test_simple_operator(self):
        expression = SplitOperators('42', function_dict)
        expression._simple_operator_bracket_parser('/')
        self.assertEqual(['/'], expression.parsing_list)

    def test_simple_operator_add_open_bracket(self):
        expression = SplitOperators('42', function_dict)
        expression._simple_operator_bracket_parser('(')
        self.assertEqual(['('], expression.parsing_list)

    def test_simple_operator_add_closed_bracket(self):
        expression = SplitOperators('42', function_dict)
        expression.brackets = '('
        expression._simple_operator_bracket_parser(')')
        self.assertEqual([')'], expression.parsing_list)

    def test_simple_operator_add_wrong_bracket(self):
        expression = SplitOperators('42', function_dict)
        with self.assertRaises(SyntaxError):
            expression._simple_operator_bracket_parser(')')

    def test_simple_operator_blank_symbol(self):
        expression = SplitOperators('42', function_dict)
        expression._simple_operator_bracket_parser(' ')
        self.assertEqual([], expression.parsing_list)

    def test_simple_operator_bracket_for_function_argument(self):
        expression = SplitOperators('42', function_dict)
        expression.arguments_needs = True
        expression._simple_operator_bracket_parser('(')
        self.assertEqual('(', expression.brackets_in_arguments)
        self.assertEqual(True, expression.arguments_needs)

    def test_split_operators_number_and_blank_i(self):
        expression = SplitOperators('42 +', function_dict)
        expression.split_operators()
        self.assertEqual(True, expression.blank_item)
        self.assertEqual([42, '+'], expression.parsing_list)
        self.assertEqual('', expression.last_number)
        self.assertEqual('', expression.last_letter)
        self.assertEqual('', expression.last_symbol)

    def test_split_operators_number(self):
        expression = SplitOperators('42', function_dict)
        expression.split_operators()
        self.assertEqual('', expression.last_number)
        self.assertEqual([42], expression.parsing_list)
        self.assertEqual('', expression.last_letter)
        self.assertEqual('', expression.last_symbol)

    def test_split_operators_function(self):
        expression = SplitOperators('sin', function_dict)
        expression.split_operators()
        self.assertEqual(['sin'], expression.parsing_list)
        self.assertEqual('', expression.last_number)
        self.assertEqual('', expression.last_letter)
        self.assertEqual('', expression.last_symbol)

    def test_split_operators_twice_operator_one_symbol(self):
        expression = SplitOperators('42/7', function_dict)
        expression.split_operators()
        self.assertEqual([42, '/', 7], expression.parsing_list)
        self.assertEqual('', expression.last_number)
        self.assertEqual('', expression.last_letter)
        self.assertEqual('', expression.last_symbol)

    def test_split_operators_twice_operator_two_symbol(self):
        expression = SplitOperators('42//7', function_dict)
        expression.split_operators()
        self.assertEqual([42, '//', 7], expression.parsing_list)
        self.assertEqual('', expression.last_number)
        self.assertEqual('', expression.last_letter)
        self.assertEqual('', expression.last_symbol)

    def test_split_operators_brackets(self):
        expression = SplitOperators('(42)', function_dict)
        expression.split_operators()
        self.assertEqual(['(', 42, ')'], expression.parsing_list)
        self.assertEqual('', expression.last_number)
        self.assertEqual('', expression.last_letter)
        self.assertEqual('', expression.last_symbol)

    def test_split_operators_extra_operator(self):
        expression = SplitOperators('42//', function_dict)
        with self.assertRaises(SyntaxError):
            expression.split_operators()

    def test_split_operators_with_function_arguments(self):
        expression = SplitOperators('log(2, 2*e)', function_dict)
        expression.split_operators()
        self.assertEqual(['log', ('2', '2*e')], expression.parsing_list)
        self.assertEqual('', expression.last_number)
        self.assertEqual('', expression.last_letter)
        self.assertEqual('', expression.last_symbol)

    def test_collect_function_arguments_first_add_to_arguments(self):
        expression = SplitOperators('42', function_dict)
        expression.arguments_needs = True
        expression._collect_function_arguments('42')
        self.assertEqual('42', expression.function_arguments)
        self.assertEqual(True, expression.arguments_needs)

    def test_collect_function_arguments_add_bracket_to_arguments(self):
        expression = SplitOperators('42', function_dict)
        expression.arguments_needs = True
        expression._collect_function_arguments('(')
        self.assertEqual('(', expression.function_arguments)
        self.assertEqual(True, expression.arguments_needs)
        self.assertEqual('(', expression.brackets_in_arguments)

    def test_collect_function_arguments_add_last_bracket_to_arguments_with_split(self):
        expression = SplitOperators('42', function_dict)
        expression.brackets_in_arguments = '('
        expression.function_arguments = '42, 8'
        expression._collect_function_arguments(')')
        self.assertEqual(('42', '8'), expression.parsing_list[-1])
        self.assertEqual((''), expression.function_arguments)
        self.assertEqual(False, expression.arguments_needs)
        self.assertEqual('', expression.brackets_in_arguments)

    def test_collect_function_arguments_add_last_bracket_to_arguments_without_split(self):
        expression = SplitOperators('42', function_dict)
        expression.brackets_in_arguments = '('
        expression.function_arguments = '42'
        expression._collect_function_arguments(')')
        self.assertEqual('', expression.function_arguments)
        self.assertEqual(('42',), expression.parsing_list[-1])
        self.assertEqual(False, expression.arguments_needs)
        self.assertEqual('', expression.brackets_in_arguments)

    def test_collect_function_arguments_add_arguments_as_functions(self):
        expression = SplitOperators('42', function_dict)
        expression.brackets_in_arguments = '('
        expression.function_arguments = 'log(42,8)*pi'
        expression._collect_function_arguments(')')
        self.assertEqual(('log(42,8)*pi',), expression.parsing_list[-1])
        self.assertEqual('', expression.function_arguments)
        self.assertEqual(False, expression.arguments_needs)
        self.assertEqual('', expression.brackets_in_arguments)

