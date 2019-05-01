#!/usr/bin/env python3
import re
import math
import argparse
import operator

parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
parser.add_argument('EXPRESSION', type=str, help='expression string to evaluate')
expr = parser.parse_args().EXPRESSION

MATH_FUNCTIONS = {name: (4, getattr(math, name)) for name in dir(math)}
OPERATORS = {
    '==': (1, operator.eq), '<': (1, operator.lt), '!=': (1, operator.ne),
    '>': (1, operator.gt), '<=': (1, operator.le), '=>': (1, operator.ge),
    '+': (2, operator.add), '^': (3, operator.pow), '-': (2, operator.sub),
    '*': (3, operator.mul), '/': (3, operator.truediv), '//': (3, operator.floordiv),
    '%': (3, operator.mod), 'abs': (4, operator.abs),
    'round': (4, lambda x: round(x))
}
NEW_DICTIONARY = dict(list(OPERATORS.items()) + list(MATH_FUNCTIONS.items()))


def counting(expression):

    def check_entrence(check_expr, mistake=False):
        brackets_error = "ERROR: Brackets are not balanced."
        cut_str = re.findall(r'[^()]', check_expr)
        if cut_str is not None:
            quantity = 0
            for ind in cut_str:
                use_expr = check_expr.replace(ind, '')
            for ind in list(use_expr):
                if ind == '(':
                    quantity = quantity + 1
                elif ind == ')':
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

        return calc(shunting_yard(parse(expression)))

    def define_args(tokens_operator):
        global quantity_arg
        quantity_arg = 0
        if tokens_operator.__class__ == 'function':
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
        number_re_neg = re.compile('^(-)?[0-9]+([.][0-9]+)?')
        number_re_pos = re.compile('^[0-9]+([.][0-9]+)?')
        list_for_reg_exp = [i for i in MATH_FUNCTIONS.keys()]
        list_for_reg_exp.sort(key=len, reverse=True)
        string_for_reg_exp = '{}'.format(' '.join('|({})'.format(i) for i in list_for_reg_exp))
        operators_or_functions_to_compile = '^(==)|(>=)|(<=)|(!=)|(abs)|(round)|(//)|[><()^%+*-/]' + string_for_reg_exp
        operators_or_functions_to_compile = operators_or_functions_to_compile.replace(' ', '')
        operators_or_functions = re.compile(operators_or_functions_to_compile)
        del_index = 0
        expression_string.replace(' ', '')
        for i in range(len(expression_string)):
            if del_index:
                del_index -= 1
                continue
            if expression_string[i - 1].isdigit() is False or i == 0:
                number = number_re_neg.match(expression_string[i:])
            else:
                number = number_re_pos.match(expression_string[i:])
            if number:
                end = number.end()
                yield float(number.string[:end])
                del_index = end - 1
                continue
            else:
                op = operators_or_functions.match(expression_string[i:])
            if op:
                end = op.end()
                yield op.string[:end]
                del_index = end - 1

    def shunting_yard(parsed_expression):
        stack = []
        for token in parsed_expression:
            if token in NEW_DICTIONARY:
                while stack and stack[-1] != "(" and NEW_DICTIONARY[token][0] <= NEW_DICTIONARY[stack[-1]][0]:
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
        mistake_error = "ERROR: You have a mistake in your expression."
        try:
            stack = []
            for token in polish:
                if token in NEW_DICTIONARY:
                    define_args(NEW_DICTIONARY[token][1])
                    if quantity_arg == 1:
                        x = stack.pop()
                        stack.append(NEW_DICTIONARY[token][1](x))
                    elif quantity_arg == 2:
                        y, x = stack.pop(), stack.pop()
                        stack.append(NEW_DICTIONARY[token][1](x, y))
                else:
                    stack.append(token)
            return stack[0]
        except IndexError:
            return mistake_error

    return check_entrence(expression)


print(counting(expr))
