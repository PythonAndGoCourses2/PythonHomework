"""Converter module"""

from .operator_manager import operator_dict, function_dict, unary_dict
from .check_manager import check_parsing_list


class Converter:
    """Converter class"""
    def __init__(self, parsing_list):
        """
        Generates an instance of the Converter class,
        take an parsing_list as list from instance of SplitOperators class
        create an empty list to put the result of converting
        """
        self.parsing_list = parsing_list
        self.last_item = ""
        self.converted_list = []

    def _clean_add_sub_operators(self):
        """
        Encapsulate function
        Take all the successive of "+" and "-" and
        :return "-" if count("-") is odd or "+" if count is even
        """
        if self.last_item.count('-') % 2 == 0:
            if self.converted_list[-1] == '(':
                self.last_item = ""
            else:
                self.last_item = '+'
        else:
            self.last_item = '-'

    def _append_to_converted_list(self, *args):
        """
        Encapsulate function
        Append all converted elements into converted_list
        and update successive of "+" and "-" to empty value
        """
        [self.converted_list.append(i) for i in args]
        self.last_item = ""

    def _number_converter(self, number):
        """
        Encapsulate function
        Add unary operator if number is the first element in the parsing_list,
        add "-" to number if last_symbol is "-",
        otherwise add "+"
        """
        if self.last_item == '-':
            if self.converted_list[-1] == 0:
                self._append_to_converted_list(unary_dict[self.last_item], number)
            elif self.last_item == '-' and self.converted_list[-1] != '(' \
                    and self.converted_list[-1] not in operator_dict.values():
                self._append_to_converted_list(operator_dict[self.last_item], number)
            else:
                self._append_to_converted_list(-number)
        else:
            self._append_to_converted_list(number)

    def _operator_converter(self, operator_str):
        """
        Encapsulate function
        Convert math operator symbol into dictionary with built-in math operator
        Raise an exception if there is no operand between two math operators
        """
        if operator_str == '-' or operator_str == '+':
            self.last_item += operator_str
        else:
            try:
                if self.converted_list[-1]['operator']:
                    raise SyntaxError('Missing operand between two math operators!')
            except TypeError:
                self._append_to_converted_list(operator_dict[operator_str])

    def _function_converter(self, function):
        """
        Encapsulate function
        Convert math function name into dictionary with built-in math function
        Check necessary of "-" before the math function
        """
        if self.last_item:
            if self.last_item == '-' and self.converted_list[-1] != '(':
                self._append_to_converted_list(
                                                operator_dict['+'],
                                                -1,
                                                operator_dict['*'],
                                                function_dict[function]
                                                )
            else:
                self._append_to_converted_list(
                                                -1,
                                                operator_dict['*'],
                                                function_dict[function]
                                                )
        else:
            self._append_to_converted_list(function_dict[function])

    def converter(self):
        """
        The main function of the Converter class
        Call function to check if the parsing_list is valid
        Go thought the parsing_list and call necessary encapsulate function
        for every number, operator or function
        :return: converted_list
        """
        check_parsing_list(self.parsing_list)
        if self.parsing_list[0] in operator_dict.keys():
            self.converted_list.append(0)
        for i in self.parsing_list:
            if i == " ":
                continue
            if i != '-' and i != '+' and self.last_item:
                self._clean_add_sub_operators()
                if self.last_item == '+':
                    self._append_to_converted_list(operator_dict[self.last_item])
            if isinstance(i, float) or isinstance(i, int):
                self._number_converter(i)
            elif i in operator_dict.keys():
                self._operator_converter(i)
            elif i in function_dict.keys():
                self._function_converter(i)
            else:
                if self.last_item:
                    self._append_to_converted_list(operator_dict['-'])
                self._append_to_converted_list(i)
        return self.converted_list
