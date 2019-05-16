#!/usr/bin/python3

import argparse
from .expression_parser import SplitOperators
from .operator_manager import operator_dict, function_dict, unary_dict
from .check_manager import check_expression
from .stack_manager import OperandStack
from .converter import Converter


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
        parser = SplitOperators().split_operators(expression_line)
        clear_parser = check_expression(parser)
        converted_list = Converter(clear_parser)
        result = calculate(converted_list.converter())
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
