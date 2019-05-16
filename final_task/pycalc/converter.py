from .operator_manager import operator_dict, function_dict, unary_dict
from .check_manager import check_parsing_list


class Converter:

    def __init__(self, parsing_list):
        self.parsing_list = parsing_list
        self.last_item = ""
        self.converted_list = []

    def _clean_add_sub_operators(self):
        if self.last_item.count('-') % 2 == 0:
            if self.converted_list[-1] == '(':
                self.last_item = ""
            else:
                self.last_item = '+'
        else:
            self.last_item = '-'

    def _append_to_converted_list(self, *args):
        [self.converted_list.append(i) for i in args]
        self.last_item = ""

    def _number_converter(self, number):
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
        if operator_str == '-' or operator_str == '+':
            self.last_item += operator_str
        else:
            try:
                if self.converted_list[-1]['operator']:
                    raise SyntaxError('Missing operand between two math operators!')
            except TypeError:
                self._append_to_converted_list(operator_dict[operator_str])

    def _function_converter(self, function):
        if self.last_item:
            if self.last_item == '-' and self.converted_list[-1] != '(':
                self._append_to_converted_list(
                                                operator_dict['+'],
                                                -1,
                                                operator_dict['*'],
                                                function_dict[function]
                                                )
            elif self.last_item == '-' and self.converted_list[-1] in '()':
                self._append_to_converted_list(
                                                -1,
                                                operator_dict['*'],
                                                function_dict[function]
                                                )
        else:
            self._append_to_converted_list(function_dict[function])

    def converter(self):
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
