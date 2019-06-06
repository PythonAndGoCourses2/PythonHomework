#!/usr/bin/env python3

import argparse
import operator
import math
import importlib

OPERATORS = '+-*/^%<>=! ()'
CONSTANTS = {attr: getattr(math, attr) for attr in dir(math) if isinstance(getattr(math, attr), (int, float))}
OPERATIONS = {
    '+': (operator.add, 3),
    '-': (operator.sub, 3),
    '*': (operator.mul, 4),
    '//': (operator.floordiv, 4),
    '^': (operator.pow, 5),
    '/': (operator.truediv, 4),
    '%': (operator.mod, 4),
    '<': (operator.lt, 2),
    '<=': (operator.le, 2),
    '==': (operator.eq, 1),
    '!=': (operator.ne, 1),
    '>=': (operator.ge, 2),
    '>': (operator.gt, 2),
    '-u': (operator.neg, 5),
    '+u': (lambda x: x, 5),
    }
FUNCTIONS = {attr: getattr(math, attr) for attr in dir(math) if not attr[0] == '_'}
FUNCTIONS['abs'] = abs
FUNCTIONS['round'] = round


def parse_command_line():
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument("EXPRESSION", type=str, help='expression string to evaluate')
    parser.add_argument('-m', '--use-modules', nargs='*', dest="MODULE", type=str, help='additional modules to use')
    args = parser.parse_args()
    expression = args.EXPRESSION
    modules = args.MODULE
    return expression, modules


def parse_to_list(exprstr):
    """ Converting the expression from string to list by moving tokens from the left side of the string
    with their simultaneous assignment to numbers, operators or functions
    """
    temp = ''
    expr_list = []
    while exprstr:
        symbol = exprstr[0]
        if symbol in OPERATIONS or (len(exprstr) > 1 and exprstr[:2] in OPERATIONS):   # if operator
            if exprstr[:2] in OPERATIONS:               # if two symbol operator
                symbol = exprstr[:2]
                expr_list.append(symbol)
                exprstr = exprstr[2:]
                continue
            expr_list.append(symbol)
            exprstr = exprstr[1:]
        elif symbol.isdigit() or symbol == '.':             # if digit or start float number
            for symbol_temp in exprstr:                     # check next symbols to find whole number
                if symbol_temp.isdigit() or symbol_temp == '.':       # if float
                    temp += symbol_temp
                else:
                    break
            if '.' in temp:
                try:
                    expr_list.append(float(temp))
                except ValueError:                          # if impossible to convert to float
                    raise ValueError('error in input number {0}'.format(temp))
            else:
                expr_list.append(int(temp))
            exprstr = exprstr[len(temp):]
            temp = ''
        elif symbol.isalpha():                              # if character is alphabetic
            for symbol_temp in exprstr:                     # check the next symbols to find func or constant
                if symbol_temp.isalpha() or symbol_temp.isdigit():
                    temp += symbol_temp                     # if alphabetic or digit (for funcs with digit in name)
                else:
                    break                                   # function name must contain only letters and digits
            if temp in CONSTANTS:
                expr_list.append(temp)
            elif temp in FUNCTIONS:
                try:
                    if exprstr[len(temp)] == '(':
                        expr_list.append(temp)
                    else:
                        raise SyntaxError('missed argument(s) for function {0}'.format(temp))
                except IndexError:
                    raise IndexError('missed argument(s) for function {0}'.format(temp))
            else:                                           # if temp not in constants or function_dict
                raise ValueError('unknown function or constant {0}'.format(temp))
            exprstr = exprstr[len(temp):]
            temp = ''
        elif symbol in ('(', ')', ','):                     # if bracket or comma - move to list
            expr_list.append(symbol)
            exprstr = exprstr[1:]
        elif symbol == ' ':
            exprstr = exprstr[1:]                           # ignore space
        else:                                               # if different symbol - raise Error
            raise SyntaxError('unsupported symbol "{0}" in expression'.format(symbol))
    return expr_list


