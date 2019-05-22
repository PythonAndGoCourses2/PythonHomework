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

    def is_number(expression):
        for element in expression:
            if '0' >= element >= '9' and element != '.':
                return False
        return True
    if len(expression) == 0:
        print("ERROR: empty expression!")
        return False

    brackets_stack = Stack.Stack()
    for element in expression:
        if element == '(':
            brackets_stack.push('(')
        elif element == ')':
            if brackets_stack.is_empty():
                print("ERROR: brackets are not paired")
                return False
            brackets_stack.pop()
        elif element == " ": expression.remove(element)
    if not brackets_stack.is_empty():
        print("ERROR: brackets are not paired")
        return False

    if expression[len(expression)-1] in signs:
        print("ERROR: no number after operator")
        return False

    main_sign_count = 0
    l_sign_count = 0
    number_count = 0

    for index in range(len(expression)):
        if expression[index] in ['+', '-']:
            main_sign_count += 1

        elif expression[index] in ['*', '/', '^', '%', '//']:
            if number_count == 0:
                print("ERROR: no numbers before sign")
                return False
            if expression[index + 1] in ['*', '/', '^', '%', '//']:
                print("ERROR: wrong signs position")
                return False

        elif expression[index] in logical_signs:
            l_sign_count +=1
            if l_sign_count > 1:
                print("ERROR: more than one logical operator")
                return False

        elif is_number(expression[index]):
            number_count += 1

        elif expression[index].isalpha():
            if expression[index] in math_consts:
                number_count += 1
            elif expression[index] in functions:
                if expression[index + 1] != '(':
                    print("ERROR: no brackets after function")
                    return False
            else:
                print("ERROR: function does not exist")
                return False

    return True


def separate(expression):       # separates expression to logical parts

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
    return expression_list


def calc(expression):
    expression.append("/")          # creating airbag
    expression.append("1")
    expression.append("+")
    expression.append("0")

    global functions                # list of functions
    brackets = False                # flag, if we are looking for brackets
    result = 0                      # result variable
    main_number = ''                # variable for number after + or -
    number = ''                     # variable for other numbers
    main_sign = '+'                 # sign before main number (default +)
    func = ''                       # variable for function
    sign = ''                       # sign before number
    previous_sign = ''              # additionaly variable for sign
    stack = Stack.Stack()           # stack for brackets
    power_stack = Stack.Stack()     # stack for powered numbers

    for index, element in enumerate(expression):
        if brackets:        # if in we find expression in brackets, we start searching of end bracket with stack
            if element == '(':
                stack.push('(')
            elif element == ')':
                stack.pop()
                if stack.is_empty():
                    end = index
                    if func != '':                                      # if we find function
                        temp = get_args(expression[begin + 1:end])      # getting arguments for func
                        if temp != ['']:
                            element = functions[func](*temp)            # processing function with 1 or more args
                        else:
                            element = functions[func]()                 # processing function with no args
                        func = ''
                    else:
                        element = float(calc(expression[begin + 1:end]))    # if no function, just a brackets

                    if sign == '^':                                     # processing power operator section
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
            if element in math_consts:                  # if element is const
                element = str(math_consts[element])
            elif element == '-e':
                element = str(-1 * math.e)
            elif element == '-pi':
                element = str(-1 * math.pi)
            elif element == '+e':
                element = str(math.e)
            elif element == '+pi':
                element = str(math.pi)

            if element == '(':                          # start extracting expression in brackets
                brackets = True
                begin = index
                stack.push('(')

            elif element in functions:                  # if element is function
                func = element

            elif element in signs:                      # if element is sign
                if element == '^':                      # processing power operator
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

                    if element in ['+', '-']:                   # processing + or -
                        if main_number != '':
                            if number != '':
                                main_number = operators_type1[previous_sign](float(main_number), float(number))
                                number = ''
                                previous_sign = ''
                            result = operators_main[main_sign](result, float(main_number))
                        main_number = ''
                        main_sign = element

                    elif element in ['*', '/', '//', '%']:          # processing other operators
                        sign = element
            else:                                        # element is number
                if sign == '^':                       # if power operator stays before this element
                    power_stack.push(element)
                    sign = ''
                else:
                    if main_number != '':                  # if main_number was found
                        if sign != '':
                            if sign in ['*', '/', '//', '%']:
                                if number != '':
                                    main_number = operators_type1[previous_sign](float(main_number), float(number))
                                number = element
                            previous_sign = sign
                            sign = ''
                    else:
                        main_number = element

    if main_number != '':                                       # adding last number to result
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
    if 'math' not in modules:                       # including module math
        modules.append('math')
    for module in modules:                          # adding all functions to dictionary
        workspace = importlib.import_module(module)
        for name in dir(workspace):
            functions[name] = getattr(workspace, name)

    new = ''

    for char in expression:
        if char != ' ':
            new += char
    if check_mistakes(separate(expression)):                  # handling some mistakes
        expression = separate(new)                          # separating expression (look separate function)
        for index, element in enumerate(expression):       # looking for logical signs
            if element in logical_signs:
                left = float(calc(expression[:index]))
                right = float(calc(expression[index+1:]))
                return logical_signs[element](left, right)
        result = float(calc(expression))                    # start counting
        return result
