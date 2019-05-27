"""Split operators module"""

from .check_manager import check_expression, number_check, operator_check, function_check


class SplitOperators:
    """SplitOperators class"""
    def __init__(self, expression, functions):
        """
        Generates an instance of the SplitManager class,
        take an expression line as string,
        create an empty list to put the result of parsing line
        """
        self.expression_line = expression
        self.function_dict = functions
        self.parsing_list = []
        self.last_number = ""
        self.last_letter = ""
        self.last_symbol = ""
        self.blank_item = False
        self.brackets = ""

    def _append_to_parsing_list(self):
        """
        Encapsulate function
        Check if there is a number, symbol of the math operator
        or the name of the math function; call the check method of each element
        and if the element is clear append it to the self.parsing_list
        """
        if self.last_symbol:
            self.parsing_list.append(operator_check(self.last_symbol))
            self.last_symbol = ""
        elif self.last_number:
            self.parsing_list.append(number_check(self.last_number))
            self.last_number = ""
        elif self.last_letter:
            self.parsing_list.append(function_check(self.last_letter, self.function_dict))
            self.last_letter = ""

    def _number_parser(self, number):
        """
        Encapsulate function
        Create a number from successive digits in expression line,
        raise Exception when there is a space between two digits,
        or when there is more than two comma. If there is symbol of math operator
        or the name of math function call function to put this item into self.parsing_list
        :param number: is one digit from expression_line
        """
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
        """
        Encapsulate function
        Create a name of function from the successive letters.
        If there is symbol of math operator call function
        to put this item into self.parsing_list
        :param letter: is one letter from expression_line
        """
        if self.last_symbol:
            self._append_to_parsing_list()
        self.last_letter += letter

    def _twice_operator_parser(self, symbol):
        """
        Encapsulate function
        Create a twice operator symbol from successive math symbols.
        Raise an Exception when there is space between two symbols,
        or if it try to create math operator with more than two elements
        If there is symbol of math operator call function
        to put this item into self.parsing_list
        :param symbol: is one math symbol from expression_line
        """
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
        """
        Encapsulate function
        At fist call function to put data into self.parsing_list if it necessary.
        After put current symbol to the self.parsing_list
        :param symbol: is one math symbol from expression_line or bracket or comma
        """
        self._append_to_parsing_list()
        if symbol in '()':
            self.brackets += symbol
            if self.brackets.count(')') > self.brackets.count('('):
                raise SyntaxError('Position of brackets is wrong')
        elif symbol != ' ':
            self.parsing_list.append(symbol)

    def split_operators(self):
        """
        The main function of class SplitOperators
        Go thought the expression_line and call necessary encapsulate function
        for every digit, letter or symbol.
        Raise an Exception when there is a twice operator in the end of line
        :return: parsing_list as a list where each element is operand, math symbol
        or name of math function
        """
        if check_expression(self.expression_line):
            for i in self.expression_line:
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
