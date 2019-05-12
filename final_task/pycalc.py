#!/usr/bin/env python3
import re
import math
import argparse
import operator
from math import pi, e

parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
parser.add_argument('EXPRESSION', type=str, help='expression string to evaluate')
expr = parser.parse_args().EXPRESSION

MATH_FUNCTIONS = {name: (5, "left", getattr(math, name)) for name in dir(math)}
MATH_FUNCTIONS_NEG = {"-" + name: (5, "left", getattr(math, name)) for name in dir(math)}
OPERATORS = {
    '==': (1, "left", operator.eq), '<': (1, "left", operator.lt), '!=': (1, "left", operator.ne),
    '>': (1, "left", operator.gt), '<=': (1, "left", operator.le), '>=': (1, "left", operator.ge),
    '+': (2, "left", operator.add), '^': (4, "right", operator.pow), '-': (2, "left", operator.sub),
    '*': (3, "left", operator.mul), '/': (3, "left", operator.truediv), '//': (3, "left", operator.floordiv),
    '%': (3, "left", operator.mod), 'abs': (5, "left", operator.abs), '-abs': (5, "left", operator.abs),
    'round': (5, "left", lambda x: round(x)), '-round': (5, "left", lambda x: round(x))
}
NEW_DICTIONARY = dict(list(OPERATORS.items()) + list(MATH_FUNCTIONS.items()) + list(MATH_FUNCTIONS_NEG.items()))
arg_count = 0


