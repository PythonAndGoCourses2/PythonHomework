#!/usr/bin/python3

import operator
import math
import sys
import argparse


def arg_parser():
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.', prog='pycalc')
    parser.add_argument(
        '-m',
        '--use-modules',
        help='additional modules to use',
        metavar='MODULE [MODULE ...]'
    )
    parser.add_argument(
        'EXPRESSION', help='expression string to calculate'
    )
    expression_line = parser.parse_args().EXPRESSION
    return expression_line


function_dict = {
    'abs': {'operator': abs, 'priority': 0},
    'round': {'operator': round, 'priority': 0}
}
for k, v in math.__dict__.items():
    if k.startswith('_'):
        continue
    function_dict[k] = {'operator': v, 'priority': 0}


operator_dict = {
    '+': {'operator': operator.add, 'priority': 3},
    '-': {'operator': operator.sub, 'priority': 3},
    '/': {'operator': operator.truediv, 'priority': 2},
    '*': {'operator': operator.mul, 'priority': 2},
    '%': {'operator': operator.mod, 'priority': 2},
    '//': {'operator': operator.floordiv, 'priority': 2},
    '^': {'operator': operator.pow, 'priority': 1},
    '==': {'operator': operator.eq, 'priority': 4},
    '!=': {'operator': operator.ne, 'priority': 4},
    '>': {'operator': operator.gt, 'priority': 4},
    '<': {'operator': operator.lt, 'priority': 4},
    '>=': {'operator': operator.ge, 'priority': 4},
    '<=': {'operator': operator.le, 'priority': 4},
}


def check_expression(expression_line):
    if not expression_line:
        raise SyntaxError('Expression cannot be empty')
    if expression_line[-1] in operator_dict.keys():
        raise SyntaxError('Extra operator {} at the end of an expression!'.format(expression_line[-1]))
    if expression_line.count('(') < expression_line.count(')'):
        raise SyntaxError('Opening bracket required!')
    elif expression_line.count('(') > expression_line.count(')'):
        raise SyntaxError('Closing bracket required!')
    return True


def check_converted_list(converted_list):
    if len(converted_list) == 1:
        if type(converted_list[0]) is int or type(converted_list[0]) is float:
            return True
        raise SyntaxError('Expression must include at list one operand or one function with arguments!')
    return True


def number_parser(number):
    try:
        return int(number)
    except ValueError:
        return float(number)


def function_parser(function_name):
    if function_name == 'e' or function_name == 'pi':
        return function_dict[function_name]['operator']
    elif function_name == 'tau':
        if sys.version_info >= (3, 6):
            return function_dict[function_name]['operator']
        else:
            return 2 * function_dict['e']['operator']
    elif function_name in function_dict.keys():
        return function_name
    else:
        raise SyntaxError('There is no function with this name {}!'.format(function_name))


def split_operators(expression_line):
    parsing_list = []
    last_number = ""
    last_letter = ""
    last_symbol = ""
    blank_item = False
    if check_expression(expression_line):
        for i in expression_line:
            if i == " ":
                blank_item = True
                if last_symbol:
                    parsing_list.append(last_symbol)
                    last_symbol = ""
                elif last_number:
                    parsing_list.append(number_parser(last_number))
                    last_number = ""
                elif last_letter:
                    parsing_list.append(function_parser(last_letter))
                    last_letter = ""
            if i.isnumeric() or i is '.':
                if blank_item and type(parsing_list[-1]) is not str:
                    raise SyntaxError('Blank symbol between two operands!')
                elif blank_item:
                    blank_item = False
                if last_symbol:
                    parsing_list.append(last_symbol)
                    last_symbol = ""
                if last_letter:
                    last_letter += i
                else:
                    if '.' in last_number and i == '.':
                        raise SyntaxError('Typo in the operand (two comma)!')
                    else:
                        last_number += i
            elif i.isalpha():
                if last_symbol:
                    parsing_list.append(last_symbol)
                    last_symbol = ""
                last_letter += i
            elif i in "!=<>/":
                if blank_item and str(parsing_list[-1]) in '!=<>/*':
                    raise SyntaxError('Blank symbol between twice operator')
                elif blank_item:
                    blank_item = False
                if last_number:
                    parsing_list.append(number_parser(last_number))
                    last_number = ""
                if last_letter:
                    parsing_list.append(function_parser(last_letter))
                    last_letter = ""
                last_symbol += i
            else:
                if last_number:
                    parsing_list.append(number_parser(last_number))
                    last_number = ""
                if last_letter:
                    parsing_list.append(function_parser(last_letter))
                    last_letter = ""
                if last_symbol:
                    parsing_list.append(last_symbol)
                    last_symbol = ""
                if i != ' ':
                    parsing_list.append(i)
        if last_number:
            parsing_list.append(number_parser(last_number))
        elif last_letter:
            parsing_list.append(function_parser(last_letter))
    return parsing_list


def clean_add_sub_operators(last_item, converted_list):
    if last_item.count('-') % 2 == 0:
        if converted_list[-1] == '(':
            last_item = ""
        else:
            last_item = '+'
    else:
        last_item = '-'
    return last_item


