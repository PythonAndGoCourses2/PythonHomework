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
    ALL_NUMBERS: possible representations of a numbers like -.5, -0.5, -5, 0.5, .5, 5, 1e-05;
    INVALID_EXPRESSIONS: list of  possible representations of a invalid expression.

"""

import argparse
import math
import operator
import re
from json import loads
from typing import List, TypeVar, Union
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
    'inf': math.inf,
    'nan': math.inf
}
ALL_NUMBERS = re.compile(r'-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?')
INVALID_EXPRESSIONS = [
    r'[\d\w()]\s+[.\d\w()]',
    r'[+-/*%^=<>]$',
    r'^[/*%^=<>!]',
    r'[+-/*%^=<>]\)',
    r'[<>/*=!]\s+[=/*]',
    r'\(\)'
]


def py_calculator(math_expression: str) -> Union[int, float, bool, tuple]:
    """

    :param math_expression: String of math expression
    :return: Result of calculation

    """
    elements_of_expression = TypeVar('elements_of_expression')

    def parse(expression: str) -> List[elements_of_expression]:
        """Split math expression, consists of 2 steps

        :param expression: String of math expression
        :return: Parsed line by items in the list

        """
        def parse_step1(expr: str) -> List[elements_of_expression]:
            """Creates a list with numbers, functions and constants from a mathematical expression

            :param expr: String of math expression
            :return: List with items of expression
            :raises: ValueError if nothing entered or invalid expression

            """
            # this regular expression contains all possible elements of the expression,
            # such as numbers, constants, functions, brackets, operators
            items_of_expression = r'(?:(?:[a-zA-Z]+[\d]+[\w]?' \
                                  r'|[a-zA-Z_]+)' \
                                  r'|(?:\d+(?:\.\d*)?' \
                                  r'|\.\d+)(?:[eE][-+]?\d+)?' \
                                  r'|[,+\-/*%^=<>!][=/]?|[(:)])'
            for invalid_expr in INVALID_EXPRESSIONS:
                if re.search(invalid_expr, expr):
                    raise ValueError(f'invalid expression')
            if not expr:
                raise ValueError(f'nothing entered')
            expr = expr.replace(' ', '')
            while '++' in expr or '--' in expr or '+-' in expr or '-+' in expr:
                expr = re.sub(r'\+\+', '+', expr)
                expr = re.sub(r'\+-', '-', expr)
                expr = re.sub(r'-\+', '-', expr)
                expr = re.sub(r'--', '+', expr)
            parse_list = re.compile(items_of_expression).findall(expr)
            return parse_list

        def parse_step2(parse_list: List[elements_of_expression]) -> List[elements_of_expression]:
            """Working with minuses in expression.

            :param parse_list: List with items of expression.
            :return: Updated list.

            """

            for index, element in enumerate(parse_list):
                if element == '-' and re.fullmatch(ALL_NUMBERS, parse_list[index + 1]):
                    if parse_list[index - 1] in '(*/%//^,':
                        parse_list[index] += parse_list.pop(index + 1)
                    elif index == len(parse_list) - 2:
                        if re.search(ALL_NUMBERS, parse_list[index + 1]):
                            parse_list[index] += parse_list.pop(index + 1)
                            parse_list.insert(index, '+')
                    elif parse_list[index + 2] in '*/%//' and re.search(ALL_NUMBERS, parse_list[index + 1]):
                        parse_list[index] += parse_list.pop(index + 1)
                        parse_list.insert(index, '+')
                elif element == '-' and parse_list[index + 1] in FUNCTIONS and parse_list[index - 1] == '(':
                    parse_list[index] = '-1'
                    parse_list.insert(index + 1, '*')
            return parse_list
        return parse_step2(parse_step1(expression))

    def check_expression(parse_expression: List[elements_of_expression]):
        """Contains functions that validate the input expression.

        :param parse_expression: List with items of expression
        :return: List with expression elements if the expression passed all checks

        """
        def check_operators(parse_list: List[elements_of_expression]):
            """Checks the validity of the entered operators.

            :param parse_list: List with items of expression.
            :raise: ValueError if operators follow each other.

            """

            for index, element in enumerate(parse_list):
                if element in OPERATORS and parse_list[index + 1] in OPERATORS and parse_list[index + 1] != '-':
                    raise ValueError(f'unknown operation {element + parse_list[index + 1]}')
            return parse_list

        def check_function_and_constants(parse_list: List[elements_of_expression]):
            """Checks the validity of the entered functions or constants

            :param parse_list: List with items of expression.
            :raise: ValueError if functions or constants are not supported by a calculator or are incorrectly entered.

            """
            copy_parse_expression = parse_list.copy()
            for index, element in enumerate(copy_parse_expression):
                if index == len(copy_parse_expression) - 1 and (element in FUNCTIONS or element in BUILT_IN_FUNCTION):
                    raise ValueError(f'function arguments not entered')
                elif (element in FUNCTIONS or element in BUILT_IN_FUNCTION) and copy_parse_expression[index + 1] != '(':
                    raise ValueError(f'function arguments not entered')
                elif re.fullmatch(ALL_NUMBERS, element):
                    copy_parse_expression.pop(index)
            diff = set(copy_parse_expression).difference(
                                                    set(FUNCTIONS),
                                                    set(OPERATORS),
                                                    set(CONSTANTS),
                                                    set(BUILT_IN_FUNCTION),
                                                    {'{', '[', '(', ',', ':', ')', ']', '}'},
                                                    {'True', 'False', 'abs_tol', 'rel_tol'},
                                                    )
            if diff:
                raise ValueError(f'unknown function or constant {diff}')
            else:
                return parse_list

        def check_brackets(parse_list: List[elements_of_expression]):
            """Check count of '(',')'.

            :param parse_list: List with items of expression.
            :raise: ValueError if amount '(' not equal to quantity ')' in expression

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

    def exec_isclose(parse_list: List[elements_of_expression]):
        """calculates the mathematical function isclose

        :param parse_list: List with items of expression.
        :return: List with isclose function result.
        :raise: ValueError if entered invalid number of arguments.
        """
        arguments = []
        for element in parse_list:
            if element == 'isclose':
                for argument in parse_list:
                    if re.fullmatch(ALL_NUMBERS, argument):
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

    def transform_to_polish_notation(parse_expression: List[elements_of_expression]) -> str:
        """

        :param parse_expression: list after parsing
        :return: string in reverse polish notation

        """
        stack = []
        reverse_polish_notation = ''
        separator = ' '
        for token in parse_expression:
            if re.fullmatch(ALL_NUMBERS, token) and float(token) >= 0:
                reverse_polish_notation += token + separator
            elif re.fullmatch(ALL_NUMBERS, token) and float(token) < 0:
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
            elif token in ['(', ':']:
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

    def quantity_of_arguments(function: str) -> int:
        """From the description of the function determines how many arguments it includes

        :param function: mathematical or numerical functions
        :return: quantity of arguments

        """
        spec = function.__doc__.split('\n')[0]
        args = spec[spec.find('(') + 1:spec.find(')')]
        return args.count(',') + 1 if args else 0

    def calculate(reverse_polish_notation: str) -> Union[int, float, bool, tuple]:
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
                        for index, number in enumerate(stack[::-1]):
                            if isinstance(number, (int, float)) and stack[::-1][1] == ',':
                                numbers.append(stack.pop()), stack.pop()
                            elif len(stack) > index + 2:
                                if isinstance(stack[::-1][index + 2], (int, float)) and stack[::-1][3] == ',':
                                    numbers.append(stack.pop(-3)), stack.pop(), stack.pop(), stack.pop()
                        if stack[-1] == ':':
                            numbers.append(stack.pop(-3)), stack.pop(), stack.pop()
                        else:
                            numbers.append(stack.pop())
                        stack.extend([numbers])
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
            elif token in [',', ':']:
                stack.append(token)
            elif token in CONSTANTS:
                stack.append(CONSTANTS[token])
            elif token in ('True', 'False'):
                stack.append(loads(token.lower()))
            elif re.search(ALL_NUMBERS, token):
                stack.append(float(token))
        if isinstance(stack[-1], bool):
            return stack.pop()
        elif isinstance(stack[-1], int):
            return stack.pop()
        elif isinstance(stack[-1], tuple):
            return stack.pop()
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
