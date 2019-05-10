"""

The module calculates mathematical expressions.

Functions:
    py_calculator: consists of 4 stages(parse, check expression, transform to polish notation, calculate);
    parse: split an expression into numbers, functions, constants, operations;
    check_expression: validates the expression entered;
    transform_to_polish_notation: converts expressions according to the rules of reverse polish notation;
    calculate: calculates expressions written in reverse polish notation.

Attributes:
    OPERATORS : dictionary of operations and their priority;
    BUILT_IN_FUNCTION: dictionary of numeric functions;
    FUNCTIONS: dictionary of mathematical functions;
    CONSTANTS: dictionary of mathematical constants;
    LOGIC_OPERATORS: list of logical operator character;
    NEGATIVE_FLOAT_TYPE1: possible representations of a negative float number like -.5;
    NEGATIVE_FLOAT_TYPE2: possible representations of a negative float number like -0.5;
    NEGATIVE_INTEGER: possible representations of a negative integer number like -5;
    FLOAT_TYPE1: possible representations of a float number like 0.5;
    FLOAT_TYPE2: possible representations of a float number like .5;
    INTEGER: possible representations of a integer number like 5;

"""

import argparse
import math
import operator
import string
import re
from json import loads

OPERATORS = {
    '+': (operator.add, 2),
    '-': (operator.sub, 2),
    '*': (operator.mul, 3),
    '/': (operator.truediv, 3),
    '//': (operator.floordiv, 3),
    '%': (operator.mod, 3),
    '^': (operator.pow, 4),
    '=': (operator.eq, 0),
    '==': (operator.eq, 0),
    '<': (operator.lt, 0),
    '<=': (operator.le, 0),
    '!=': (operator.ne, 0),
    '>=': (operator.ge, 0),
    '>': (operator.gt, 0),
}

BUILT_IN_FUNCTION = {
    'abs': abs,
    'round': round
}

FUNCTIONS = {attr: getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))}

CONSTANTS = {
    'e': math.e,
    'pi': math.pi,
    'tau': math.tau,
    '-e': -math.e,
    '-pi': -math.pi,
    '-tau': -math.tau,
    'inf': math.inf,
    '-inf': -math.inf,
    'nan': math.inf
}

LOGIC_OPERATORS = ['=', '!', '<', '>']

NEGATIVE_FLOAT_TYPE1 = re.compile(r'^-\.\d+$')
NEGATIVE_FLOAT_TYPE2 = re.compile(r'^-\d+\.\d+$')
NEGATIVE_INTEGER = re.compile(r'^-\d+$')
FLOAT_TYPE1 = re.compile(r'^\d+\.\d+$')
FLOAT_TYPE2 = re.compile(r'^\.\d+$')
INTEGER = re.compile(r'^\d+$')


