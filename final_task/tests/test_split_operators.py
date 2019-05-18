import unittest
from unittest.mock import patch, MagicMock
from pycalc.split_operators import SplitOperators


class TestSplitOperators(unittest.TestCase):

    def test_init_class_method(self):
        expression = SplitOperators('1')
        self.assertEqual('1', expression.expression_line)
        self.assertEqual([], expression.parsing_list)
        self.assertEqual("", expression.last_number)
        self.assertEqual("", expression.last_letter)
        self.assertEqual("", expression.last_symbol)
        self.assertEqual(False, expression.blank_item)

    def test_uno_number(self):
        expression = SplitOperators('1')
        result = expression.split_operators()
        self.assertEqual([1], result)

    def test_twice_number(self):
        expression = SplitOperators('12')
        result = expression.split_operators()
        self.assertEqual([12], result)

    def test_symbol_append_to_parsing_list(self):
        expression = SplitOperators('')
        expression.last_symbol = '*'
        expression._append_to_parsing_list()
        self.assertEqual(['*'], expression.parsing_list)
        self.assertEqual('', expression.last_symbol)

    def test_number_append_to_parsing_list(self):
        expression = SplitOperators('12')
        expression.last_number = '12'
        expression._append_to_parsing_list()
        self.assertEqual([12], expression.parsing_list)
        self.assertEqual('', expression.last_number)

    def test_letter_append_to_parsing_list(self):
        expression = SplitOperators('12')
        expression.last_letter = 'sin'
        expression._append_to_parsing_list()
        self.assertEqual(['sin'], expression.parsing_list)
        self.assertEqual('', expression.last_letter)

    def test_number_parser_with_symbol(self):
        expression = SplitOperators('12')
        expression.last_symbol = '+'
        expression._number_parser('2')
        self.assertEqual(['+'], expression.parsing_list)
        self.assertEqual('2', expression.last_number)

    def test_number_parser_with_letter(self):
        expression = SplitOperators('12')
        expression.last_letter = 'log'
        expression._number_parser('10')
        self.assertEqual('log10', expression.last_letter)
        self.assertEqual('', expression.last_number)

    def test_number_parser_with_first_number(self):
        expression = SplitOperators('12')
        expression._number_parser('1')
        self.assertEqual('1', expression.last_number)
        self.assertEqual([], expression.parsing_list)

    def test_number_parser_with_second_number(self):
        expression = SplitOperators('12')
        expression.last_number = '1'
        expression._number_parser('2')
        self.assertEqual('12', expression.last_number)
        self.assertEqual([], expression.parsing_list)

    def test_number_parser_two_comma(self):
        expression = SplitOperators('12')
        expression.last_number = '1.0'
        with self.assertRaises(SyntaxError):
            expression._number_parser('.')

    def test_number_parser_space_into_operand(self):
        expression = SplitOperators('12')
        expression.blank_item = True
        expression.parsing_list.append(1)
        with self.assertRaises(SyntaxError):
            expression._number_parser(2)

    def test_number_parser_blank_item_from_true_to_false(self):
        expression = SplitOperators('12')
        expression.blank_item = True
        expression.parsing_list.append('+')
        expression._number_parser('2')
        self.assertEqual(False, expression.blank_item)
        self.assertEqual(['+'], expression.parsing_list)

    def test_function_parser_with_symbol(self):
        expression = SplitOperators('12')
        expression.last_symbol = '+'
        expression._function_parser('s')
        self.assertEqual(['+'], expression.parsing_list)
        self.assertEqual('s', expression.last_letter)

    def test_function_parser_second_letter(self):
        expression = SplitOperators('12')
        expression.last_letter = 's'
        expression._function_parser('i')
        self.assertEqual([], expression.parsing_list)
        self.assertEqual('si', expression.last_letter)

    def test_twice_operator_parser_blank_item_from_true_to_false(self):
        expression = SplitOperators('12')
        expression.blank_item = True
        expression.parsing_list.append(1)
        expression._twice_operator_parser('*')
        self.assertEqual(False, expression.blank_item)
        self.assertEqual('*', expression.last_symbol)
        self.assertEqual([1], expression.parsing_list)

    def test_twice_operator_add_second_symbol(self):
        expression = SplitOperators('12')
        expression.last_symbol = '*'
        expression._twice_operator_parser('*')
        self.assertEqual('**', expression.last_symbol)
        self.assertEqual([], expression.parsing_list)

    # need to think about how to simulate func call
    # def test_twice_operator_parser(self):
    #     expression = SplitOperators('12')
    #     expression.parsing_list.append(1)
    #     call_func = SplitOperators._append_to_parsing_list(expression)
    #     with patch.object(call_func, 'Clear') as mock:
    #         expression._twice_operator_parser('*')
    #     call_func.assert_called_once()
    #     self.assertEqual([1], expression.parsing_list)

    def test_twice_operator_parser_wrong_duble_operator(self):
        expression = SplitOperators('12')
        expression.last_symbol = '**'
        with self.assertRaises(SyntaxError):
            expression._twice_operator_parser('*')

    def test_twice_operator_parser_space_into_operator(self):
        expression = SplitOperators('12')
        expression.blank_item = True
        expression.parsing_list.append('*')
        with self.assertRaises(SyntaxError):
            expression._twice_operator_parser('*')

    # need to think about how to simulate func call
    def test_simple_operator(self):
        expression = SplitOperators('12')
        expression._simple_operator_bracket_parser('/')
        self.assertEqual(['/'], expression.parsing_list)

    # need to think about how to simulate func call
    def test_simple_operator_add_bracke(self):
        expression = SplitOperators('12')
        expression._simple_operator_bracket_parser('(')
        self.assertEqual(['('], expression.parsing_list)

    # need to think about how to simulate func call
    def test_simple_operator_blank_symbol(self):
        expression = SplitOperators('12')
        expression._simple_operator_bracket_parser(' ')
        self.assertEqual([], expression.parsing_list)
