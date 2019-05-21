import pycalc.stack as Stack
import importlib
import operator
import math
import re

signs = ['+', '-', '*', '/', '^', '%', '>', '<', '=', '//', '!']

logical_signs = {
    '>': operator.gt,
    '>=': operator.ge,
    '==': operator.eq,
    '!=': operator.ne,
    "<=": operator.le,
    "<": operator.le
}

math_consts = {
    "pi": math.pi,
    "e": math.e

}

functions = {'round': round, 'abs': abs}


def get_args(expression):
    if len(expression) == 0:
        return ''
    expression.append(',')
    result = []
    prev = -1
    for index, part in enumerate(expression):
        if part == ',':
            result.append(float(calc(expression[prev + 1: index])))
            prev = index
    return result


def check_mistakes(expression):
    brackets_statck = Stack.Stack()
    for element in expression:
        if element == '(':
            brackets_statck.push('(')
        elif element == ')':
            if brackets_statck.is_empty():
                return ""       # not-pared brackets
            brackets_statck.pop()
    if not brackets_statck.is_empty():
        return ""       # not-pared brackets
    return True


def separate(expression):       # separates expression to logical parts
    expression_list = []
    flag = "number"
    current = ''
    for char in expression:
        if '0' <= char <= '9' or char == '.':              # if part is number
            if flag == 'number':            # if previously symbols were numbers
                current += char
            else:                           # if previously symbols weren't number
                if current != '':
                    if flag == 'sign' and len(re.findall('-', current)) + len(re.findall("/+", current)) > 1:
                        if (-1) ** len(re.findall('-', current)) < 0:
                            current = '-'
                        else:
                            current = '+'
                    expression_list.append(current)
                    current = ''
                flag = 'number'
                current += char
        elif 'a' <= char.lower() <= 'z':
            if flag == 'function':          # if previously symbols were function
                current += char
            else:                           # if previously symbols weren't numbers
                if current != '':
                    if flag == 'sign' and len(re.findall('-', current)) + len(re.findall('\+', current)) > 1:
                        if (-1) ** len(re.findall('-', current)) < 0:
                            current = '-'
                        else:
                            current = '+'
                    expression_list.append(current)
                    current = ''
                flag = 'function'
                current += char
        elif char in signs:                 # if previously symbols were sign
            if flag == 'sign':
                current += char
            else:                           # if previously symbols weren't numbers
                if current != '':
                    expression_list.append(current)
                    current = ''
                flag = 'sign'
                current += char
        elif char in ['(', ')']:
            if current != '':
                if flag == 'sign' and len(re.findall('-', current)) + len(re.findall('\+', current)) > 1:
                    if (-1) ** len(re.findall('-', current)) < 0:
                        current = '-'
                    else:
                        current = '+'
                expression_list.append(current)
                current = ''
            flag = 'bracket'
            expression_list.append(char)
        elif char == ',':
            if current != '':
                expression_list.append(current)
                current = ''
            flag = 'args'
            expression_list.append(char)
    if current != '':
        expression_list.append(current)
    return expression_list


def calc(expression):
    expression.append("+")
    expression.append("0")
    global functions
    brackets = False
    stack = Stack.Stack()
    result = 0
    main_number = ''
    main_sign = '+'
    func = ''
    sign = ''
    power_stack = Stack.Stack()
    for index, element in enumerate(expression):
        if brackets:        # if in we find expression in brackets, we start searching of end bracket with stack
            if element == '(':
                stack.push('(')
            elif element == ')':
                stack.pop()
                if stack.is_empty():
                    end = index
                    if func != '':
                        temp = get_args(expression[begin + 1:end])
                        if temp != ['']:
                            element = functions[func](*temp)       # getting arguments fo func
                        else:
                            element = functions[func]()
                        func = ''
                    else:
                        element = float(calc(expression[begin + 1:end]))
                    if main_number != '':
                        if sign != '':
                            if sign == '*':
                                main_number = str(float(main_number) * element)
                            elif sign == '/':
                                main_number = str(float(main_number) / element)
                            elif sign == '//':
                                main_number = str(float(main_number) // element)
                            elif sign == '%':
                                main_number = str(float(main_number) % element)
                            elif sign == '^':  # Not realised!
                                power_stack.push(element)
                            sign = ''
                    else:
                        main_number = str(element)
                    brackets = False

        else:               # if no in stack
            if element in math_consts:
                element = str(math_consts[element])
            if element == '(':
                brackets = True
                begin = index
                stack.push('(')

            elif element in functions:
                func = element

            elif element in signs:
                if element == '^':            # Not realised!
                    sign = '^'
                else:
                    if not power_stack.is_empty():
                        last = float(power_stack.pop())
                        if power_stack.is_empty():
                            main_number = str(float(main_number) ** last)
                        else:
                            while not power_stack.is_empty():
                                last = float(power_stack.pop()) ** last
                                main_number = str(float(main_number) ** last)
                    if element in ['+', '-']:
                        if main_number != '':
                            if main_sign == '+':
                                result += float(main_number)
                            elif main_sign == '-':
                                result -= float(main_number)
                        main_number = ''
                        main_sign = element
                    elif element in ['*', '/', '//', '%']:
                        sign = element

            else:
                if sign == '^':
                    power_stack.push(element)
                    sign = ''
                else:
                    if main_number != '':
                        if sign != '':
                            if sign == '*':
                                main_number = str(float(main_number) * float(element))
                            elif sign == '/':
                                main_number = str(float(main_number) / float(element))
                            elif sign == '//':
                                main_number = str(float(main_number) // float(element))
                            elif sign == '%':
                                main_number = str(float(main_number) % float(element))
                            sign = ''
                    else:
                        main_number = element
    if main_number != '':
        if main_sign == '+':
            result += float(main_number)
        elif main_sign == '-':
            result -= float(main_number)
    if result == 0 and main_number == '':
        return ''
    else:
        return str(result)


def pycalc(expression, modules=list()):
    global functions
    if 'math' not in modules:
        modules.append('math')
    for module in modules:
        workspace = importlib.import_module(module)
        for name in dir(workspace):
            functions[name] = getattr(workspace, name)
    # expression += "+0"
    expression = separate(expression)
    if check_mistakes(expression):
        for index, element in enumerate(expression):
            if element in logical_signs:
                left = float(calc(expression[:index]))
                right = float(calc(expression[index+1:]))
                return logical_signs[element](left, right)
        result = float(calc(expression))
        return result

# 1 --- 1
# -+---+-1
# 10^(2+1)
# log10(100)
# abs(-5)

