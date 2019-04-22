'''This module calculate the exception'''
import math


def get_priority(operand):
    '''Determines the priority of the operation'''
    low_priority = ('+', '-')
    return 1 if operand in low_priority else 2


def convert_into_rpn(expression):
    '''Rewrites the expression into the reverse polish notation'''
    arithmetic_operations = ('+', '-', '*', '/', '//', '%', '^')
    math_functions = [getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))]
    constants = (math.pi, math.e, math.tau)
    stack = []
    num = ''
    polish_notation = ''

    # rewriting expression into reverse polish notation
    for symbol in expression:
        if symbol in arithmetic_operations:
            polish_notation += num + ' '
            num = ''
            while True:
                if not stack:
                    break
                if stack[-1] == '(' or (get_priority(symbol) > get_priority(stack[-1])):
                    break
                elif get_priority(symbol) <= get_priority(stack[-1]):
                    polish_notation += stack.pop()
            stack.append(symbol)
        elif symbol.isdigit() or symbol == '.':
            num += symbol
        elif symbol == '(':
            stack.append(symbol)
        elif symbol == ')':
            polish_notation += num + ' '
            num = ''
            while True:
                tmp = stack.pop()
                if tmp == '(':
                    break
                polish_notation += tmp + ' '
    polish_notation += num + ' '
    while stack:
        polish_notation += stack.pop() + ' '

    return polish_notation


def solve(expression):
    '''Solves an expression using reverse polish notation.'''
    polish_notation = convert_into_rpn(expression)
    num = ''
    stack = []
    for symbol in polish_notation:
        if symbol.isdigit() or symbol == '.':
            num += symbol
        else:
            if num:
                stack.append(float(num))
                num = ''
            if symbol == '+':
                tmp = stack.pop() + stack.pop()
                stack.append(tmp)
            elif symbol == '-':
                lower_element = stack.pop()
                upper_element = stack.pop()
                stack.append(upper_element - lower_element)
            elif symbol == '*':
                tmp = stack.pop() * stack.pop()
                stack.append(tmp)
            elif symbol == '/':
                lower_element = stack.pop()
                upper_element = stack.pop()
                stack.append(upper_element / lower_element)
    return stack[0]


def main():
    expression = str(input())
    print(solve(expression))

if __name__ == "__main__":
    main()
