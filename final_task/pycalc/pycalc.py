#!/usr/bin/env python3

import argparse
import operator
import math

operators = '+-*/^%<>=! ()'
# comparisons = ['<', '<=', '==', '!=', '>=', '>']
constants = {'pi': math.pi, 'e': math.e, 'tau': math.tau}
operation_dict = {
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
    '-u': (operator.neg, 5),   # or lambda x: x * -1
    '+u': (lambda x: x, 5)
    }

function_dict = math.__dict__
function_dict['abs'] = abs
function_dict['round'] = round
# print(functions_dict)


def parse_command_line():
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument("EXPRESSION", type=str, help='expression string to evaluate')
    # parser.add_argument('-m', '--MODULE', type=str, help='use modules MODULE [MODULE...] additional modules to use')

    args = parser.parse_args()
    expression = args.EXPRESSION

    # module = args.MODULE
    return expression


def parse_to_list(exprstr):
    """ Converting the expression from string to list by moving tokens from the left side of the string
        with their simultaneous assignment to numbers, operators or functions"""
    temp = ''
    expr_list = []
    while exprstr:
        symbol = exprstr[0]
        # print(symbol)
        if symbol in operation_dict or (len(exprstr) > 1 and exprstr[:2] in operation_dict):   # if operator
            if exprstr[:2] in operation_dict:               # if two symbol operator
                symbol = exprstr[:2]
                expr_list.append(symbol)
                exprstr = exprstr[2:]
                continue
            expr_list.append(symbol)
            exprstr = exprstr[1:]
        
        elif symbol.isdigit() or symbol == '.':             # if digit or start float number
            for i in range(len(exprstr)):
                symbol = exprstr[i]
                if symbol.isdigit() or symbol == '.':       # if float
                    temp += symbol
                else:
                    break
            if '.' in temp:
                try:
                    expr_list.append(float(temp))
                except ValueError:                          # if impossible to convert to float - raise Error
                    raise ValueError('ERROR: error in input number')
            else:
                expr_list.append(int(temp))
            exprstr = exprstr[len(temp):]
            temp = ''
        elif symbol.isalpha():                              # if character is alphabetic
            for i in range(len(exprstr)):                   # check the next symbols to find func or constant
                symbol = exprstr[i]
                if symbol.isalpha() or symbol.isdigit():    # if alphabetic or digit (for funcs with digit in name)
                    temp += symbol
                    if temp in constants:
                        expr_list.append(temp)
                        break
                    elif temp in function_dict:
                        try:
                            if exprstr[i+1] == '(':
                                expr_list.append(temp)
                                break
                            else:
                                continue
                        except IndexError:
                            raise IndexError('ERROR: missed argument(s) for function {0}'.format(temp))
                else:
                    if symbol == '(' and temp not in (constants or function_dict):
                        raise ValueError('ERROR: unknown function or constant {0}'.format(temp))
                    break
            else:
                if temp not in (constants or function_dict):
                    raise ValueError('ERROR: unknown function or constant {0}'.format(temp))
            exprstr = exprstr[len(temp):]
            temp = ''
        elif symbol in ('(', ')', ','):                     # if bracket or comma - move to list
            expr_list.append(symbol)
            exprstr = exprstr[1:]
        elif symbol == ' ':                
            exprstr = exprstr[1:]
        else:                                               # if different symbol - raise Error
            raise SyntaxError('ERROR: unsupported symbol "{0}" in expression'.format(symbol))
    # print(expr_list)
    return expr_list


def unary_operator_check(expr_list):
    """ Checking the '+' and '-' operators for unary conditions and their modifying.
    Conditions for assignment to the unary group - '-' or '+' stay on first position in equation or
    after another arithmetic operator or opening parentheses or comma.
    """
    if expr_list[0] in ('-', '+'):
        expr_list[0] += 'u'
    for index in range(1, len(expr_list)):
        if expr_list[index] in ('-', '+') and (expr_list[index - 1] in ('(', ',') or
                                               expr_list[index-1] in operation_dict):
            expr_list[index] += 'u'


