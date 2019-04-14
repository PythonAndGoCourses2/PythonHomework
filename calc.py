#!/usr/bin/python3

import operator
import math
from math import *


function_dict = {
    'abs': {'operator': abs, 'priority': 0},
    'round': {'operator': round, 'priority': 0}
}
for k,v in math.__dict__.items():
    if k.startswith('_'):
        continue
    function_dict[k] = {'operator': v, 'priority': 0}


operator_dict = {
    '+': {'operator': operator.add, 'priority': 4},
    '-': {'operator': operator.sub, 'priority': 4},
    '/': {'operator': operator.truediv, 'priority': 3},
    '*': {'operator': operator.mul, 'priority': 3},
    '%': {'operator': operator.mod, 'priority': 3},
    '//': {'operator': operator.floordiv, 'priority': 3},
    '^': {'operator': operator.pow, 'priority': 1},
    '==': {'operator': operator.eq, 'priority': 9},
    '!=': {'operator': operator.ne, 'priority': 9},
    '>': {'operator': operator.gt, 'priority': 9},
    '<': {'operator': operator.lt, 'priority': 9},
    '>=': {'operator': operator.ge, 'priority': 9},
    '<=': {'operator': operator.le, 'priority': 9},

}


example = [
    "-13",
    "6-(-13)",
    "1---1",
    "-+---+-1",
    "1+2*2",
    "1+(2+3*2)*3",
    "10*(2+1)",
    "10^(2+1)",
    "100/3^2",
    "100/3%2^2",
    "pi+e",
    "log(e)",
    "sin(pi/2)",
    "log10(100)",
    "sin(pi/2)*111*6",
    "2*sin(pi/2)",
    "abs(-5)",
    "round(123.45689)",
    "102%12%7",
    "100/4/3",
    "2^3^4",
    "1+2*3==1+2*3",
    "e^5>=e^5+1",
    "1+2*4/3+1!=1+2*4/3+2",
    "(100)",
    "666",
    "-.1",
    "1/3",
    "1.0/3.0",
    ".1 * 2.0^56.0",
    "e^34",
    "(2.0^(pi/pi+e/e+2.0^0.0))",
    "(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)",
    "sin(pi/2^1) + log(1*4+2^2+1, 3^2)",
    "10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5",
    "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)",
    "2.0^(2.0^2.0*2.0^2.0)",
    "sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"

]


def number_parser(number):
    try:
        return int(number)
    except:
        return float(number)


def function_parser(function_name):
    if function_name == 'e' or function_name == 'pi':
        return function_dict[function_name]['operator']
    return function_name


def split_operators(s):
    parsing_list = []
    last_number = ""
    last_letter = ""
    last_symbol = ""
    for i in s:
        if i == " ":
            continue
        if i.isnumeric() or i is '.':
            if last_symbol:
                parsing_list.append(last_symbol)
                last_symbol = ""
            if last_letter:
                last_letter += i
            else:
                last_number += i
        elif i.isalpha():
            if last_symbol:
                parsing_list.append(last_symbol)
                last_symbol = ""
            last_letter += i
        else:
            if last_number:
                parsing_list.append(number_parser(last_number))
                last_number = ""
            if last_letter:
                parsing_list.append(function_parser(last_letter))
                last_letter = ""
            if i:
                parsing_list.append(i)
    if last_number:
        parsing_list.append(number_parser(last_number))
    elif last_letter:
        parsing_list.append(function_parser(last_letter))
    return parsing_list


def clean_add_sub_operators(last_item, converted_list):
    if last_item.count('-') % 2 == 0:
        if converted_list[-1] == '(':
            last_item= ""
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
        if i != '-' and i != '+' and last_item:
            last_item = clean_add_sub_operators(last_item, converted_list)
            if last_item == '+':
                converted_list.append(operator_dict[last_item])
                last_item = ''
        if type(i) is float or type(i) is int:
            if last_item == '-' and converted_list[-1] != '(' and converted_list[-1] not in operator_dict.values():
                converted_list.append(operator_dict['+'])
                converted_list.append(-i)
                last_item = ""
            elif last_item == '-':
                converted_list.append(-i)
                last_item = ""
            else:
                converted_list.append(i)
        elif i in operator_dict.keys():
            if i == '-' or i == '+':
                last_item +=i
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
    return converted_list


