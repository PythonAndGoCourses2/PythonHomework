#!/usr/bin/python3

import operator
import math
import sys
import argparse
from .expression_parser import *
from .operator_manager import *
from .check_manager import *


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


def check_parsing_list(parsing_list):
    if parsing_list[0] in operator_dict.keys():
        if parsing_list[0] is not '+' and parsing_list[0] is not '-':
            raise SyntaxError('Expression cannot start with "{}"'.format(parsing_list[0]))
    if len(parsing_list) == 1:
        if type(parsing_list[0]) is int or type(parsing_list[0]) is float:
            return True
        raise SyntaxError('Expression must include at list one operand!')
    if parsing_list[-1] in operator_dict.keys():
        raise SyntaxError('Extra operator "{}" at the end of an expression!'.format(parsing_list[-1]))
    if parsing_list[-1] in function_dict.keys():
        raise SyntaxError('Function "{}" without argument'.format(parsing_list[-1]))
    return True


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
    check_parsing_list(parsing_list)
    if parsing_list[0] == "-" or parsing_list[0] == "+":
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
        if isinstance(i, float) or isinstance(i, int):
            if last_item == '-':
                if converted_list[-1] == 0:
                    converted_list.append(unary_dict[last_item])
                    converted_list.append(i)
                    last_item = ""
                elif last_item == '-' and converted_list[-1] != '(' \
                        and converted_list[-1] not in operator_dict.values():
                    converted_list.append(operator_dict[last_item])
                    converted_list.append(i)
                    last_item = ""
                else:
                    converted_list.append(-i)
                    last_item = ""
            else:
                converted_list.append(i)
        elif i in operator_dict.keys():
            if i == '-' or i == '+':
                last_item += i
            else:
                try:
                    if converted_list[-1]['operator']:
                        raise SyntaxError('Missing operand between two math operators!')
                except TypeError:
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
    elif operator_on_stack in operator_dict.values() or operator_on_stack in unary_dict.values():
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
        if isinstance(item, float) or isinstance(item, int):
            operands.put_on_stack(item)
        elif item in operator_dict.values() \
                or item in function_dict.values() \
                or item in unary_dict.values():
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
                    if func_arguments:
                        raise SyntaxError('This function can have only two arguments')
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
        parser = SplitOperators().split_operators(expression_line)
        clear_parser = check_expression(parser)
        converted_list = converter(parser)
        result = calculate(converted_list)
        print(result)
    except SyntaxError as err:
        print('ERROR: {}'.format(err))
    except ZeroDivisionError as err:
        print('ERROR: {}!'.format(err))
    except ValueError as err:
        print('ERROR: {}!'.format(err))
    except OverflowError as err:
        print('ERROR: {}!'.format(err))


if __name__ == '__main__':
    main()
