# -*- coding: Windows-1251 -*-
import inspect
import re
import builtins

from config import *


class PyCalcProcessing(object):

    def __init__(self, formula_string):
        self.formula_string = re.sub(' +', ' ', formula_string)

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
        :return: was_error
        """
        was_error = False
        # check that formula is not empty
        if not isinstance(formula_string, str) or not formula_string:
            print('ERROR: Formula should be not empty string!')
            return True
        # check that there is not more than one delimiter in a row in the formula
        # it's more convenient to do it here in order to simplify parsing to tokens
        if '..' in formula_string:
            print('ERROR: Number can not contain more than one delimiter "." !')
            was_error = True
        # check if there is whitespace between double operators
        if re.search('/ /|< =|> =|= =|! =', formula_string):
            print('ERROR: space is not allowed in operators: //, <=, >=, ==, !=.')
            was_error = True
        if re.search(r'\d\s\d', formula_string):
            print('ERROR: space is not allowed between digits!')
            was_error = True
        # check allowed tokens
        for el in formula_string.strip():
            if el not in ALLOWED_TOKENS:
                print('ERROR: Formula contains incorrect symbol "{}"'.format(el))
                was_error = True
        return was_error

    @staticmethod
    def parse(formula_string):
        """
        Parsing formula to tokens

        :param formula_string: input formula as text which have passed pre-validation
        :return: None
        """
        number = op = function = ''
        for el in formula_string.strip():
            if el in LETTERS:  # function processing
                function += el.lower()
                if op:  # shot the operator if it has been accumulated
                    yield op
                    op = ''
                if number:  # shot number if it was accumulated
                    yield float(number) if number != '.' else '.'
                    number = ''
            elif el in string.digits + '.':  # processing integers and floats
                if function:
                    function += el  # continue to accumulate the function until meet something different from the number
                else:
                    number += el
                    if op:  # shot the operator if has been accumulated
                        yield op
                        op = ''
                    if function:  # shot the function if it has been accumulated
                        yield function
                        function = ''
            elif el in OPERATORS_BEGIN:  # operator processing
                if el in DOUBLE_OPER_PART1 and not op:  # if double operator is possible, add and wait
                    op += el
                elif el in DOUBLE_OPER_PART2 and op:  # found double
                    op += el
                    if number:  # shot number if it was accumulated
                        yield float(number) if number != '.' else '.'
                        number = ''
                    if function:  # shot the function if it has been accumulated
                        yield function
                        function = ''
                    yield op  # shot an double operator when it was accumulated
                    op = ''
                else:  # if the operator is single
                    if op:  # if it was accumulated at the previous step - shot, reset
                        yield op
                        op = ''
                    if number:  # shot number if it was accumulated
                        yield float(number) if number != '.' else '.'
                        number = ''
                    if function:  # shot the function if it has been accumulated
                        yield function
                        function = ''
                    yield el  # hit a single operator
                if number:  # shot number if it was accumulated
                    yield float(number) if number != '.' else '.'
                    number = ''
                if function:  # shot the function if it has been accumulated
                    yield function
                    function = ''
            elif el in PARENTHESES + (',',):  # handling brackets and commas (if a function with multiple arguments)
                if number:  # shot number if it was accumulated
                    yield float(number) if number != '.' else '.'
                    number = ''
                if function:  # shot the function if it has been accumulated
                    yield function
                    function = ''
                if op:  # shot the operator if has been accumulated
                    yield op
                    op = ''
                yield el  # shot brace or comma as soon as they are met

        if function:  # shot the function if it has been accumulated
            yield function
        if number:  # shot number if it was accumulated
            yield float(number) if number != '.' else '.'
        if op:  # shot the operator if it has been accumulated
            yield op

    def validate_parsed_list(self, parsed_list):
        """
        Validation of various errors before polish sorting

        :param parsed_list: list with tokens of pre-validated and parsed formula for validation
        :return: was_error
        """
        was_error = False
        counter = 0  # counter for parentheses
        was_number = False
        previous_el = ''

        if parsed_list[-1] in OPERATORS:
            print('ERROR: Operator at the end of the formula: "{}" '.format(parsed_list[-1]))
            was_error = True
        if parsed_list[0] in BINARY_OPERATORS:
            print('ERROR: Formula can not start with binary operator "{}"'.format(parsed_list[0]))
            was_error = True

        for el in parsed_list:
            counter = self._matched_parentheses(el, counter)

            message = 'ERROR: After {} element {} is forbidden!'.format(str(previous_el), str(el))

            if isinstance(el, float) or el in MATH_CONSTS and was_number is False:
                was_number = True

            if el == '.':
                print('ERROR: Single delimiter is prohibited in formula!')
                was_error = True

            if isinstance(el, str) and el[0] in LETTERS:
                if el.lower() not in ALL_FUNCTIONS_AND_CONSTS:
                    print('ERROR: Function or constant {} is not supported by calculator'.format(el))
                    was_error = True

            if previous_el == '(':
                if el in ((')', ',',) + tuple(BINARY_OPERATORS.keys())):
                    print(message)
                    was_error = True

            if previous_el == ')':
                if el in (('(',) + ALL_FUNCTIONS_AND_CONSTS) or isinstance(el, float):
                    print(message)
                    was_error = True

            if previous_el == ',':
                if el in (')', ',', '.'):
                    print(message)
                    was_error = True

            if previous_el in UNARY_OPERATORS:
                if el in ((')', ',',) + tuple(BINARY_OPERATORS.keys())):
                    print(message)

            if previous_el in BINARY_OPERATORS:
                if el in ((')', ',',) + tuple(BINARY_OPERATORS.keys())):
                    print(message)
                    was_error = True

            if previous_el in ALL_FUNCTIONS:
                if el != '(':
                    print(message)
                    was_error = True

            if isinstance(previous_el, float) or previous_el in MATH_CONSTS:
                if el in (('(',) + ALL_FUNCTIONS_AND_CONSTS) or isinstance(el, float):
                    print(message)
                    was_error = True

            previous_el = el

        if counter != 0:
            print('ERROR: Wrong number of opened or closed parentheses in formula!')
            was_error = True

        if was_number is False:
            print('ERROR: Formula does not contain numbers!')
            was_error = True

        return was_error

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
                is_unary_plus = ((processed_list and processed_list[-1]
                                  in (('(', ',') + tuple(BINARY_OPERATORS.keys()))) or not processed_list)
                if stack_str:
                    if '-' in stack_str:
                        if stack_str.count('-') % 2 == 0:  # count the number of minuses, replacing with plus or minus
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
        """
        Implementing polish sorting needed for calculating the result

        :param parsed_formula: list that passed validation with tokens of parsed formula
        :return: None
        """
        stack = []  # use list as stack
        previous_token = ''
        for token in parsed_formula:
            # if the element is an operator, then we send further all the operators from the stack,
            # whose priority is greater than or equal to the newcomer,
            # up to the opening bracket or the stack is empty.
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
                # if the element is a closing bracket, we give all the elements from the stack,
                # up to the opening bracket, and throw away the opening bracket out of the stack.
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                # if the element is an opening bracket, just put it to the stack
                stack.append(token)
            elif token == ",":  # end of argument
                # give all operators from the stack to the opening bracket
                while stack and stack[-1] != "(":
                    yield stack.pop()
            else:
                # if the element is a number or a constant, send it immediately to the output
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
        """
        Calculating the result after polish sorting

        :param polish_list: list that have been polish-sorted
        :return: stack[0]: the result of calculation
        """
        stack = []
        function_result = None

        for token in polish_list:
            if token in MATH_FUNCTIONS:
                arguments = []
                func_name = getattr(math, token)

                if func_name != math.log:
                    number_of_args = self._get_num_args(func_name)
                    for i in range(number_of_args):
                        if stack:
                            arguments.insert(0, stack.pop())
                else:
                    # since log has a changing number of arguments, separate processing
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

                stack.append(function_result)  # calculate the operator, return to the stack
                arguments = []

            elif token in BUILT_IN_FUNCTIONS:
                x = stack.pop()  # take one number from the stack
                func_name = getattr(builtins, token)
                stack.append(func_name(x))
            elif token in OPERATORS:  # if the incoming element is an operator,
                y, x = stack.pop(), stack.pop()  # pick up two numbers from the stack
                stack.append(OPERATORS[token][1](x, y))  # calculate the operator, return to the stack
            elif token in MATH_CONSTS:
                stack.append(getattr(math, token))
            else:
                stack.append(token)

        if len(stack) > 1:
            print('ERROR: Formula contains incorrect number of arguments in function.')

        return stack[0]  # the result of the calculation is the only item on the stack

    def launch_processing(self):
        """
        Launch of program

        :param self
        :return: None
        """
        parsed_list = []
        polish_list = []
        was_error = self.pre_validate(self.formula_string)
        if not was_error:
            for el in self.parse(self.formula_string):
                parsed_list.append(el)
            was_error = self.validate_parsed_list(parsed_list)
            if not was_error:
                parsed_list = self.process_unary_operations(parsed_list)
                for el in self.sort_to_polish(parsed_list):
                    polish_list.append(el)
                result = self.calc(polish_list)
                print(result)
