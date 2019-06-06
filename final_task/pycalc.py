import re
from argparse import ArgumentParser
from math import *

""" global variables for tolerance to be used if isclose function is called """
r = 1e-09
a = 0.0

"""  left-associated functions from math """
Left_func = [sin, cos, tan, asin, acos, atan, asinh, acosh, atanh, sinh, cosh, tanh, exp, abs, round,
            fabs, floor, frexp, trunc, ceil, expm1, sqrt, degrees, radians, erf, log, log10, log2, log1p,
            erfc, gamma, lgamma]
"""  names of left-associated functions from math """
Left_func_names = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'asinh', 'acosh', 'atanh', 'sinh', 'cosh', 'tanh',
                   'exp', 'abs', 'round', 'erfc', 'gamma', 'lgamma','fabs', 'floor', 'frexp', 'trunc', 'ceil',
                   'expm1', 'sqrt', 'degrees', 'radians', 'erf', 'log10', 'log1p', 'log2']

"""  establishes precedence for operators """
precedences_dic = {'eq': 0.2, 'noneq': 0.2, 'eqmore': 0.2, 'eqless': 0.2, '>': 0.2, '<': 0.2, 'neg': 4, '+': 1, '-': 1,
                   '*': 2, '/': 2, '//': 2, '%': 2, '(': 8, ')': 8, '!': 5, '^': 3.9, 'pow': 3.9, 'sin': 4,
                   'asin': 4, 'acos': 4,  'atan': 4, 'asinh': 4, 'acosh': 4, 'atanh': 4, 'sinh': 4, 'cosh': 4,
                   'tanh': 4, 'cos': 4, 'tan': 4, 'exp': 4, 'log': 4, 'log10': 4, ',': 0.9, 'abs': 5, 'round': 5,
                   'ceil': 4, 'isnan': 0.2, 'isinf': 0.2, 'isfinite': 0.2, 'isclose': 0.2, 'log2': 4,
                   'copysign': 4, 'fabs': 4,  'floor': 4, 'fmod': 4, 'frexp': 4, 'ldexp': 4, 'modf': 0.2, 'trunc': 4,
                   'expm1': 4, 'log1p': 4, 'gcd': 4, 'sqrt': 4, 'atan2': 4, 'degrees': 4, 'hypot': 4,
                   'radians': 4, 'erf': 4, 'erfc': 4, 'gamma': 4, 'lgamma': 4}
"""  left-associated functions and logical operators """
left_association = {'neg': 4, 'sin': 4, 'cos': 4, 'tan': 4, 'asin': 4, 'acos': 4, 'atan': 4, 'asinh': 4, 'acosh': 4,
                    'atanh': 4, 'sinh': 4, 'cosh': 4, 'tanh': 4, 'exp': 4, 'log': 4, 'log10': 4, 'abs': 5, 'round': 5,
                    'fabs': 4, 'floor': 4, 'frexp': 4, 'trunc': 4, 'ceil': 4, 'isnan': 0.2, 'isinf': 0.2,
                    'isfinite': 0.2, 'expm1': 4, 'log1p': 4, 'sqrt': 4, 'degrees': 4, 'modf': 0.2, 'log2': 4,
                    'radians': 4, 'erf': 4, 'erfc': 4, 'gamma': 4, 'lgamma': 4}


def validate_number(unit):
    """ evaluates whether unit is a float number """
    try:
        float(unit)
        return True
    except ValueError:
        return False


def validate_expression(items):
    """ checks for inappropriate whitespaces """
    for i in range(len(items)):
        try:
            validate_items(items[i], items[i+1])
        except IndexError:
            return items


def validate_items(item1, item2):
    """ detects error cases """
    if validate_number(item1) and validate_number(item2):
        print('ERROR: Two or more numbers in a row. Please make sure all operators are present.')
        exit(1)
    elif item1 == '/' and item2 == '/':
        print('ERROR: Please remove the whitespace if you require a floor division.')
        exit(1)
    elif item1 == '*' and item2 == '*':
        print('ERROR: Please use "^" operator for power calculation.')
        exit(1)
    else:
        return True


def validate_precedence(operator1, operator2):
    """ defines precedence for operators basing on a dictionary """
    if precedences_dic[operator1] == precedences_dic[operator2] and precedences_dic[operator1] == 3.9:
        return False
    else:
        return precedences_dic[operator1] >= precedences_dic[operator2]


