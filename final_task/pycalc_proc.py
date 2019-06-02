# -*- coding: Windows-1251 -*-
import sys
import inspect

from final_task.config import *


# �. �. ValueError ����� � ��� traceback, ������������� ������� � sys, ����� � ��� �������� ������ ���������
def excepthook(type, value, traceback):
    print(value)


sys.excepthook = excepthook


class PyCalcProcessing(object):

    def __init__(self, formula_string):
        self.formula_string = formula_string

    @staticmethod
    def _matched_parentheses(el, count):
        """
        Counter for '(', ')'.

        :param el (str): opening or closing parentheses
        :param count (int): counter of parentheses
        :return: count (int)
        """
        if el == "(":
            count += 1
        elif el == ")":
            count -= 1
        return count

    @staticmethod
    def pre_validate(formula_string):
        """
        Need to apply pre-validation of some errors before parsing to tokens fo more convenient
        parsing in current version of implementation.

        :param formula_string: input formula as text
        :return: None
        """
        # ��������, ��� ������� �� ������ ������
        if not isinstance(formula_string, str) or not formula_string:
            print('ERROR: Formula should be not empty string!')
        # ���������, ��� � ������� ��� ����� ������ ����������� ������
        # � ������� ���������� ������� ������� ��� �����, ����� ��������� ���������� ������� �� ������
        if '..' in formula_string:
            print('ERROR: Number can not contain more than one delimiter "." !')
        # �������� �� ����������� ��������
        for el in formula_string.strip():
            if el not in ALLOWED_TOKENS:
                print('ERROR: Formula contains incorrect symbol "{}"'.format(el))

    @staticmethod
    def parse(formula_string):
        number = ''  # ��� ���������� �����
        op = ''  # ��� ���������� ����������
        function = ''  # ��� ���������� �������
        for el in formula_string.strip():
            if el in LETTERS:  # ��������� �������
                function += el.lower()
                if op:  # ���������� ��������, ���� ��� ��������
                    yield op
                    op = ''
                if number:  # ���������� �����, ���� ���� ���������
                    yield float(number) if number != '.' else '.'
                    number = ''
            elif el in string.digits + '.':  # ��������� ����� ����� � � ������
                if function:
                    function += el  # ���������� ����������� �������, ���� �� �������� ���-�� �������� �� �����
                else:
                    number += el
                    if op:  # ���������� ��������, ���� ��� ��������
                        yield op
                        op = ''
                    if function:  # ���������� �������, ���� ���� ���������
                        yield function
                        function = ''
            elif el in OPERATORS_BEGIN:  # ��������� ����������
                if el in DOUBLE_OPER_PART1 and not op:  # ���� �������� ������� ��������, �������� � ���
                    op += el
                elif el in DOUBLE_OPER_PART2 and op:  # ������ �������
                    op += el
                    if number:  # ���������� �����, ���� ���� ���������
                        yield float(number) if number != '.' else '.'
                        number = ''
                    if function:  # ���������� �������, ���� ���� ���������
                        yield function
                        function = ''
                    yield op  # ���������� �������� �������, ����� �� ��� ��������
                    op = ''
                else:  # ���� �������� ���������
                    if op:  # ���� ��� �������� �� ���������� ���� - ����������, ��������
                        yield op
                        op = ''
                    if number:  # ���������� �����, ���� ���� ���������
                        yield float(number) if number != '.' else '.'
                        number = ''
                    if function:  # ���������� �������, ���� ���� ���������
                        yield function
                        function = ''
                    yield el  # ������������ ��������� ��������
                if number:  # ���������� �����, ���� ���� ���������
                    yield float(number) if number != '.' else '.'
                    number = ''
                if function:  # ���������� �������, ���� ���� ���������
                    yield function
                    function = ''
            elif el in PARENTHESES + (',',):  # ��������� ������ � ������� (���� ������� � ����������� �����������)
                if number:  # ���������� �����, ���� ���� ���������
                    yield float(number) if number != '.' else '.'
                    number = ''
                if function:  # ���������� �������, ���� ���� ���������
                    yield function
                    function = ''
                if op:  # ���������� ��������, ���� ��� ��������
                    yield op
                    op = ''
                yield el  # ���������� ������ ��� �������, ��� ������ ���������
        if function:  # ���������� �������, ���� ���� ���������
            yield function
        if number:  # ���������� �����, ���� ���� ���������
            yield float(number) if number != '.' else '.'
        if op:  # ���������� ��������, ���� ���� ���������
            yield op

    def validate_parsed_list(self, parsed_list):
        if parsed_list[-1] in OPERATORS:
            print('ERROR: Operator at the end of the formula: "{}" '.format(parsed_list[-1]))
        if parsed_list[0] in BINARY_OPERATORS:
            print('ERROR: Formula can not start with binary operator "{}"'.format(parsed_list[0]))

        counter = 0  # counter for parentheses
        was_number = False

        previous_el = ''
        for el in parsed_list:
            counter = self._matched_parentheses(el, counter)

            message = 'ERROR: After {} element {} is forbidden!'.format(str(previous_el), str(el))

            if el == '.':
                print('ERROR: Single delimiter is prohibited in formula!')

            if isinstance(el, str) and el[0] in LETTERS:
                if el.lower() not in ALL_FUNCTIONS_AND_CONSTS:
                    print('Function or constant {} is not supported by calculator'.format(el))

            if previous_el == '(':
                if el in ((')', ',',) + tuple(BINARY_OPERATORS.keys())):
                    print(message)

            if previous_el == ')':
                if el in (('(',) + ALL_FUNCTIONS_AND_CONSTS) or isinstance(el, float):
                    print(message)

            if previous_el == ',':
                if el in (')', ',', '.'):
                    print(message)

            if previous_el in UNARY_OPERATORS:
                if el in ((')', ',',) + tuple(BINARY_OPERATORS.keys())):
                    print(message)

            if previous_el in BINARY_OPERATORS:
                if el in ((')', ',',) + tuple(BINARY_OPERATORS.keys())):
                    print(message)

            if previous_el in ALL_FUNCTIONS:
                if el != '(':
                    print(message)

            if isinstance(previous_el, float) or previous_el in MATH_CONSTS:
                was_number = True
                if el in (('(',) + ALL_FUNCTIONS_AND_CONSTS) or isinstance(el, float):
                    print(message)

            previous_el = el

        if counter != 0:
            print('ERROR: Wrong number of opened or closed parentheses in formula!')

        if not was_number:
            print('Formula does not contain numbers!')

        return 'Formula was validated! Errors were not found.'

    @staticmethod
    def process_unary_operations(validated_list):
        """
        :param validated_list: list of tokens after parsing of input formula and validation of it
        :return: processed_list: all unary '+' are removed, all redundant unary '-' are removed
        """
        stack_str = ''
        processed_list = []
        for el in validated_list:
            if el in UNARY_OPERATORS:
                stack_str += el
            else:
                is_unary_plus = ((processed_list and processed_list[-1] in
                                  (('(', ',') + tuple(BINARY_OPERATORS.keys()))) or not processed_list)
                if stack_str:
                    if '-' in stack_str:
                        if stack_str.count('-') % 2 == 0:  # ������� ���-�� -, ������� �� + ���� �� -
                            if is_unary_plus:
                                stack_str = ''
                            else:
                                stack_str = '+'
                        else:
                            stack_str = '-'
                    else:
                        if is_unary_plus:
                            stack_str = ''
                        else:
                            stack_str = '+'
                    if stack_str:
                        processed_list.append(stack_str)
                    stack_str = ''
                processed_list.append(el)
        return processed_list

    @staticmethod
    def sort_to_polish(parsed_formula):
        stack = []  # � �������� ����� ���������� ������
        previous_token = ''
        for token in parsed_formula:
            # ���� ������� - ��������, �� ���������� ������ ��� ��������� �� �����,
            # ��� ��������� ������ ��� ����� ����������,
            # �� ����������� ������ ��� ����������� �����.
            if token in ALL_FUNCTIONS_AND_OPERATORS_DICT:
                if token == '-' and previous_token in ('(', ',', '') + tuple(BINARY_OPERATORS.keys()):
                    yield 0.0
                    stack.append(token)
                else:
                    while (stack and stack[-1] != "(" and
                           ALL_FUNCTIONS_AND_OPERATORS_DICT[token][0] <= ALL_FUNCTIONS_AND_OPERATORS_DICT[stack[-1]][0]
                           and token != '^'):
                        yield stack.pop()
                    stack.append(token)
            elif token == ")":
                # ���� ������� - ����������� ������, ����� ��� �������� �� �����, �� ����������� ������,
                # � ����������� ������ ���������� �� �����.
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                # ���� ������� - ����������� ������, ������ ������� � � ����
                stack.append(token)
            elif token == ",":  # ����� ���������
                # ����� ��� ��������� �� ����� �� ����������� ������
                while stack and stack[-1] != "(":
                    yield stack.pop()
            else:
                # ���� ������� - ����� ��� ���������, �������� ��� ����� �� �����
                yield token
            previous_token = token
        while stack:
            yield stack.pop()

    @staticmethod
    def _get_num_args(func):
        if inspect.isfunction(func):
            return len(inspect.getfullargspec(func).args)
        else:
            spec = func.__doc__.split('\n')[0]
            args = spec[spec.find('(') + 1:spec.find(')')]
        return args.count(',') + 1 if args else 0

    def calc(self, polish_list):
        stack = []
        function_result = None

        for token in polish_list:
            if token in MATH_FUNCTIONS:
                arguments = []
                func_name = getattr(math, token)

                #  TODO ���� ������� � log
                if func_name != math.log:
                    number_of_args = self._get_num_args(func_name)
                    for i in range(number_of_args):
                        if stack:
                            arguments.insert(0, stack.pop())
                else:
                    # �. �. log ����� ���������� ���-�� ���������� ��������� ���������
                    index_current_log_token = polish_list.index(token)
                    try:
                        next_token_after_log = polish_list[index_current_log_token + 1]
                    except IndexError:
                        next_token_after_log = ''

                    if next_token_after_log in OPERATORS and len(stack) == 2:
                        arguments.insert(0, stack.pop())
                    else:
                        if len(stack) >= 2:
                            arguments.insert(0, stack.pop())
                            arguments.insert(0, stack.pop())
                        else:
                            arguments.insert(0, stack.pop())

                try:
                    function_result = func_name(*tuple(arguments))
                except TypeError:
                    print('ERROR: Formula contains incorrect number of arguments in function.')

                stack.append(function_result)  # ��������� ��������, ���������� � ����
                arguments = []

            elif token in BUILT_IN_FUNCTIONS:
                x = stack.pop()  # �������� 1 ����o �� �����
                # TODO how to get built-in attr automatically
                if token == 'abs':
                    stack.append(abs(x))
                elif token == 'round':
                    stack.append(round(x))
            elif token in OPERATORS:  # ���� ���������� ������� - ��������,
                y, x = stack.pop(), stack.pop()  # �������� 2 ����� �� �����
                stack.append(OPERATORS[token][1](x, y))  # ��������� ��������, ���������� � ����
            elif token in MATH_CONSTS:
                stack.append(getattr(math, token))
            else:
                stack.append(token)

        if len(stack) > 1:
            print('ERROR: Formula contains incorrect number of arguments in function.')

        return stack[0]  # ��������� ���������� - ������������ ������� � �����

    def launch_processing(self):
        self.pre_validate(self.formula_string)
        parsed_list = []
        for el in self.parse(self.formula_string):
            parsed_list.append(el)
        self.validate_parsed_list(parsed_list)
        parsed_list = self.process_unary_operations(parsed_list)
        polish_list = []
        for el in self.sort_to_polish(parsed_list):
            polish_list.append(el)
        result = self.calc(polish_list)
        print(result)


obj = PyCalcProcessing('abs')
obj.launch_processing()