def precedence(oper1, oper2):
    """ Determining of operator precedence """
    left_associated = ['+', '-', '*', '//', '/', '%', '<', '<=', '==', '!=', '>=', '>']
    right_associated = ['^', '-u', '+u']
    if oper1 in left_associated:
        return operation_dict[oper1][1] <= operation_dict[oper2][1]
    elif oper1 in right_associated:
        return operation_dict[oper1][1] < operation_dict[oper2][1]


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
        if type(item) == int or type(item) == float or item in constants:
            output_list.append(item)
            expr_list = expr_list[1:]
        elif item in function_dict:
            stack.append(item)
            expr_list = expr_list[1:]
        elif item == ',':
            expr_list = expr_list[1:]
            if '(' in stack:
                while stack[-1] != '(':
                    output_list.append(stack.pop())
            else:
                raise SyntaxError('ERROR: the opening parentheses or comma is missed')
            output_list.append(item)              # comma will indicate the presence of multi parameters for the func
        elif item in operation_dict:
            if stack and (stack[-1] in operation_dict):
                while stack and (stack[-1] in operation_dict):
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
                raise SyntaxError('ERROR: opening parentheses is missed')
            if stack and (stack[-1] in function_dict):
                output_list.append(stack.pop())
            expr_list = expr_list[1:]
    else:
        while stack:
            if stack[-1] == '(':
                raise SyntaxError('ERROR: closing parentheses is missed')
            output_list.append(stack.pop())
    return output_list                                      # returning reverse_polish_notation


def perform_operation(operator, operand_1, operand_2):
    """ Perform binary operator for operands """
    return operation_dict[operator][0](operand_1, operand_2)


def perform_unary_operation(operator, operand):
    """ Perform unary operator for operand """
    return operation_dict[operator][0](operand)


def perform_function(function, *operand):
    """ Perform function with one ore more parameters """
    return function_dict[function](*operand)


def calculation_from_rpn(rev_pol_not_list):
    """ Sequential calculation from left to right of expression in Reverse Polish Notation.
    Operators and functions are applied to corresponding previous staying operand(s) """
    stack = []
    # arg_stack = []
    for item in rev_pol_not_list:
        # print(item)
        if item in constants:
            stack.append(constants[item])
        elif type(item) == int or type(item) == float:
            stack.append(item)
        elif item == ',':
            # arg_stack.append(stack.pop())
            stack.append(item)                              # indicate presence of two parameters for function
        elif item in function_dict:
            if len(stack) > 1 and stack[-2] == ',':
                try:
                    params = []
                    params.append(stack[-3])
                    # params.append(arg_stack[-1])
                    params.append(stack[-1])
                    # try to perform func with two parameters
                    intermediate_result = perform_function(item, *params)
                    stack.pop()                             # pop 2nd parameter
                    stack.pop()                             # pop comma
                    stack.pop()                             # pop 1st parameter
                    # arg_stack.pop()
                    stack.append(intermediate_result)       # append intermediate result to stack
                except TypeError:
                    try:
                        # try to perform func with one parameter
                        intermediate_result = perform_function(item, stack.pop())
                        stack.append(intermediate_result)   # append intermediate result to stack
                    except TypeError:
                        raise TypeError("ERROR: unsupported operand for function")
                except ValueError:
                    raise ValueError("ERROR: unsupported operands for function")
            else:
                try:
                    intermediate_result = perform_function(item, stack.pop())
                    stack.append(intermediate_result)
                except TypeError:
                    raise TypeError("ERROR: unsupported operand for function {0}".format(item))
        elif item in operation_dict:
            if item in ('-u', '+u'):
                intermediate_result = perform_unary_operation(item, stack.pop())
            else:
                try:
                    operand_2, operand_1 = stack.pop(), stack.pop()
                    intermediate_result = perform_operation(item, operand_1, operand_2)
                except ZeroDivisionError:
                    raise ZeroDivisionError('ERROR: division by zero')
                except IndexError:
                    raise IndexError('ERROR: insufficient amount of operands')
            stack.append(intermediate_result)
    if len(stack) == 1:
        result = stack[0]
        return result
    else:
        raise Exception('ERROR: insufficient amount of operators or function or too many operands/arguments')


def check_empty_operators(exprstr):
    """ Checking expression for empty string or string containing only operators or parentheses """
    if len(exprstr) == 0 or\
       set(exprstr).issubset(set(operators)) or\
       set(exprstr).issubset({'(', ')', ' '}):
        raise SyntaxError('ERROR: no digits and/or functions in expression')
    else:
        return False


def brackets_check(exprstr):
    """ Checking for brackets balance """
    if ('(' and ')') in exprstr:
        if exprstr.count('(') == exprstr.count(')'):
            if exprstr.index(')') < exprstr.index('('):
                raise SyntaxError('ERROR: brackets are not balanced')
            return True
        else:
            raise SyntaxError('ERROR: brackets are not balanced')
    else:
        return True


def calculation(exprstr):
    """
    Calculation of string type argument from command line
    """
    if (not check_empty_operators(exprstr)) and brackets_check(exprstr):
        expr_list = parse_to_list(exprstr)
        # print(expr_list)
        unary_operator_check(expr_list)
        # print(expr_list)
        rev_pol_not_list = shunting_yard_alg(expr_list)
        # print(rev_pol_not_list)
        result = calculation_from_rpn(rev_pol_not_list)
        return result


def main():
    try:
        expression = parse_command_line()
        print(calculation(expression))
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