def fsum_parser(items):
    """ evaluates fsum function and returns the outcome back into the arguments list """
    fsumlist = []
    for unit in items:
        if validate_number(unit):
            fsumlist.append(float(unit))
        elif unit in ('[', ']'):
            fsumlist.append(unit)
    i = fsumlist.index('[')+1
    j = fsumlist.index(']')
    del fsumlist[j:]
    del fsumlist[:i]
    k = items.index('fsum')
    m = items.index(']')+2
    kitems = items[:k]
    kitems.append(math.fsum(fsumlist))
    mitems = items[m:]
    items = kitems+mitems
    return items


def isclose_parser(items):
    """ formats isclose function and accepts tolerance values (if any) to two global variables """
    if 'rel_tol' in items:
        ri = items.index('rel_tol') + 2
        global r
        r = float(items[ri])
    if 'abs_tol' in items:
        ai = items.index('abs_tol') + 2
        global a
        a = float(items[ai])
    if 'rel_tol' in items:
        cut = items.index('rel_tol') - 1
        del items[cut:]
    if 'abs_tol' in items:
        cut = items.index('abs_tol') - 1
        del items[cut:]
    items.append(")")
    return items


def left_function(operator, value, operands):
  """ calculates left-associated functions """
    for function in Left_func:
        if function.__name__ == operator and operator in ['log10', 'log1p', 'log2']:
            try:
                operands.append(function(value))
            except ValueError:
                print('ERROR: Logarithm impossible to calculate.')
                exit(1)
        elif function.__name__ == operator:
            operands.append(function(value))
    return operands