def counting(expression):
    def checklog(expression):
        expression = re.sub(r'(?<=-)[+]+|[+]+(?=-)', "", expression)
        match = re.search(r'^[-]{2,}', expression)
        if match is not None:
            check_expr = match.group(0)
            len_pattern = len(check_expr)
            if len_pattern % 2 == 0:
                new_expression = re.sub(check_expr, "", expression)
                checklog(new_expression)
                return new_expression
            elif len_pattern % 2 != 0:
                new_expression = re.sub(check_expr, "-", expression)
                checklog(new_expression)
                return new_expression
        else:
            match = re.search(r'[-]{3,}', expression)
            if match is not None:
                check_expr = match.group(0)
                len_pattern = len(check_expr)
                if len_pattern % 2 == 0:
                    new_expression = re.sub(check_expr, "--", expression)
                    checklog(new_expression)
                    return new_expression
                elif len_pattern % 2 != 0:
                    new_expression = re.sub(check_expr, "-", expression)
                    checklog(new_expression)
                    return new_expression
            else:
                return expression

    def check_entrence(check_expr, mistake=False):
        check_expr = checklog(check_expr)
        if check_expr is "":
            return "ERROR: expression is empty."
        brackets_error = "ERROR: Brackets are not balanced."
        cut_str = re.findall(r'\(|\)', check_expr)
        if cut_str is not None:
            quantity = 0
            for index in cut_str:
                if index == '(':
                    quantity = quantity + 1
                elif index == ')':
                    quantity = quantity - 1
                if quantity < 0:
                    mistake = True
                    break
            if quantity != 0:
                mistake = True
        if mistake is True:
            return brackets_error

        left_space_error = "ERROR: You should remove left space(s)."
        check = re.findall(r'^\s+', check_expr)
        if check:
            return left_space_error

        non_arg_betw_digit_error = "ERROR: You have no operators or functions between digits."
        check = re.findall(r'\d\s+\d|\)\s+\d|\d\s+\(', check_expr)
        if check:
            return non_arg_betw_digit_error

        space_between_operator_error = "ERROR: You have to delete space(s) between the operator(s)."
        check = re.findall(r'(=\s+=)|(>\s+=)|(<\s+=)|(!\s+=)|(/\s+/)|(\w\s+\w)', check_expr)
        if check:
            return space_between_operator_error

        return calc(shunting_yard(parse(check_expr)))

    def define_args(tokens_operator):
        global quantity_arg
        quantity_arg = 0
        if tokens_operator.__name__ == '<lambda>':
            quantity_arg = tokens_operator.__code__.co_argcount
        else:
            match = re.search(r'\(.*\)', tokens_operator.__doc__)
            obj = re.search(r'\,', match.string)
            if obj is not None:
                for symbol in obj.group(0):
                    if symbol == ',':
                        quantity_arg += 1
            quantity_arg += 1
        return quantity_arg

    def parse(expression_string):
        number_re_neg = re.compile('^((-)?[0-9]+([.][0-9]+)?)|(-)?[0-9]*([.][0-9]+)')
        number_re_pos = re.compile('^([0-9]+([.][0-9]+)?)|([0-9]*([.][0-9]+))')
        list_for_reg_exp = [index for index in MATH_FUNCTIONS.keys()]
        list_for_reg_exp.sort(key=len, reverse=True)
        string_for_reg_exp = '{}'.format(' '.join('|({})'.format(index) for index in list_for_reg_exp))
        string_for_reg_exp_with_neg = '{}'.format(' '.join('(-?{})|'.format(index) for index in list_for_reg_exp))
        operators_or_functions_neg_to_compile = (
                '^' + string_for_reg_exp_with_neg + '(==)|(>=)|(<=)|(!=)|(-?abs)|(-?round)|(//)|[><()^%+*-/]').replace(
            ' ', '')
        operators_or_functions_pos_to_compile = (
                '^(==)|(>=)|(<=)|(!=)|(abs)|(round)|(//)|[><()^%+*-/]' + string_for_reg_exp).replace(' ', '')
        operators_or_functions_pos = re.compile(operators_or_functions_pos_to_compile)
        operators_or_functions_neg = re.compile(operators_or_functions_neg_to_compile)
        del_index = 0
        expression_string = expression_string.replace(' ', '')

        for index in range(len(expression_string)):
            if del_index:
                del_index -= 1
                continue
            if expression_string[index - 1].isdigit() is False or index == 0:
                number = number_re_neg.match(expression_string[index:])
            else:
                number = number_re_pos.match(expression_string[index:])
            if number:
                end = number.end()
                yield float(number.string[:end])
                del_index = end - 1
                continue
            else:
                if index == 0 or (
                        expression_string[index - 1].isdigit() is False and expression_string[index - 1] != ")"):
                    op = operators_or_functions_neg.match(expression_string[index:])
                else:
                    op = operators_or_functions_pos.match(expression_string[index:])
            if op:
                end = op.end()
                yield op.string[:end]
                del_index = end - 1

    def shunting_yard(parsed_expression):
        stack = []
        for token in parsed_expression:
            if token in MATH_FUNCTIONS:
                stack.append(token)
                global arg_count
                arg_count = 1
            elif token is ',':
                # out.append(stack.pop())
                arg_count += 1
                while stack[-1] != '(':
                    y = stack.pop()
                    yield y
            elif token in NEW_DICTIONARY:
                while stack and stack[-1] != "(" and ((NEW_DICTIONARY[token][1] is "left" and NEW_DICTIONARY[token][
                    0] <= NEW_DICTIONARY[stack[-1]][0]) or (NEW_DICTIONARY[token][1] is "right" and
                                                            NEW_DICTIONARY[token][0] < NEW_DICTIONARY[stack[-1]][0])):
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(polish):
        mistake_error = "ERROR:Invalid syntax"
        try:
            stack = []
            for token in polish:
                if token in NEW_DICTIONARY:
                    result = re.match(r'-?(pi|e|tau)', token)
                    if result is not None:
                        if result.group(0)[0] == "-":
                            stack.append(- + NEW_DICTIONARY[token][2])
                        else:
                            stack.append(NEW_DICTIONARY[token][2])
                    elif token == "log" or token == "-log":
                        if arg_count == 2:
                            y, x = stack.pop(), stack.pop()
                            if token[0] == "-":
                                stack.append(- + NEW_DICTIONARY[token][2](x, y))
                            else:
                                stack.append(NEW_DICTIONARY[token][2](x, y))
                        else:
                            x = stack.pop()
                            if token[0] == "-":
                                stack.append(- + NEW_DICTIONARY[token][2](x))
                            else:
                                stack.append(NEW_DICTIONARY[token][2](x))
                    elif token == "-":
                        y, x = stack.pop(), stack.pop()
                        stack.append(NEW_DICTIONARY[token][2](x, y))
                    else:
                        define_args(NEW_DICTIONARY[token][2])
                        if quantity_arg == 1:
                            x = stack.pop()
                            if token[0] == "-":
                                stack.append(- + NEW_DICTIONARY[token][2](x))
                            else:
                                stack.append(NEW_DICTIONARY[token][2](x))
                        elif quantity_arg == 2:
                            y, x = stack.pop(), stack.pop()
                            if token[0] == "-":
                                stack.append(- + NEW_DICTIONARY[token][2](x, y))
                            else:
                                stack.append(NEW_DICTIONARY[token][2](x, y))
                else:
                    stack.append(token)
            if len(stack) > 1:
                return "ERROR:Invalid syntax"
            else:
                return stack[0]
        except IndexError:
            return mistake_error

    return check_entrence(expression)


print(counting(expr))
