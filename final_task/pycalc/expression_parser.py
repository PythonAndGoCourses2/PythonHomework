import sys
from .operator_manager import *


def check_expression(expression_line):
    if not expression_line:
        raise SyntaxError('Expression cannot be empty')
    if expression_line.count('(') < expression_line.count(')'):
        raise SyntaxError('Opening bracket required!')
    elif expression_line.count('(') > expression_line.count(')'):
        raise SyntaxError('Closing bracket required!')
    return True


class SplitOperators:

    def __init__(self):
        self.parsing_list = []
        self.last_number = ""
        self.last_letter = ""
        self.last_symbol = ""
        self.blank_item = False

    def operartor_check(self, operator_symbol):
        if operator_symbol in operator_dict.keys():
            return operator_symbol
        raise SyntaxError('Typo in math operator!')

    def number_check(self, number):
        try:
            return int(number)
        except ValueError:
            return float(number)

    def function_check(self, function_name):
        if function_name == 'e' or function_name == 'pi':
            return function_dict[function_name]['operator']
        elif function_name == 'tau':
            if sys.version_info >= (3, 6):
                return function_dict[function_name]['operator']
            else:
                return 2 * function_dict['e']['operator']
        elif function_name in function_dict.keys():
            return function_name
        else:
            raise SyntaxError(
                'There is no function with this name {}!'.format(function_name)
            )

    def append_to_parsing_list(self):
        if self.last_symbol:
            self.parsing_list.append(self.operartor_check(self.last_symbol))
            self.last_symbol = ""
        elif self.last_number:
            self.parsing_list.append(self.number_check(self.last_number))
            self.last_number = ""
        elif self.last_letter:
            self.parsing_list.append(self.function_check(self.last_letter))
            self.last_letter = ""

    def number_parser(self, number):
        if self.blank_item and not isinstance(self.parsing_list[-1], str):
            raise SyntaxError('Blank symbol between two operands!')
        elif self.blank_item:
            self.blank_item = False
        if self.last_symbol:
            self.append_to_parsing_list()
        if self.last_letter:
            self.last_letter += number
        else:
            if '.' in self.last_number and number == '.':
                raise SyntaxError('Typo in the operand (two comma)!')
            else:
                self.last_number += number

    def function_parser(self, letter):
        if self.last_symbol:
            self.append_to_parsing_list()
        self.last_letter += letter

    def twice_operator_parser(self, symbol):
        if len(self.last_symbol) == 2:
            raise SyntaxError('Invalid operator "{}"'.format(self.last_symbol + symbol))
        if self.blank_item and str(self.parsing_list[-1]) in "!=<>/*":
            raise SyntaxError('Blank symbol between twice operator')
        elif self.blank_item:
            self.blank_item = False
        if not self.last_symbol:
            self.append_to_parsing_list()
        self.last_symbol += symbol

    def simple_operator_bracket_parser(self, symbol):
        self.append_to_parsing_list()
        if symbol != ' ':
            self.parsing_list.append(symbol)

    def split_operators(self, expression_line):
        if check_expression(expression_line):
            for i in expression_line:
                if i == " ":
                    self.blank_item = True
                    self.append_to_parsing_list()
                if i.isnumeric() or i == '.':
                    self.number_parser(i)
                elif i.isalpha():
                    self.function_parser(i)
                elif i in "!=<>/*":
                    self.twice_operator_parser(i)
                else:
                    self.symple_operator_bracket_parser(i)
            if self.last_symbol:
                raise SyntaxError(
                    'Extra operator "{}" at the end of the expression!'.format(self.last_symbol)
                )
            self.append_to_parsing_list()
        return self.parsing_list
