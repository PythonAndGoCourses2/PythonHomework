import re
import math
from inspect import signature
from inspect import getargs
from operators import *
from split import *


def tran_in_pol_not(inp):
    """Перевод введённого математического выражения в обратную польскую нотацию."""
    out_stack = []
    slave_stack = []
    # парсинг выражения
    split_list = split_string(inp, list_of_op)
    for i, char in enumerate(split_list):
        if char is '(':
            slave_stack.append(char)
        elif char is ')':
            if '(' not in slave_stack:
                print("ERROR: brackets are not balanced")
                raise Exception
            while slave_stack:
                elem = slave_stack.pop()
                if elem is not '(':
                    out_stack.append(elem)
                else:
                    break
        elif is_num(char):
            out_stack.append(char)
        elif char in list_of_op:
            if len(split_list) == 1:
                print("ERROR: it is essential to have at list one operand")
                raise ArithmeticError
            if char in unary_op:
                inf_op = list(split_by_prefix(char, ['+', '-']))[0]
                if i + 1 != len(split_list) and (i == 0 or is_num(split_list[i + 1])):
                    out_stack.extend([split_list[i + 1], 1])
                    split_list[i + 1] = inf_op
                else:
                    if i + 1 == len(split_list):
                        out_stack.extend([1, inf_op])
                    for index in range(i + 1, len(split_list)):
                        if is_num(split_list[index]):
                            if index + 1 == len(split_list):
                                split_list.extend([inf_op, 1])
                                break
                            split_list.insert(index, 1)
                            split_list.insert(index + 1, inf_op)
                            break
            elif operators[char].type == 'inf':
                '''if len(slave_stack) == 0:
                    slave_stack.append(char)
                else:'''
                if char == '-':
                    if i == 0:
                        out_stack.append(0)
                    elif i + 1 == len(split_list):
                        print("ERROR: Invalid expression: there is no 2nd operand after -.")
                        raise ArithmeticError
                    elif is_num(split_list[i + 1]):
                        if split_list[i - 1] == '(' and split_list[i + 2] != ')':
                            out_stack.append(0)

                while slave_stack:
                    item = slave_stack.pop()
                    if item in parentheses or (item in list_of_op and
                                               operators[char].priority < operators[item].priority):
                        slave_stack.append(item)
                        break
                    else:
                        out_stack.append(item)
                slave_stack.append(char)
        else:
            slave_stack.append(char)

    while len(slave_stack) > 0:
        if '(' in slave_stack:
            print("ERROR: brackets are not balanced")
            raise Exception
        out_stack.append(slave_stack.pop())
    return out_stack


def pols_not(exp1):
    """Вычисление результата выражения по введённой польской нотации."""
    stack = []
    index = 0
    value = 0
    end = False
    while not end:
        item = exp1[index]
        # добавить в стек прочитанное число,
        # или результат операции
        if is_num(item):
            value = float(item)
            stack.append(value)
        else:
            if item in operators:
                foo = operators[item].func
            elif item in math_func:
                foo = math_func[item]
            else:
                try:
                    foo = getattr(math, item)
                except Exception as inst:
                    print("Unexpected instance:", inst)
                    raise
            # Evaluate a function according to the type an args or just set a value
            if callable(foo):
                try:
                    if item in list_of_op and operators[item].type == 'inf':
                        op1, op2 = stack.pop(), stack.pop()
                        value = foo(op2, op1)
                    else:
                        value = foo(stack.pop())
                # выполнить операцию по ключу С
                except ArithmeticError as err:
                    print("Handling run-time error with evaluating a function or taking args: ", err)
                    raise
            else:
                value = foo
            stack.append(value)
        index += 1
        if index >= len(exp1):
            end = True
    return value