class OperandStack():

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
    global func_argments
    if operator_on_stack in function_dict.values():
        if func_argments:
            second_operand = operands.take_from_stack()
            first_operand = operands.take_from_stack()
            current_result = operator_on_stack['operator'](first_operand, second_operand)
            func_argments = False
            # print_calc_on_stack(first_operand, second_operand,operator_on_stack, current_result)
        else:
            first_operand = operands.take_from_stack()
            current_result = operator_on_stack['operator'](first_operand)
            # print_calc_on_stack(first_operand, operator_on_stack,current_result)
    elif operator_on_stack in operator_dict.values():
        if len(operands.stack) == 1:
            second_operand = operands.take_from_stack()
            first_operand = 0
        else:
            second_operand = operands.take_from_stack()
            first_operand = operands.take_from_stack()
        current_result = operator_on_stack['operator'](first_operand, second_operand)
        # print_calc_on_stack(first_operand, second_operand, operator_on_stack,current_result)
    elif operator_on_stack == '(':
        return
    operands.put_on_stack(current_result)
    if len(function.stack) and function.top() is not '(':
        if current_operator['priority'] >= function.top()['priority']:
            current_result = calc_on_stack()
    return current_result


def calculacte(converted_list):
    global operands, function, func_argments, current_operator, current_result
    operands = OperandStack()
    function = OperandStack()
    func_argments = False
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
                    func_argments = True
                    break
                elif func_argments:
                    calc_on_stack()
                else:
                    func_argments = False
                current_result = calc_on_stack()

                if item is ')':
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


operands = OperandStack()
function = OperandStack()

for expression in example:
    string = ''
    for i in expression:
        if i == '^':
            string += '**'
        else:
            string +=i
    try:
        calculacte(converter(split_operators(expression)))
    except:
        print('fault')
    if current_result != eval(string):
        print(expression)
        print(current_result, current_result == eval(string))
        print('\n')

# operands = OperandStack()
# function = OperandStack()
#
# func_argments = False
# for item in converted_list:
#     if type(item) is float or type(item) is int:
#         operands.put_on_stack(item)
#     elif item in operator_dict.values() or item in function_dict.values():
#         current_operator = item
#         if function.is_empty():
#            function.put_on_stack(current_operator)
#         else:
#             if function.top() is '(' or current_operator['priority'] < function.top()['priority'] or \
#                     current_operator == operator_dict['^'] and function.top() == operator_dict['^']:
#                 function.put_on_stack(current_operator)
#             else:
#                 current_result = calc_on_stack()
#
#                 function.put_on_stack(current_operator)
#     elif item is '(':
#         function.put_on_stack(item)
#     elif item is ')' and function.top() == '(':
#         function.take_from_stack()
#     else:
#         for i in range(len(function.stack)):
#             if item is ',' and function.top() is '(':
#                 func_argments = True
#                 break
#             elif func_argments:
#                 calc_on_stack()
#             else:
#                 func_argments = False
#             current_result = calc_on_stack()
#
#             if item is ')':
#                 if function.top() is '(':
#                     function.take_from_stack()
#                     break
#
# if function.is_empty():
#     current_result = operands.take_from_stack()
# elif len(function.stack) == 1:
#     current_result = calc_on_stack()
# else:
#     for i in range(len(function.stack)):
#         current_operator = function.top()
#         current_result = calc_on_stack()
#         if not len(function.stack):
#             break







# print(-20+34-50*6-11*2/2)
# print(54-300+22)
# print(-math.pi+3-((-60/2**2-1)/(2+3)**(-3)))
# print(60/2**2-1)
# print(102%12%7)
# print(60/2**2---1+-+math.e)
# print(operands.stack)
# print(function.stack)
# print(math.sin(math.pi/2+math.cos(math.e)**2)*111*6)
# print(sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(43.0))))+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0)
# print(sin(-cos(-sin(3.0)-cos(-sin(-3.0**5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0))
# print((2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))**(1.0/3.0))
# print(.1*2.0**56.0)
# print(math.sin(/math.pi)+math.e*round(2+9))
# print(math.sin(math.pi/2)*111*6)
# print(2.0**(2.0**2.0**2.0**2.0))
# print(math.sin(math.e**math.log(math.e**math.e**math.sin(23.0),45.0) + math.cos(3.0+math.log10(math.e**-math.e))))
# print(sin(pi/2**1) + log10(1*4+2**2+1))
# print(10*e**0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5)
# print(.4-5/-0.1-10)
# print(1+2*4/3+1>1+2*4/3+2)
# print(sin(e**log(e**e**sin(23.0),45.0) + log(e**e**sin(23.0),45.0)))
# print(sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e))))
# print(sin(log(-sin(23.0),45.0)**2 + log(-sin(23.0),45.0)**3))
# print(log(-sin(23.0),45.0))




