from argparse import ArgumentParser
from calculator import calc


def parse_command_line():
    parser = ArgumentParser(description='Pure-python command-line calculator')
    parser.add_argument('EXPRESSION', type=str, help='expression string to evaluate')
    parser.add_argument('-m', '--use-modules', required=False, nargs='+', help='additional modules to use')
    args = parser.parse_args()
    return args


def parse_added_modules():
    modules = parse_command_line().use_modules
    dicts_modules = []
    if modules is None:
        dicts_modules = None
    else:
        for item in modules:
            dicts_modules.append(__import__(item).__dict__)
    return dicts_modules


def is_error_spaces(expression):
    """This function first removes duplicate spaces.
     It then checks for spaces between functions and numbers and double operators.
    """

    expression = ' '.join(expression.split())
    for i in range(1, len(expression) - 1):
        if expression[i] == ' ':
            if expression[i - 1].isdigit() and expression[i + 1].isalnum():
                return True
            elif expression[i - 1] + expression[i + 1] in calc.OPERATION_PRIORITIES:
                return True
    return False


def is_error_brackets(expression):
    opening_brackets = 0
    closing_brackets = 0
    for i, item in enumerate(expression):
        if item == '(':
            opening_brackets += 1
            if not i and expression[i - 1].isdigit():
                return True
        elif item == ')':
            closing_brackets += 1
            if closing_brackets > opening_brackets or i != len(expression)-1 and expression[i+1].isdigit():
                return True
    if opening_brackets == closing_brackets:
        return False
    return True


def is_operator_check(item, bracket):
    if (item in calc.OPERATION_PRIORITIES or item == '!' or item == '=') and \
            item != '+' and item != '-' and item != bracket:
        return True
    return False


def is_error_operators(expression):
    """This function first checks for incorrect operators at the beginning and end.
    Then he looks for the wrong combination of operators.
    """

    if is_operator_check(expression[0], '(') or (expression[-1] in calc.OPERATION_PRIORITIES or expression[-1] == '!' or
                                                 expression[-1] == '=') and expression[-1] != ')':
        return True
    is_only_operators = True
    i = 0
    while i < len(expression)-1:
        if is_only_operators and expression[i].isalnum():
            is_only_operators = False
        if is_operator_check(expression[i], ')'):
            if is_operator_check(expression[i + 1], '('):
                if expression[i]+expression[i+1] in calc.OPERATION_PRIORITIES or expression[i]+expression[i+1] == '()':
                    i += 2
                    continue
                else:
                    return True
        i += 1
    else:
        if is_only_operators and expression[i].isalnum():
            is_only_operators = False
        if is_only_operators:
            return True
    return False


def check_exception():
    expression = parse_command_line().EXPRESSION
    try:
        dicts_modules = parse_added_modules()
    except ModuleNotFoundError:
        raise Exception('ERROR: Module Not Found')
    else:
        if expression is None or not expression.rstrip():
            raise Exception('ERROR: expression argument is required')
        elif is_error_spaces(expression):
            raise Exception('ERROR: spaces')
        else:
            expression = ''.join(expression.split())
            if is_error_brackets(expression):
                raise Exception('ERROR: brackets')
            elif is_error_operators(expression):
                raise Exception('ERROR: operator')
            else:
                return expression, dicts_modules
