import re
from argparse import ArgumentParser
import math

#  establishes precedence for operators
precedences_dic = {'eq': 0.2, 'noneq': 0.2, 'eqmore': 0.2, 'eqless': 0.2, '>': 0.2, '<': 0.2, 'neg': 4, '+': 1, '-': 1,
                   '*': 2, '/': 2, '//': 2, '%': 2, '(': 8, ')': 8, '!': 5, '^': 3.9, 'pow': 3.9, 'sin': 4, 'cos': 4, 'tan': 4,
                   'asin': 4, 'acos': 4,  'atan': 4, 'asinh': 4, 'acosh': 4, 'atanh': 4, 'sinh': 4, 'cosh': 4,
                   'tanh': 4, 'exp': 4, 'log': 4, 'log10': 4, ',': 0.9, 'abs': 5, 'round': 5}
#  establishes left-associated operators
left_association = {'neg': 4, 'sin': 4, 'cos': 4, 'tan': 4, 'asin': 4, 'acos': 4, 'atan': 4, 'asinh': 4, 'acosh': 4,
                    'atanh': 4, 'sinh': 4, 'cosh': 4, 'tanh': 4, 'exp': 4, 'log': 4, 'log10': 4, 'abs': 5, 'round': 5}


def validate_number(unit):
    # evaluates whether unit is a float number
    try:
        float(unit)
        return True
    except ValueError:
        return False


def validate_expression(items):
    # checks for inappropriate whitespaces
    for i in range(len(items)):
        try:
            validate_items(items[i], items[i+1])
        except IndexError:
            return items


def validate_items(item1, item2):
    # detects error cases
    if validate_number(item1) and validate_number(item2):
        print('ERROR: Two or more numbers in a row. Please make sure all operators are present.')
        exit(1)
    elif item1 == '/' and item2 == '/':
        print('ERROR: Please remove the whitespace if you require a floor division.')
        exit(1)
    elif item1 == '*' and item2 == '*':
        print('ERROR: Please use "^" operator for power calculation.')
        exit(1)
    elif item1 == 'sqrt':
        print('ERROR: Please use "^" operator for power calculation. Sqrt would be ^0.5.')
        exit(1)
    else:
        return True


def validate_precedence(operator1, operator2):
    # defines precedence for operators basing on a dictionary
    if precedences_dic[operator1] == precedences_dic[operator2] and precedences_dic[operator1] == 3.9:
        return False
    else:
        return precedences_dic[operator1] >= precedences_dic[operator2]


def calculate(operators, operands):
    # defines operators' decision tree and performs basic operations

    operator = operators.pop()
    y = None
    if operator != "!":
        y = operands.pop()
    x = None
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
        operands.append(math.pow(x, y))
    elif operator == "!":
        operands.append(math.factorial(x))
    elif operator == "sin":
        operands.append(math.sin(y))
    elif operator == "cos":
        operands.append(math.cos(y))
    elif operator == "tan":
        operands.append(math.tan(y))
    elif operator == "acos":
        operands.append(math.acos(y))
    elif operator == "asin":
        operands.append(math.asin(y))
    elif operator == "atan":
        operands.append(math.atan(y))
    elif operator == "acosh":
        operands.append(math.acosh(y))
    elif operator == "asinh":
        operands.append(math.asinh(y))
    elif operator == "atanh":
        operands.append(math.atanh(y))
    elif operator == "cosh":
        operands.append(math.cosh(y))
    elif operator == "sinh":
        operands.append(math.sinh(y))
    elif operator == "tanh":
        operands.append(math.tanh(y))
    elif operator == "exp":
        operands.append(math.exp(y))
    elif operator == "log":
        operands.append(math.log(y))
    elif operator == ",":
        if operators[-2] == 'log':
            operators.pop(-2)
            operands.append(math.log(x, y))
        elif operators[-2] == 'pow':
            operators.pop(-2)
            operands.append(math.pow(x, y))
        else:
            print("ERROR: Cannot accept comma as a delimiter. Please use a dot instead.")
            exit(1)
    elif operator == "log10":
        operands.append(math.log10(y))
    elif operator == "abs":
        operands.append(abs(y))
    elif operator == "round":
        operands.append(round(y))
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
    # removes whitespaces
    exp = expression
    exp = exp.replace(" ", "")
    units = pre_format(exp)
    return units


def pre_format(expression):
    # formats input expression to acceptable readout
    exp = expression
    if exp[0] == "-":
        exp = '0-'+exp[1:]
    exp = exp.replace("(-", "(0-").replace("--", "-0+").replace("+-", "+0-")
    exp = exp.replace("--", "-0+")
    exp = exp.replace("-+", "-0+")
    exp = exp.replace('*-', '* neg ').replace(' -', ' neg ').replace('^-', '^ neg ').replace('/-', '/ neg ')
    exp = exp.replace('>-', '> neg ').replace('<-', '< neg ').replace('=-', '= neg ')
    exp = exp.replace("-", " - ").replace("+", " + ").replace("*", " * ").replace("/", " / ")
    exp = exp.replace("/  /", " // ").replace("%", " % ").replace("^", " ^ ").replace(",", " , ")
    exp = exp.replace("(", " ( ").replace(")", " ) ").replace("%", " % ")
    exp = exp.replace("==", " eq ").replace("!=", " <> ").replace(">=", " eqmore ").replace("<=", " eqless ")
    exp = exp.replace("=", " = ").replace("<>", " noneq ").replace(">", " > ").replace("<", " < ").replace("!", " !")
    items = exp.split()
    if len([i for i, x in enumerate(items) if x in ['>', 'eq', 'noneq', 'eqless', 'eqmore', '<']]) > 1:
        print("ERROR: Cannot have more than one comparison operator in an expression.")
        exit(1)
    if len([i for i, x in enumerate(items) if x in ['(']]) != len([i for i, x in enumerate(items) if x in [')']]):
        print("ERROR: Unbalanced parentheses.")
        exit(1)
    if "=" in items:
        print("ERROR: Please use '==', '!=', '>=', '<=', '>', '<' if you require a boolean comparison.")
        exit(1)
    return items


def process(expression):
    # checks for validation results and processes the expression
    operands = []
    operators = []
    items = pre_format(expression)
    validate_expression(items)
    units = clear_format(expression)
    for unit in units:
        if validate_number(unit):
            operands.append(float(unit))
        # handles two constants
        elif unit == 'pi':
            operands.append(math.pi)
        elif unit == 'e':
            operands.append(math.e)
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
    parser = ArgumentParser('PyCalc', description='Pure-Python command-line calculator',
                            usage='pycalc [-h] EXPRESSION [-m]	MODULE	[MODULE	...]]')
    parser.add_argument('--expr', action='store_true',
                        help='Evaluates an expression string. Please wrap the string with " ".')
    parsed, args = parser.parse_known_args()
    expression = ''.join(args)
    return str(expression)


def main():
    expression = exp_parser()
    if len(expression) == 0:
        expression = str(input('No expression is received as an argument. Please enter an expression to evaluate: '))
    try:
        print(process(expression))
    except Exception as ex:
        print("ERROR: Please check arguments and operators in this expression."
              "\nTo reduce the chance of error please wrap the expression with \" \"."
              " Program internal message: {0}".format(str(ex)))
        exit(1)


if __name__ == '__main__':
    main()
