import re
import math
from operators import *
from split import *


def tran_in_pol_not(inp):
    out_stack = []
    slave_stack = []
    split_list = split_string(inp, list_of_op)
    for i, char in enumerate(split_list):
        if is_num(char) or char in post_func:
            out_stack.append(char)
        elif char in inf_func:
            if len(slave_stack) == 0:
                slave_stack.append(char)
            else:
                if char == '-':
                    if i == 0:
                        out_stack.append(0)
                    elif i + 1 == len(split_list):
                        raise ArithmeticError
                    elif is_num(split_list[i + 1]):
                        if split_list[i - 1] == '(' and split_list[i + 2] != ')':
                            out_stack.append(0)

                while True and len(slave_stack) > 0:
                    item = slave_stack.pop()
                    if item not in inf_func or inf_func[char] < inf_func[item]:
                        slave_stack.append(item)
                        break
                    else:
                        out_stack.append(item)
                slave_stack.append(char)
        else:
            if char is '(':
                slave_stack.append(char)
            elif char is ')':
                while True:
                    elem = slave_stack.pop()
                    if elem is not '(':
                        out_stack.append(elem)
                    else:
                        break
            else:
                slave_stack.append(char)

    while len(slave_stack) > 0:
        out_stack.append(slave_stack.pop())

    return out_stack


def pols_not(exp1):
    stack = []
    i = 0
    x = 0
    end = False
    while not end:
        c = exp1[i]
        if is_num(c):
            x = float(c)
            stack.append(x)
        else:
            '''foo = None'''
            if c in operators:
                foo = operators[c]
            else:
                try:
                    foo = getattr(math, c)
                except Exception as inst:
                    print("Unexpected error:", inst)
                    raise
            #достать n последних числа из стека в зависимости от функции
            '''params_count = len(signature(foo).parameters)#no signature found for builtin <built-in function> error in v3.6
            operands = [stack.pop() for _ in range(0, params_count)]
            #выполнить операцию по ключу С'''
            if callable(foo):
                '''if params_count == 1:
                    x = foo(operands[0])
                elif params_count == 2:
                    x = foo(operands[1], operands[0])
                else:
                    x = foo(operands)'''
                if c in inf_func:
                    op1, op2 = stack.pop(), stack.pop()
                    x = foo(op2, op1)
                else:
                    x = foo(stack.pop())
            else:
                #добавить в стек прочитанное число,
                #или результат операции
                x = foo
            stack.append(x)
        i += 1
        if i >= len(exp1):
            end = True
    return x