def py_calculator(math_expression):
    """

    :param math_expression: String of mathematic expression
    :return: Result of calculation

    """
    def parse(expression: str) -> list:
        """Split mathematic expression, consists of four  steps

        :param expression: String of mathematic expression
        :return: Parsed line by items in the list

        """
        def parse_step1(expr: str) -> list:
            """Сreates a list with numbers, functions and constants from a mathematical expression

            :param expr: String of math expression
            :return: List with items of expression
            :raises: ValueError if nothing entered or invalid expression

            """
            parse_list = []
            number, function = '', ''
            if re.compile(r'[\d\w()]\s+[.\d\w()]').findall(expr) \
                    or re.compile(r'[+-/*%^=<>]$').findall(expr) \
                    or re.compile(r'^[/*%^=<>!]').findall(expr) \
                    or re.compile(r'[+-/*%^=<>]\)').findall(expr) \
                    or re.compile(r'[<>/*=!]\s+[=/*]').findall(expr) \
                    or re.compile(r'\(\)').findall(expr):
                raise ValueError(f'invalid expression')
            elif not expr:
                raise ValueError(f'nothing entered')
            for element in expr:
                if element in string.ascii_letters or element == '_':
                    function += element
                elif element in string.digits or element == '.':
                    number += element
                    parse_list.append(function)
                    function = ''
                elif element in OPERATORS or element in LOGIC_OPERATORS or element in ['(', ',', ')']:
                    parse_list.extend([function, number, element])
                    number, function = '', ''
            if number:
                parse_list.append(number)
            elif function:
                parse_list.append(function)
            return list(filter(None, parse_list))

        def parse_step2(parse_list: list) -> list:
            """Finishes the parsing functions and collects logical operators and //.

            :param parse_list: List with items of expression
            :return: Updated list.
            :raise: ValueError if function arguments not entered

            """
            try:
                for index, element in enumerate(parse_list):
                    if element == 'log' and parse_list[index + 1] == 'p' and parse_list[index + 2] == '1':
                        parse_list[index] += parse_list.pop(index + 2) + parse_list.pop(index + 1)
                    elif (element in FUNCTIONS or element in BUILT_IN_FUNCTION) and parse_list[index + 1] != '(':
                        parse_list[index] += parse_list.pop(index + 1)
                    elif element == 'expm' and parse_list[index + 1] == '1':
                        parse_list[index] += parse_list.pop(index + 1)
                    elif element == '/' and parse_list[index + 1] == '/':
                        parse_list[index] += parse_list.pop(index + 1)
                    elif element in LOGIC_OPERATORS and parse_list[index + 1] == '=':
                        parse_list[index] += parse_list.pop(index + 1)
            except IndexError:
                raise ValueError(f'function arguments not entered')
            else:
                return parse_list

        def parse_step3(parse_list: list) -> list:
            """Converts multiple + and -.

            :param parse_list: List with items of expression.
            :return: Updated list.

            """
            for _ in range(len(parse_list)):
                for index, element in enumerate(parse_list):
                    if element == '-' and parse_list[index + 1] == '-' \
                            or element == '+' and parse_list[index + 1] == '+':
                        parse_list[index] = '+'
                        parse_list.pop(index + 1)
                    elif element == '+' and parse_list[index + 1] == '-' \
                            or element == '-' and parse_list[index + 1] == '+':
                        parse_list[index] = '-'
                        parse_list.pop(index + 1)
            return parse_list

        def parse_step4(parse_list: list) -> list:
            """Working with minuses in expression.

            :param parse_list: List with items of expression.
            :return: Updated list.

            """
            try:
                for index, element in enumerate(parse_list):
                    if element == '-' and (parse_list[index + 1].isdigit()
                                           or parse_list[index + 1].replace('.', '', 1).isdigit()
                                           or parse_list[index + 1] in CONSTANTS):
                        if parse_list[index - 1] in '(*/%//^,':
                            parse_list[index] += parse_list.pop(index + 1)
                        elif parse_list.index(element) == 0:
                            parse_list[index] += parse_list.pop(index + 1)
                        elif parse_list[index + 2] in '*/%//':
                            parse_list[index] += parse_list.pop(index + 1)
                            parse_list.insert(index, '+')
                    elif element == '-' and parse_list[index + 1] in FUNCTIONS and parse_list[index - 1] == '(':
                        parse_list[index] = '-1'
                        parse_list.insert(index + 1, '*')
            except IndexError:
                pass
            finally:
                return parse_list
        return parse_step4(parse_step3(parse_step2(parse_step1(expression))))

    def check_expression(parse_expression):
        """Contains functions that validate the input expression.

        :param parse_expression: List with items of expression
        :return: List with expression elements if the expression passed all checks

        """
        def check_operators(parse_list):
            """Checks the validity of the entered operators.

            :param parse_list: List with items of expression.
            :raise: ValueError if operators follow each other.

            """

            for index, element in enumerate(parse_list):
                if element in OPERATORS and parse_list[index + 1] in OPERATORS and parse_list[index + 1] != '-':
                    raise ValueError(f'unknown operation {element + parse_list[index + 1]}')
            return parse_list

        def check_function_and_constants(parse_list):
            """Checks the validity of the entered functions or constants

            :param parse_list: List with items of expression.
            :raise: ValueError if functions or constants are not supported by a calculator or are incorrectly entered.

            """
            copy_parse_expression = parse_list.copy()
            for index, element in enumerate(copy_parse_expression):
                if element == ''.join(INTEGER.findall(element)) \
                        or element == ''.join(FLOAT_TYPE1.findall(element)) \
                        or element == ''.join(FLOAT_TYPE2.findall(element)) \
                        or element == ''.join(NEGATIVE_INTEGER.findall(element)) \
                        or element == ''.join(NEGATIVE_FLOAT_TYPE1.findall(element)) \
                        or element == ''.join(NEGATIVE_FLOAT_TYPE2.findall(element)):
                    copy_parse_expression.pop(index)
            diff = set(copy_parse_expression).difference(
                                                    set(FUNCTIONS),
                                                    set(OPERATORS),
                                                    set(CONSTANTS),
                                                    set(BUILT_IN_FUNCTION),
                                                    set(string.digits),
                                                    {'{', '[', '(', ',', ')', ']', '}'},
                                                    {'True', 'False', 'abs_tol', 'rel_tol'}
                                                    )
            if diff:
                raise ValueError(f'unknown function or constant {diff}')
            else:
                return parse_list

        def check_brackets(parse_list):
            """Check count of '(',')'.

            :param parse_list: List with items of expression.
            :raise: ValueError if Amount '(' not equal to quantity ')' in expression

            """
            if parse_list.count('(') != parse_list.count(')'):
                raise ValueError(f'brackets are not balanced')
            else:
                return parse_list

        return check_operators(check_brackets(check_function_and_constants(parse_expression)))

    class FuncIsclose:
        def __init__(self, arg1, arg2, arg3=1e-09, arg4=0.0):
            self.arg1 = arg1
            self.arg2 = arg2
            self.rel_tol = arg3
            self.abs_tol = arg4

        def calc(self):
            return math.isclose(self.arg1, self.arg2, rel_tol=self.rel_tol, abs_tol=self.abs_tol)

    def exec_isclose(parse_list):
        """calculates the mathematical function isclose

        :param parse_list: List with items of expression.
        :return: List with isclose function result.
        :raise: ValueError if entered invalid number of arguments.
        """
        arguments = []
        for element in parse_list:
            if element == 'isclose':
                for argument in parse_list:
                    if argument == ''.join(INTEGER.findall(argument)) \
                            or argument == ''.join(FLOAT_TYPE1.findall(argument)) \
                            or argument == ''.join(FLOAT_TYPE2.findall(argument)) \
                            or argument == ''.join(NEGATIVE_INTEGER.findall(argument)) \
                            or argument == ''.join(NEGATIVE_FLOAT_TYPE1.findall(argument)) \
                            or argument == ''.join(NEGATIVE_FLOAT_TYPE2.findall(argument)):
                        arguments.append(float(argument))
                if len(arguments) == 1 or len(arguments) > 4:
                    raise ValueError(f'invalid number of arguments')
                elif len(arguments) == 2:
                    isclose = FuncIsclose(arguments[0], arguments[1])
                    return [str(isclose.calc())]
                elif len(arguments) == 3:
                    isclose = FuncIsclose(arguments[0], arguments[1], arguments[2])
                    return [str(isclose.calc())]
                elif len(arguments) == 4:
                    isclose = FuncIsclose(arguments[0], arguments[1], arguments[2], arguments[3])
                    return [str(isclose.calc())]
            else:
                return parse_list

    def transform_to_polish_notation(parse_expression: list) -> str:
        """

        :param parse_expression: list after parsing
        :return: string in reverse polish notation

        """
        stack = []
        reverse_polish_notation = ''
        separator = ' '
        for token in parse_expression:
            if token == ''.join(INTEGER.findall(token)) \
                    or token == ''.join(FLOAT_TYPE1.findall(token)) \
                    or token == ''.join(FLOAT_TYPE2.findall(token)):
                reverse_polish_notation += token + separator
            elif token == ''.join(NEGATIVE_INTEGER.findall(token)) \
                    or token == ''.join(NEGATIVE_FLOAT_TYPE1.findall(token)) \
                    or token == ''.join(NEGATIVE_FLOAT_TYPE2.findall(token)):
                # writes a negative number of -5 in the form of 0 5 -, according to the rules of the reverse notation
                reverse_polish_notation += '0' + separator + token[1:] + separator + token[0] + separator
            elif token == ')':
                for element in stack[::-1]:
                    if element == '(':
                        break
                    reverse_polish_notation += stack.pop() + separator
                stack.pop()
            elif token == ',':
                for element in stack[::-1]:
                    if element == '(':
                        break
                    reverse_polish_notation += stack.pop() + separator
                reverse_polish_notation += token + separator
            elif token == '(':
                stack.append(token)
            elif token in FUNCTIONS or token in BUILT_IN_FUNCTION:
                stack.append(token)
            elif token in OPERATORS:
                if not stack:
                    stack.append(token)
                elif token == stack[-1] and token == '^':
                    stack.append(token)
                elif stack[-1] == '(':
                    stack.append(token)
                elif stack[-1] in FUNCTIONS or stack[-1] in BUILT_IN_FUNCTION:
                    reverse_polish_notation += stack.pop() + separator
                    if not stack:
                        stack.append(token)
                    elif stack[-1] in OPERATORS:
                        if OPERATORS[token][-1] <= OPERATORS[stack[-1]][-1]:
                            reverse_polish_notation += stack.pop() + separator
                            stack.append(token)
                        elif OPERATORS[token][-1] > OPERATORS[stack[-1]][-1]:
                            stack.append(token)
                elif token == '-' and parse_expression[parse_expression.index(token) - 1] in '/*^%//':
                    if OPERATORS[token][-1] <= OPERATORS[stack[-1]][-1]:
                        stack.append(token)
                        reverse_polish_notation += '0' + separator
                elif OPERATORS[token][-1] <= OPERATORS[stack[-1]][-1]:
                    reverse_polish_notation += stack.pop() + separator
                    if stack:
                        if stack[-1] == '(':
                            stack.append(token)
                        elif OPERATORS[token][-1] <= OPERATORS[stack[-1]][-1]:
                            reverse_polish_notation += stack.pop() + separator
                            stack.append(token)
                        elif OPERATORS[token][-1] > OPERATORS[stack[-1]][-1]:
                            stack.append(token)
                    elif not stack:
                        stack.append(token)
                else:
                    stack.append(token)
            elif token in CONSTANTS:
                reverse_polish_notation += token + separator
            elif token in ('True', 'False'):
                reverse_polish_notation += token + separator
        while stack:
            reverse_polish_notation += stack.pop() + separator
        return reverse_polish_notation

    def quantity_of_arguments(function):
        """From the description of the function determines how many arguments it includes

        :param function: mathematical or numerical functions
        :return: quantity of arguments

        """
        spec = function.__doc__.split('\n')[0]
        args = spec[spec.find('(') + 1:spec.find(')')]
        return args.count(',') + 1 if args else 0

    def calculate(reverse_polish_notation):
        stack = [0]
        for token in reverse_polish_notation.split(' '):
            if token in OPERATORS:
                op2, op1 = stack.pop(), stack.pop()
                stack.append(OPERATORS[token][0](op1, op2))
            elif token in BUILT_IN_FUNCTION:
                if stack[-2] == ',':
                    op2 = stack.pop()
                    stack.pop()
                    op1 = stack.pop()
                    if stack[-1] == ',':
                        raise ValueError(f'invalid number of arguments')
                    else:
                        stack.append(BUILT_IN_FUNCTION[token](op1, int(op2)))
                else:
                    op = stack.pop()
                    stack.append(BUILT_IN_FUNCTION[token](op))
            elif token in FUNCTIONS:
                if quantity_of_arguments(FUNCTIONS[token]) == 1:
                    if token == 'fsum':
                        numbers = []
                        for number in stack[::-1]:
                            if isinstance(number, (int, float)) and stack[::-1][1] == ',':
                                numbers.append(stack.pop())
                                stack.pop()
                            elif stack[::-1][0] == ',' and isinstance(number, (int, float)):
                                raise ValueError(f'invalid expression')
                        numbers.append(stack.pop())
                        stack.append(numbers)
                        op = stack.pop()
                        stack.append(FUNCTIONS[token](op))
                        numbers.clear()
                    else:
                        op = stack.pop()
                        if stack[-1] == ',':
                            raise ValueError(f'invalid number of arguments')
                        stack.append(FUNCTIONS[token](op))
                elif quantity_of_arguments(FUNCTIONS[token]) == 2:
                    if stack[-2] == ',':
                        op2 = stack.pop()
                        stack.pop()
                        op1 = stack.pop()
                        if stack[-1] == ',':
                            raise ValueError(f'invalid number of arguments')
                        elif token == 'ldexp':
                            stack.append(FUNCTIONS[token](op1, int(op2)))
                        elif token == 'gcd':
                            stack.append(FUNCTIONS[token](int(op1), int(op2)))
                        else:
                            stack.append(FUNCTIONS[token](op1, op2))
                    else:
                        op = stack.pop()
                        stack.append(FUNCTIONS[token](op))
            elif token == ',':
                stack.append(token)
            elif token in CONSTANTS:
                stack.append(CONSTANTS[token])
            elif token in ('True', 'False'):
                stack.append(loads(token.lower()))
            elif token.isdigit() or token.replace('.', '', 1).isdigit() or token.replace('-', '', 1).isdigit():
                stack.append(float(token))
        if isinstance(stack[-1], bool):
            return stack.pop()
        elif isinstance(stack[-1], int):
            return stack.pop()
        elif isinstance(stack[-1], tuple):
            return stack.pop()
        elif stack[-1].is_integer():
            return int(stack.pop())
        else:
            return stack.pop()
    return calculate(transform_to_polish_notation(exec_isclose(check_expression(parse(math_expression)))))


def main():
    try:
        parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
        parser.add_argument('EXPRESSION', type=str, help='expression string to evaluate')
        args = parser.parse_args()
        result = py_calculator(args.EXPRESSION)
        print(result)
    except Exception as exp:
        print(f'ERROR: {exp}')


if __name__ == '__main__':
    main()
