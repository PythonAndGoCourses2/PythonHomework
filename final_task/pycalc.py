#!/usr/bin/python

import argparse
import string
import math
import operator
import re


def pycalc(info_string):
    FUNCTIONS = {attr: getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))}
    FUNCTIONS['abs'], FUNCTIONS['round'], FUNCTIONS['lg'] = abs, round, math.log10
    """Math functions + build-in python functions"""

    OPERATORS = {
        '+': (operator.add, 2), '-': (operator.sub, 2), '*': (operator.mul, 3),
        '/': (operator.truediv, 3), '//': (operator.floordiv, 3), '%': (operator.mod, 3),
        '^': (operator.pow, 4), '=': (operator.eq, 0), '==': (operator.eq, 0),
        '<': (operator.lt, 0), '<=': (operator.le, 0), '!=': (operator.ne, 0),
        '>=': (operator.ge, 0), '>': (operator.gt, 0)}
    """Operators by priority """

    CONSTANTS = {'pi': math.pi, 'e': math.e, 'tau': math.tau}

    NUMBERS = re.compile(r'-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?')

    def split_brackets(tokensarray, token):
        """Function split brackets. For example: '((' -> '(','('."""
        if '(' in token or ')' in token:
            for brackets in token:
                tokensarray.append(brackets)

        else:
            tokensarray.append(token)

    def make_input_comfortable(the_input):
        """Make input information more usable for futher processing """
        if re.compile(r'[\d\w()]\s+[.\d\w()]').findall(the_input) \
                or re.compile(r'[+-/*%^=<>]$').findall(the_input) \
                or re.compile(r'^[/*%^=<>!]').findall(the_input) \
                or re.compile(r'[+-/*%^=<>]\)').findall(the_input) \
                or re.compile(r'[<>/*=!]\s+[=/*]').findall(the_input) \
                or re.compile(r'\(\)').findall(the_input):
            raise ValueError("Invalid expression")
        elif not the_input:
            raise ValueError("Empty field")
        elif the_input.count('(') != the_input.count(')'):
            raise ValueError("Brackets are not balanced")
        the_input = the_input.replace(' ', '')
        the_input = the_input.replace('log10(', 'lg(')
        while '++' in the_input or '--' in the_input or '+-' in the_input or '-+' in the_input:
            the_input = re.sub(r'\+\+', '+', the_input)
            the_input = re.sub(r'\+-', '-', the_input)
            the_input = re.sub(r'-\+', '-', the_input)
            the_input = re.sub(r'--', '+', the_input)
        return the_input

    def tokenize(comfortable_input):
        """Splitting information into tokens for the
           explict form of expression,functions and
           constants. """
        categories = [string.digits + '.', '(', ')' '//', '^', '+-*/%', '==', '<=', '>=', '!=', '>', '<',
                      string.ascii_lowercase]
        token = ''
        tokens_array = []
        category = None
        for char in comfortable_input:
            if token:
                if category and char in category:
                    token += char
                else:
                    split_brackets(tokens_array, token)
                    token = char
                    category = None
                    for subcategory in categories:
                        if char in subcategory:
                            category = subcategory
                            break
            else:
                category = None
                if not category:
                    for subcategory in categories:
                        if char in subcategory:
                            category = subcategory
                            break
                token += char
        if token:
            split_brackets(tokens_array, token)
        return tokens_array

    def negative_numbers(parse_information):
        """Working with negative numbers in parse information from command line"""

        for index, element in enumerate(parse_information):
            if element == '-' and (re.fullmatch(NUMBERS, parse_information[index + 1])):
                if parse_information[index - 1] in '(*/%//^,':
                    parse_information[index] += parse_information.pop(index + 1)
                elif parse_information.index(element) == 0:
                    parse_information[index] += parse_information.pop(index + 1)
                elif index == len(parse_information) - 2:
                    if re.search(NUMBERS, parse_information[index + 1]):
                        parse_information[index] += parse_information.pop(index + 1)
                        parse_information.insert(index, '+')
                elif parse_information[index + 2] in '*/%//' and re.search(NUMBERS, parse_information[index + 1]):
                    parse_information[index] += parse_information.pop(index + 1)
                    parse_information.insert(index, '+')
            elif element == '-' and (
                    parse_information[index + 1] in FUNCTIONS or parse_information[index + 1] in CONSTANTS) and \
                    parse_information[index - 1] == '(':
                parse_information[index] = '-1'
                parse_information.insert(index + 1, '*')
        return parse_information

    def check_function_and_constants(parse_information):
        """Checks functions or constants. Do the entered functions
         and constants coincide with those used in the process"""
        copy_check_expression = parse_information.copy()
        for index, element in enumerate(copy_check_expression):
            if index == len(copy_check_expression) - 1 and (element in FUNCTIONS):
                raise ValueError(f'function arguments not entered')
            elif (element in FUNCTIONS) and copy_check_expression[index + 1] != '(':
                raise ValueError(f'function arguments not entered')
            elif re.fullmatch(NUMBERS, element):
                copy_check_expression.pop(index)
        difference = set(copy_check_expression).difference(
            set(FUNCTIONS),
            set(OPERATORS),
            set(CONSTANTS),
            set(string.digits),
            {'{', '[', '(', ',', ')', ']', '}'},
            {'True', 'False'}
        )
        if difference:
            raise ValueError(f'unknown function or constant {difference}')
        else:
            return parse_information

    def polish_notation(parsed_information):
        """Function translate parsed information to RPN"""
        stack = []
        reverse_polish_notation = ''
        separator = ' '
        for token in parsed_information:
            if re.fullmatch(NUMBERS, token) and float(token) >= 0:
                reverse_polish_notation += token + separator
            elif re.fullmatch(NUMBERS, token) and float(token) < 0:
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
            elif token in FUNCTIONS:
                stack.append(token)
            elif token in OPERATORS:
                if not stack:
                    stack.append(token)
                elif token == stack[-1] and token == '^':
                    stack.append(token)
                elif stack[-1] == '(':
                    stack.append(token)
                elif stack[-1] in FUNCTIONS:
                    reverse_polish_notation += stack.pop() + separator
                    if not stack:
                        stack.append(token)
                    elif stack[-1] in OPERATORS:
                        if OPERATORS[token][-1] <= OPERATORS[stack[-1]][-1]:
                            reverse_polish_notation += stack.pop() + separator
                            stack.append(token)
                        elif OPERATORS[token][-1] > OPERATORS[stack[-1]][-1]:
                            stack.append(token)
                elif token == '-' and parsed_information[parsed_information.index(token) - 1] in '/*^%//':
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

    def arguments(math_function):
        """Determines how many arguments function includes."""

        spec = math_function.__doc__.split('\n')[0]
        arg = spec[spec.find('(') + 1:spec.find(')')]
        return arg.count(',') + 1 if arg else 0

    def calculate(polish_information):
        stack = [0]
        for token in polish_information.split(' '):
            if token in OPERATORS:
                op2, op1 = stack.pop(), stack.pop()
                stack.append(OPERATORS[token][0](op1, op2))
            elif token in FUNCTIONS:
                if arguments(FUNCTIONS[token]) == 1:
                    op = stack.pop()
                    if stack[-1] == ',':
                        raise ValueError("Invalid number of arguments")
                    stack.append(FUNCTIONS[token](op))
                elif arguments(FUNCTIONS[token]) == 2:
                    if stack[-2] == ',':
                        op2 = stack.pop()
                        stack.pop()
                        op1 = stack.pop()
                        if stack[-1] == ',':
                            raise ValueError("Invalid number of arguments")
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

    return calculate(polish_notation(check_function_and_constants(
        negative_numbers(tokenize(make_input_comfortable(info_string))))))


def main():
    try:
        parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
        parser.add_argument("EXPRESSION", help="expression string to evaluate", type=str)
        args = parser.parse_args()
        print(pycalc(args.EXPRESSION))
    except Exception as exeption:
        print(f'ERROR: {exeption}')


if __name__ == '__main__':
    main()
