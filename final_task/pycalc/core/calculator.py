'''This module calculate the expression'''
import math
import operator as op

def get_priority(operand):
    '''Determines the priority of the operation'''
    low_priority = ('+', '-')
    return 1 if operand in low_priority else 2


def handling_operator(polish_notation, num, stack, symbol):
    '''if the lexeme is an operator, then:
            if it is the last character of the expression, the expression is incorrect;
            if this is a unary minus, then add it to the stack;
            otherwise:
                pushing the top elements of the stack into the result string, while the priority of the current operator is less than or equal to the priority of the operator located on the verine of the stack;
                put the current operator in the stack;'''
    polish_notation += num + ' '
    while True:
        if not stack:
            break
        if stack[-1] == '(' or (get_priority(symbol) > get_priority(stack[-1])):
            break
        elif get_priority(symbol) <= get_priority(stack[-1]):
            polish_notation += stack.pop()
    stack.append(symbol)

    return polish_notation, ''


def handling_closing_bracket(polish_notation, num, stack):
    '''if the lexeme is a closing bracket, then:
            we place elements from the stack into the resulting line until we meet the opening bracket, moreover, the opening bracket is removed from the stack, but not added to the resulting line;
            if the function symbol is at the top of the stack, then we put it from the stack into the result string;
            if the opening loop was not met, then the brackets are not consistent.'''
    polish_notation += num + ' '
    while True:
        tmp = stack.pop()
        if tmp == '(':
            break
        polish_notation += tmp + ' '

    return polish_notation, ''

def convert_into_rpn(expression):
    '''Rewrites the expression into the reverse polish notation'''
    arithmetic_operations = ('+', '-', '*', '/', '//', '%', '^')
    math_functions = [getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))]
    constants = (math.pi, math.e, math.tau)
    stack = []
    num = ''
    polish_notation = ''

    for symbol in expression:
        if symbol in arithmetic_operations:
            polish_notation, num = handling_operator(polish_notation, num, stack, symbol)
        elif symbol.isdigit() or symbol == '.':
            num += symbol
        elif symbol == '(':
            stack.append(symbol)
        elif symbol == ')':
            polish_notation, num = handling_closing_bracket(polish_notation, num, stack)
    polish_notation += num + ' '
    while stack:
        polish_notation += stack.pop() + ' '

    return polish_notation


def solve(expression):
    '''Solves an expression using reverse polish notation.'''
    operators = {
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.floordiv
    }
    polish_notation = convert_into_rpn(expression)
    num = ''
    stack = []
    for symbol in polish_notation:
        if symbol.isdigit() or symbol == '.':
            num += symbol
        elif symbol in operators.keys():
            if num:
                stack.append(float(num))
                num = ''
            lower_num, upper_num = stack.pop(), stack.pop()
            stack.append(operators[symbol](upper_num, lower_num))
        elif not symbol.isdigit():
            if num:
                stack.append(float(num))
                num = ''
    return stack[0]
