import sys
from .operator_manager import operator_dict, function_dict, unary_dict
from .check_manager import check_expression, number_check, operator_check, function_check


class SplitOperators:

    def __init__(self):
        self.parsing_list = []
        self.last_number = ""
        self.last_letter = ""
        self.last_symbol = ""
        self.blank_item = False

    def _append_to_parsing_list(self):
        if self.last_symbol:
            self.parsing_list.append(operator_check(self.last_symbol))
            self.last_symbol = ""
        elif self.last_number:
            self.parsing_list.append(number_check(self.last_number))
            self.last_number = ""
        elif self.last_letter:
            self.parsing_list.append(function_check(self.last_letter))
            self.last_letter = ""

    def _number_parser(self, number):
        if self.blank_item and not isinstance(self.parsing_list[-1], str):
            raise SyntaxError('Blank symbol between two operands!')
        elif self.blank_item:
            self.blank_item = False
        if self.last_symbol:
            self._append_to_parsing_list()
        if self.last_letter:
            self.last_letter += number
        else:
            if '.' in self.last_number and number == '.':
                raise SyntaxError('Typo in the operand (two comma)!')
            else:
                self.last_number += number

    def _function_parser(self, letter):
        if self.last_symbol:
            self._append_to_parsing_list()
        self.last_letter += letter

    def _twice_operator_parser(self, symbol):
        if len(self.last_symbol) == 2:
            raise SyntaxError('Invalid operator "{}"'.format(self.last_symbol + symbol))
        if self.blank_item and str(self.parsing_list[-1]) in "!=<>/*":
            raise SyntaxError('Blank symbol between twice operator')
        elif self.blank_item:
            self.blank_item = False
        if not self.last_symbol:
            self._append_to_parsing_list()
        self.last_symbol += symbol

    def _simple_operator_bracket_parser(self, symbol):
        self._append_to_parsing_list()
        if symbol != ' ':
            self.parsing_list.append(symbol)

    def split_operators(self, expression_line):
        if check_expression(expression_line):
            for i in expression_line:
                if i == " ":
                    self.blank_item = True
                    self._append_to_parsing_list()
                if i.isnumeric() or i == '.':
                    self._number_parser(i)
                elif i.isalpha():
                    self._function_parser(i)
                elif i in "!=<>/*":
                    self._twice_operator_parser(i)
                else:
                    self._simple_operator_bracket_parser(i)
            if self.last_symbol:
                raise SyntaxError(
                    'Extra operator "{}" at the end of the expression!'.format(self.last_symbol)
                )
            self._append_to_parsing_list()
        return self.parsing_list