def converter(parsing_list):
    if parsing_list[0] == "-":
        converted_list = [0]
    else:
        converted_list = []
    last_item = ""
    for i in parsing_list:
        if i == " ":
            continue
        if i != '-' and i != '+' and last_item:
            last_item = clean_add_sub_operators(last_item, converted_list)
            if last_item == '+':
                converted_list.append(operator_dict[last_item])
                last_item = ''
        if type(i) is float or type(i) is int:
            if last_item == '-' and converted_list[-1] != '(' \
                    and converted_list[-1] not in operator_dict.values():
                converted_list.append(operator_dict[last_item])
                converted_list.append(i)
                last_item = ""
            elif last_item == '-':
                converted_list.append(-i)
                last_item = ""
            else:
                converted_list.append(i)
        elif i in operator_dict.keys():
            if i == '-' or i == '+':
                last_item += i
            else:
                converted_list.append(operator_dict[i])
        elif i in function_dict.keys():
            if last_item:
                if last_item == '-' and converted_list[-1] != '(':
                    converted_list.append(operator_dict['+'])
                    converted_list.append(-1)
                    converted_list.append(operator_dict['*'])
                    converted_list.append(function_dict[i])
                    last_item = ""
                elif last_item == '-' and converted_list[-1] == '(':
                    converted_list.append(-1)
                    converted_list.append(operator_dict['*'])
                    converted_list.append(function_dict[i])
                    last_item = ""
            else:
                converted_list.append(function_dict[i])
        else:
            if last_item:
                converted_list.append(operator_dict['-'])
                last_item = ""
            converted_list.append(i)
    check_converted_list(converted_list)
    return converted_list


class OperandStack:

    def __init__(self):
        self.stack = list()

    def put_on_stack(self, item):
        self.stack.append(item)

    def top(self):
        return self.stack[-1]

    def take_from_stack(self):
        return self.stack.pop()

    def is_empty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False


def calc_on_stack():
    operator_on_stack = function.take_from_stack()
    global func_arguments
    if operator_on_stack in function_dict.values():
        if func_arguments:
            second_operand = operands.take_from_stack()
            first_operand = operands.take_from_stack()
            current_result = operator_on_stack['operator'](first_operand, second_operand)
            func_arguments = False
        else:
            first_operand = operands.take_from_stack()
            current_result = operator_on_stack['operator'](first_operand)
    elif operator_on_stack in operator_dict.values():
        if len(operands.stack) == 1:
            second_operand = operands.take_from_stack()
            first_operand = 0
        else:
            second_operand = operands.take_from_stack()
            first_operand = operands.take_from_stack()
        current_result = operator_on_stack['operator'](first_operand, second_operand)
    elif operator_on_stack == '(':
        return
    operands.put_on_stack(current_result)
    if len(function.stack) and function.top() is not '(':
        if current_operator['priority'] >= function.top()['priority']:
            current_result = calc_on_stack()
    return current_result


def calculate(converted_list):
    global operands, function, func_arguments, current_operator, current_result
    operands = OperandStack()
    function = OperandStack()
    func_arguments = False
    for item in converted_list:
        if type(item) is float or type(item) is int:
            operands.put_on_stack(item)
        elif item in operator_dict.values() or item in function_dict.values():
            current_operator = item
            if function.is_empty():
                function.put_on_stack(current_operator)
            else:
                if function.top() is '(' or current_operator['priority'] < function.top()['priority'] or \
                        current_operator == operator_dict['^'] and function.top() == operator_dict['^']:
                    function.put_on_stack(current_operator)
                else:
                    current_result = calc_on_stack()
                    function.put_on_stack(current_operator)
        elif item is '(':
            function.put_on_stack(item)
        elif item is ')' and function.top() == '(':
            function.take_from_stack()
        else:
            for i in range(len(function.stack)):
                if item is ',' and function.top() is '(':
                    func_arguments = True
                    break
                elif func_arguments:
                    current_result = calc_on_stack()
                else:
                    func_arguments = False
                if len(function.stack):
                    current_result = calc_on_stack()
                    if item is ')' and len(function.stack):
                        if function.top() is '(':
                            function.take_from_stack()
                            break
    if function.is_empty():
        current_result = operands.take_from_stack()
    elif len(function.stack) == 1:
        current_result = calc_on_stack()
    else:
        for i in range(len(function.stack)):
            current_operator = function.top()
            current_result = calc_on_stack()
            if not len(function.stack):
                break
    return current_result


def main():
    try:
        expression_line = arg_parser()
        operands = OperandStack()
        function = OperandStack()
        parser = split_operators(expression_line)
        converted_list = converter(parser)
        result = calculate(converted_list)
        print(result)
    except SyntaxError as err:
        print('ERROR: {}'.format(err))
    except ZeroDivisionError as err:
        print('ERROR: {}!'.format(err))
    except ValueError as err:
        print('ERROR: math error!')


if __name__ == '__main__':
    main()
