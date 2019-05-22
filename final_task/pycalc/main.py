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



operators_type1 = {
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '%': operator.mod
}

operators_main = {
    '+': operator.add,
    '-': operator.sub
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
    stack = Stack.Stack()
    for index, part in enumerate(expression):
        if part == ',' and stack.is_empty():
            result.append(float(calc(expression[prev + 1: index])))
            prev = index
        elif part == '(':
            stack.push(part)
        elif part == ')':
            stack.pop()
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
    new = ''

    for char in expression:
        if char != ' ':
            new += char

    expression = new

    def check_log10():
        nonlocal current
        nonlocal expression_list
        if current == '10' and expression_list[len(expression_list)-1] == 'log':
            expression_list.pop()
            expression_list.append('log10')
            current = ''

    def fix_signs():
        nonlocal flag
        nonlocal current
        if flag == 'sign_main' and len(re.findall('-', current)) + len(re.findall("\+", current)) > 1:
            if (-1) ** len(re.findall('-', current)) < 0:
                current = '-'
            else:
                current = '+'

    def is_number(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    expression_list = []
    flag = "number"
    current = ''
    for char in expression:
        if char == ' ':
            flag = 'space'
        elif '0' <= char <= '9' or char == '.':              # if part is number
            if flag == 'number':            # if previously symbols were numbers
                current += char
            else:                           # if previously symbols weren't number
                if current != '':
                    fix_signs()
                    expression_list.append(current)
                    current = ''
                flag = 'number'
                current += char
        elif 'a' <= char.lower() <= 'z':
            if flag == 'function':          # if previously symbols were function
                current += char
            else:                           # if previously symbols weren't numbers
                if current != '':
                    fix_signs()
                    expression_list.append(current)
                    current = ''
                flag = 'function'
                current += char

        elif char in operators_type1 or char == '^':                 # if previously symbols were sign
            if flag == 'sign_type1':
                current += char
            else:                           # if previously symbols weren't numbers
                if current != '':
                    expression_list.append(current)
                    current = ''
                flag = 'sign_type1'
                current += char

        elif char in signs:                 # if previously symbols were sign
            if flag == 'sign_main':
                current += char
            else:                           # if previously symbols weren't numbers
                if current != '':
                    expression_list.append(current)
                    current = ''
                flag = 'sign_main'
                current += char

        elif char in ['(', ')']:
            if current != '':
                check_log10()
                fix_signs()
                if current != '':
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

    index = 1
    while index <= len(expression_list)-1:
        if expression_list[index] in operators_main and\
                (expression_list[index-1] in operators_type1 or expression_list[index-1] == '^') and\
                (is_number(expression_list[index+1]) or expression_list[index+1] in math_consts):
            expression_list[index+1] = expression_list[index] + expression_list[index + 1]
            expression_list.pop(index)
        else:
            index += 1
    print(expression_list)
    return expression_list


def calc(expression):
    expression.append("/")
    expression.append("1")
    expression.append("+")
    expression.append("0")
    global functions
    brackets = False
    result = 0
    main_number = ''
    number = ''
    main_sign = '+'
    func = ''
    sign = ''
    previous_sign = ''
    stack = Stack.Stack()
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

                    if sign == '^':
                        power_stack.push(element)
                        sign = ''
                    else:
                        if main_number != '':
                            if sign != '':
                                if sign in ['*', '/', '//', '%']:
                                    if number != '':
                                        main_number = operators_type1[previous_sign](float(main_number), float(number))
                                    number = element
                                previous_sign = sign
                                sign = ''
                        else:
                            main_number = element
                    brackets = False

        else:               # if no in stack
            if element in math_consts:
                element = str(math_consts[element])
            elif element == '-e':
                element = str(-1 * math.e)
            elif element == '-pi':
                element = str(-1 * math.pi)
            elif element == '+e':
                element = str(math.e)
            elif element == '+pi':
                element = str(math.pi)

            if element == '(':
                brackets = True
                begin = index
                stack.push('(')

            elif element in functions:
                func = element          # 10*(2+1)/1+0

            elif element in signs:
                if element == '^':  # 1+9/3^2
                    sign = '^'
                else:
                    if not power_stack.is_empty():
                        last = float(power_stack.pop())
                        if power_stack.is_empty():
                            if number != '':
                                number = str(float(number) ** last)
                            else:
                                main_number = str(float(main_number) ** last)
                        else:
                            while not power_stack.is_empty():
                                last = float(power_stack.pop()) ** last
                                main_number = str(float(main_number) ** last)
                    if element in ['+', '-']:
                        if main_number != '':
                            if number != '':
                                main_number = operators_type1[previous_sign](float(main_number), float(number))
                                number = ''
                                previous_sign = ''
                            result = operators_main[main_sign](result, float(main_number))
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
                            if sign in ['*', '/', '//', '%']:
                                if number != '':
                                    main_number = operators_type1[previous_sign](float(main_number), float(number))
                                number = element
                            previous_sign = sign
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