def check_unary_operator(expr_list):
    """ Checking the '+' and '-' operators for unary conditions and their modifying.
    Conditions for assignment to the unary group - '-' or '+' stay on first position in equation or
    after another arithmetic operator or opening parentheses or comma.
    """
    if expr_list[0] in ('-', '+'):
        expr_list[0] += 'u'
    for index in range(1, len(expr_list)):
        if expr_list[index] in ('-', '+') and (expr_list[index - 1] in ('(', ',') or
                                               expr_list[index-1] in OPERATIONS):
            expr_list[index] += 'u'


def precedence(oper1, oper2):
    """ Determining of operator precedence """
    left_associated = ['+', '-', '*', '//', '/', '%', '<', '<=', '==', '!=', '>=', '>']
    right_associated = ['^', '-u', '+u']
    if oper1 in left_associated:
        return OPERATIONS[oper1][1] <= OPERATIONS[oper2][1]
    elif oper1 in right_associated:
        return OPERATIONS[oper1][1] < OPERATIONS[oper2][1]


def shunting_yard_alg(expr_list):
    """ Parsing mathematical expressions specified in infix notation to Reverse Polish Notation
    by Shunting-Yard algorithm.
    RPN - notation of equation in which operator or function stay after corresponding operand(s).
    Operators are added according their precedence. No parentheses are needed.
    Resulting notation is ready for calculation (from left to right).
    """
    output_list = []
    stack = []
    while expr_list:
        item = expr_list[0]
        if isinstance(item, (int, float)) or item in CONSTANTS:
            output_list.append(item)
            expr_list = expr_list[1:]
        elif item in FUNCTIONS:
            stack.append(item)
            expr_list = expr_list[1:]
        elif item == ',':
            expr_list = expr_list[1:]
            if '(' in stack:
                while stack[-1] != '(':
                    output_list.append(stack.pop())
            else:
                raise SyntaxError('the opening parentheses or comma is missed')
            output_list.append(item)              # comma will indicate the presence of multi parameters for the func
            if expr_list and expr_list[0] == ')':
                raise SyntaxError('error in the data inside the parentheses')
        elif item in OPERATIONS:
            if stack and (stack[-1] in OPERATIONS):
                while stack and (stack[-1] in OPERATIONS):
                    if precedence(item, stack[-1]):
                        output_list.append(stack.pop())
                    else:
                        break
                stack.append(item)
            elif stack == [] or '(' in stack:
                stack.append(item)
            expr_list = expr_list[1:]
        elif item == '(':
            stack.append(item)
            expr_list = expr_list[1:]
        elif item == ')':
            while stack and stack[-1] != '(':
                output_list.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
            elif not stack:
                raise SyntaxError('opening parentheses is missed')
            if stack and (stack[-1] in FUNCTIONS):
                output_list.append(stack.pop())
            expr_list = expr_list[1:]
    else:
        while stack:
            if stack[-1] == '(':
                raise SyntaxError('closing parentheses is missed')
            output_list.append(stack.pop())
    return output_list                                      # returning expression in Reverse Polish Notation


def perform_operation(operator, operand_1, operand_2):
    """ Perform binary operator for operands """
    return OPERATIONS[operator][0](operand_1, operand_2)


def perform_unary_operation(operator, operand):
    """ Perform unary operator for operand """
    return OPERATIONS[operator][0](operand)


def perform_function(function, *operand):
    """ Perform function with one or more arguments """
    try:
        result = FUNCTIONS[function](*operand)
    except ValueError:
        raise ValueError('error in entered data for function {0}'.format(function))
    # except TypeError:
        # result = function_dict[function](operand)
        # raise TypeError('unsupported data in function {0} parentheses'.format(function))
    return result