def calculate(operators, operands):
    """ defines operators decision tree and performs basic operations """

    operator = operators.pop()
    y = None
    if operator != "!":
        y = operands.pop()
    x = None
    if operator in Left_func_names:
        left_function(operator, y, operands)
        return operands
    if operator not in left_association:
        x = operands.pop()
    if operator == "+":
        operands.append(x + y)
    elif operator == "-":
        if x:
            operands.append(x - y)
        else:
            operands.append(-y)
    elif operator == "neg":
        operands.append(-y)
    elif operator == "*":
        operands.append(x * y)

    elif operator == "/":
        try:
            operands.append(x / y)
        except ZeroDivisionError:
            print('ERROR: Cannot divide by zero')
            exit(1)
    elif operator == "%":
        try:
            operands.append(x % y)
        except ZeroDivisionError:
            print('ERROR: Cannot divide by zero')
            exit(1)
    elif operator == "//":
        try:
            operands.append(x // y)
        except ZeroDivisionError:
            print('ERROR: Cannot divide by zero')
            exit(1)

    elif operator == "^":
        operands.append(pow(x, y))
    elif operator == "!":
        try:
            operands.append(factorial(x))
        except ValueError:
            print('ERROR: Factorial impossible to calculate.')
            exit(1)
    elif operator == "log":
        try:
            operands.append(log(y))
        except ValueError:
            print('ERROR: Logarithm impossible to calculate.')
            exit(1)

    elif operator == ",":
        if operators[-2] == 'log':
            operators.pop(-2)
            try:
                operands.append(log(x, y))
            except ValueError:
                print('ERROR: Logarithm impossible to calculate.')
                exit(1)

        elif operators[-2] == 'pow':
            operators.pop(-2)
            operands.append(pow(x, y))

        elif operators[-2] == 'copysign':
            operators.pop(-2)
            operands.append(copysign(x, y))

        elif operators[-2] == 'fmod':
            operators.pop(-2)
            operands.append(fmod(x, y))

        elif operators[-2] == 'ldexp':
            operators.pop(-2)
            operands.append(ldexp(x, y))

        elif operators[-2] == 'hypot':
            operators.pop(-2)
            operands.append(hypot(x, y))

        elif operators[-2] == 'atan2':
            operators.pop(-2)
            operands.append(atan2(y, x))

        elif operators[-2] == 'gcd':
            y = int(y)
            x = int(x)
            operators.pop(-2)
            operands.append(gcd(y, x))

        elif operators[-2] == 'isclose':
            global r
            global a
            print(isclose(x, y, rel_tol=r, abs_tol=a))
            exit(1)

        else:
            print("ERROR: Function unknown. If a comma is used as a delimiter, please use a dot instead.")
            exit(1)

    # Logical operators produce output and exit from calculate, not from main
    elif operator == "isinf":
        print(isinf(y))
        exit(1)
    elif operator == "isnan":
        print(isnan(y))
        exit(1)
    elif operator == "modf":
        print(modf(y))
        exit(1)
    elif operator == "isfinite":
        print(isfinite(y))
        exit(1)
    elif operator == 'eq':
        print(bool(x == y))
        exit(1)
    elif operator == '>':
        print(bool(x > y))
        exit(1)
    elif operator == '<':
        print(bool(x < y))
        exit(1)
    elif operator == 'noneq':
        print(bool(x != y))
        exit(1)
    elif operator == 'eqmore':
        print(bool(x >= y))
        exit(1)
    elif operator == 'eqless':
        print(bool(x <= y))
        exit(1)
    else:
        print('ERROR: Operator or function unknown')
        exit(1)


def clear_format(expression):
    """ removes whitespaces """
    exp = expression
    exp = exp.replace(" ", "")
    units = pre_format(exp)
    return units


def pre_format(expression):
    """ formats input expression to acceptable readout """
    exp = expression
    if exp[0] == "-":
        exp = '0-'+exp[1:]
    exp = exp.replace("(-", "(0-").replace("--", "-0+").replace("+-", "+0-").replace("[", " [ ")
    exp = exp.replace("--", "-0+").replace("-+", "-0+").replace(",-", ", 0-").replace("]", " ] ")
    exp = exp.replace('*-', '* neg ').replace(' -', ' neg ').replace('^-', '^ neg ').replace('/-', '/ neg ')
    exp = exp.replace('>-', '> neg ').replace('<-', '< neg ').replace('=-', '= neg ')
    exp = exp.replace("-", " - ").replace("+", " + ").replace("*", " * ").replace("/", " / ")
    exp = exp.replace("/  /", " // ").replace("%", " % ").replace("^", " ^ ").replace(",", " , ")
    exp = exp.replace("(", " ( ").replace(")", " ) ").replace("%", " % ")
    exp = exp.replace("==", " eq ").replace("!=", " <> ").replace(">=", " eqmore ").replace("<=", " eqless ")
    exp = exp.replace("=", " = ").replace("<>", " noneq ").replace(">", " > ").replace("<", " < ").replace("!", " !")
    items = exp.split()
    # preliminary check for some error cases and two functions, fsum and isclose
    if "isclose" and "=" in items:
        items = isclose_parser(items)
    if len([i for i, x in enumerate(items) if x in ['>', 'eq', 'noneq', 'eqless', 'eqmore', '<']]) > 1:
        print("ERROR: Cannot have more than one comparison operator in an expression.")
        exit(1)
    if len([i for i, x in enumerate(items) if x in ['(']]) != len([i for i, x in enumerate(items) if x in [')']]):
        print("ERROR: Unbalanced parentheses.")
        exit(1)
    if "=" in items:
        print("ERROR: Please use '==', '!=', '>=', '<=', '>', '<' if you require a boolean comparison.")
        exit(1)
    if "fsum" in items:
        items = fsum_parser(items)
    return items


def process(expression):
    """ checks for validation results and processes the expression """
    operands = []
    operators = []
    items = pre_format(expression)
    validate_expression(items)
    units = clear_format(expression)
    for unit in units:
        if validate_number(unit):
            operands.append(float(unit))
        # handles constants
        elif unit == 'pi':
            operands.append(math.pi)
        elif unit == 'e':
            operands.append(math.e)
        elif unit == 'tau':
            operands.append(math.tau)
        elif unit == 'inf':
            operands.append(math.inf)
        elif unit == 'NaN':
            operands.append(math.nan)

        elif unit == '(':
            operators.append(unit)
        elif unit == ')':
            # Shunting-yard protocol
            nextop = operators[-1] if operators else None
            while nextop is not None and nextop != '(':
                calculate(operators, operands)
                nextop = operators[-1] if operators else None
            operators.pop()
        else:
            #  Operator is moved into processing
            nextop = operators[-1] if operators else None
            while nextop is not None and nextop != ')' and nextop != '(' and validate_precedence(nextop, unit):
                calculate(operators, operands)
                nextop = operators[-1] if operators else None
            operators.append(unit)
    while operators:
        calculate(operators, operands)

    return operands[0] if operands else None


def exp_parser():
    """ retrieves expression from the command line """
    parser = ArgumentParser('PyCalc', description='Pure-Python command-line calculator',
                            usage='pycalc [-h] EXPRESSION')
    parser.add_argument('--expr', action='store_true',
                        help='Evaluates an expression string. Please wrap the string with " ".')
    parsed, args = parser.parse_known_args()
    expression = ''.join(args)
    return str(expression)


def main():
    """ receives expression from parser, launches processing and produces output """
    expression = exp_parser()
    if len(expression) == 0:
        # attempt to receive an expression via manual input
        expression = str(input('No expression is received from the command line. Please enter an expression: '))
    try:
        print(process(expression))
    except Exception as ex:
        print("ERROR: Please check arguments and operators in this expression."
              "\nTo reduce the chance of error please wrap the expression with \" \"."
              " Program internal message: {0}".format(str(ex)))
        exit(1)


if __name__ == '__main__':
    main()