def calculation_from_rpn(rev_pol_not_list):
    """ Sequential calculation from left to right of expression in Reverse Polish Notation.
    Operators and functions are applied to corresponding previous staying operand(s)
    """
    stack = []
    arg_stack = []
    for item in rev_pol_not_list:
        if item in CONSTANTS:
            stack.append(CONSTANTS[item])
        elif isinstance(item, (int, float)):
            stack.append(item)
        elif item == ',':
            arg_stack.append(stack.pop())
            stack.append(item)
        elif item in FUNCTIONS:
            if len(stack) > 1 and stack[-2] == ',':
                commas = 0                                  # cheking the presence of commas and sum all successive ones
                for index in range(-2, -len(stack)-1, -1):
                    if stack[index] == ',':
                        commas += 1
                    else:
                        break
                while commas:
                    params = arg_stack[-commas:]
                    params.append(stack[-1])
                    try:
                        intermediate_result = perform_function(item, *params)
                        for index in range(commas + 1):
                            stack.pop()
                        for index in range(commas):
                            arg_stack.pop()
                        stack.append(intermediate_result)
                        break
                    except TypeError:
                        commas -= 1
                        continue
                else:
                    try:
                        intermediate_result = perform_function(item, stack.pop())
                        stack.append(intermediate_result)
                    except TypeError:
                        raise TypeError("unsupported operand(s)")
            else:
                try:
                    intermediate_result = perform_function(item, stack.pop())
                    stack.append(intermediate_result)
                except TypeError:
                    raise TypeError("unsupported operand for function '{0}'".format(item))
                except OverflowError:
                    raise OverflowError(f'result of {item} too large to be represented')
        elif item in OPERATIONS:
            if item in ('-u', '+u'):
                intermediate_result = perform_unary_operation(item, stack.pop())
            else:
                try:
                    operand_2, operand_1 = stack.pop(), stack.pop()
                    intermediate_result = perform_operation(item, operand_1, operand_2)
                except ZeroDivisionError:
                    raise ZeroDivisionError('division by zero')
                except IndexError:
                    raise IndexError('insufficient amount of operands')
                except OverflowError:
                    raise OverflowError(f'result of {item} too large to be represented')
            stack.append(intermediate_result)
    if len(stack) == 1:
        result = stack[0]
        return result
    else:
        raise SyntaxError('insufficient amount of operators or function or too many operands/arguments')


def check_empty_operators(exprstr):
    """ Checking expression for empty string or string containing only operators or parentheses """
    if len(exprstr) == 0:
        raise SyntaxError('empty expression')
    elif set(exprstr).issubset(set(OPERATORS)):
        raise SyntaxError('no digits, constants or functions in expression')
    else:
        return False


def check_brackets(exprstr):
    """ Checking for brackets balance """
    if ('(' and ')') in exprstr:
        if exprstr.count('(') == exprstr.count(')'):
            if exprstr.index(')') < exprstr.index('('):
                raise SyntaxError('brackets are not balanced')
            return True
        else:
            raise SyntaxError('brackets are not balanced')
    else:
        return True


def calculation(exprstr):
    """ Calculation of string type argument from command line """
    if (not check_empty_operators(exprstr)) and check_brackets(exprstr):
        expr_list = parse_to_list(exprstr)
        check_unary_operator(expr_list)
        return calculation_from_rpn(shunting_yard_alg(expr_list))


def import_new_module(module_name):
    """ Trying to import module provided with -m (--use-modules) flag and
    updating the constants and functions dictionaries.
    Functions and constants from user defined modules have higher priority.
    in case of name conflict then stuff from math module or built-in functions
    If the module cannot be imported info about this will be printed
    but calculation will be tried to execute
    """
    try:
        module = importlib.import_module(module_name)
        try:
            CONSTANTS.update({attr: getattr(module, attr) for attr in dir(module)
                              if isinstance(getattr(module, attr), (int, float))})
            FUNCTIONS.update({attr: getattr(module, attr) for attr in dir(module) if not attr[0] == '_'})
        except Exception:
            print(f'Smth bad with new module {module_name}')
            pass
            # raise Exception('Smth bad with new module')
    except ImportError:
        print(f'Unable to import the module {module_name}')


def main():
    try:
        expression, modules = parse_command_line()
        if modules:
            for module in modules:
                import_new_module(module)
        print(calculation(expression))
    except Exception as err:
        print('ERROR: ', err)


if __name__ == '__main__':
    main()
