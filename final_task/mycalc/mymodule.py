import math
import operator
import argparse


ARITHMETIC_OPERATORS = {'*': operator.mul, '%': operator.mod, '//': operator.floordiv, '^': operator.pow,
                        '/': operator.truediv, '+': operator.add, '-': operator.sub}
COMPARE = {'>': operator.gt, '<': operator.lt, '!=': operator.ne, '==': operator.eq,
           '>=': operator.ge, ' <=': operator.le}
CONSTANT = {'e': math.e, 'pi': math.pi, 'tau': math.tau, '-e': -math.e, '-pi': -math.pi,
            '-tau': -math.tau, '+e': math.e, '+pi': math.pi, '+tau': math.tau, 'False': False, 'True': True}
FUNCTIONS = dict([(attr, getattr(math, attr)) for attr in dir(math) if callable(getattr(math, attr))])
FUNCTIONS['abs'], FUNCTIONS['round'] = abs, round


def byild_parser():
    parser = argparse.ArgumentParser(description='Pure-python command line calculator.')
    parser.add_argument('EXPRESSION', help='expression string to evalute. for example: \
                        "(e + pi)^pi + 3" get the answer: 261.45937196674714', type=str)
    parser.add_argument('-m', '--module', action='store', required=False, nargs="?",
                        dest='initroot', const=True, default=False, type=float, help='Use the module \
                        to find all the complex roots of polynomial equations with real coefficients \
                        of degree no more than 4. For example: \
                        "sin(pi/2)*x^3 - exp(e^2)*x = 666*x^2 + 1" -m get the answer: \
                        x_1 = 668.42, x_2 = -2.42, x_3 = 0. You can use the optional INITROOT argument \
                        to find the approximate value of the real root of an equation for one variable "x". \
                        INITROOT - the initial approximation of the root. For example: " cos(x) = x^3 " -m 3 \
                        get the answer: x_1 = 0.865474033. Used modified iteration Newton method with accuracy 1e-7.')
    args = parser.parse_args()
    return args


def first_function(expression):
    expression = expression.strip()
    if expression in '':
        raise ValueError('empty string')
    return expression


def find_comparsion(expression):
    begin = 0
    lst_expression = []
    comparsion = []
    tup = ('>', '<', '!', '=')
    if expression[0] in tup or expression[-1] in tup:
        raise ValueError
    for indx, elem in enumerate(expression):
        if elem in '><=!':
            lst_expression.append(expression[begin:indx])
            comparsion.append(elem)
            begin = indx + 1
    lst_expression.append(expression[begin:])
    quantity = lst_expression.count('')
    while quantity != 0:
        indx = lst_expression.index('')
        del lst_expression[indx]
        comparsion[indx-1:indx+1] = [comparsion[indx-1]+comparsion[indx]]
        quantity -= 1
    return [comparsion, lst_expression]


def calc_logical(lst):
    [compare_list, number_list] = lst
    if compare_list:
        logic = True
        for indx, elem in enumerate(compare_list):
            try:
                x = calculation_without_brackets(number_list[indx])
                y = calculation_without_brackets(number_list[indx+1])
                logic *= COMPARE[elem](x, y)
            except KeyError:
                raise KeyError('ERROR: unknown compare operator', elem)
        return bool(logic)
    else:
        return calculation_without_brackets(number_list[0])


def replace_power(expression, lst_numbers):
    i = expression.rfind('^')
    if i == -1:
        return expression, lst_numbers
    else:
        if lst_numbers[i] < 0:
            power = (-lst_numbers[i]) ** lst_numbers[i+1]
            lst_numbers[i:i+2] = [-power]
            return replace_power(expression[:i], lst_numbers)
        else:
            power = lst_numbers[i] ** lst_numbers[i+1]
            lst_numbers[i:i+2] = [power]
            return replace_power(expression[:i], lst_numbers)


def del_space(expression, val):
    for elem in val:
        lst = list(map(lambda x: x.strip(), expression.split(elem)))
        expression = elem.join(lst)
    return expression


def replace_many_plus_minus(expression):
    A = {'++': '+', '--': '+', '-+': '-', '+-': '-'}
    for key, value in A.items():
        if key in expression:
            expression = expression.replace(key, value)
            return replace_many_plus_minus(expression)
    return expression


def plus_reject(expression):
    A = {'+': 1, '-': 0}
    begin = 1
    lst_expression = []
    expr = del_space(expression, '+-')
    expr = ' ' + replace_many_plus_minus(expr)
    for indx, elem in enumerate(expr[2:]):
        if elem in '+-' and expr[indx+1] not in ('/', '%', '^', '*'):
            if expr[indx+1] == 'e' and expr[indx].isdigit():
                continue
            lst_expression.append(expr[begin:indx+2])
            begin = indx + 2 + A[elem]
    lst_expression.append(expr[begin:])
    return lst_expression


def calculation(expression):
    lst_expression = expression.split('//')
    lst_numbers = list(map(calculation_without_quotient, lst_expression))
    total = lst_numbers[0]
    for indx in range(1, len(lst_numbers)):
        total = total // lst_numbers[indx]
    return total


def calculation_without_quotient(expression):
    lst_numbers = []
    operations = ''
    begin = 0
    for indx, elem in enumerate(expression):
        if elem in '*/%^':
            operations += elem
            lst_numbers.append(expression[begin:indx])
            begin = indx + 1
    lst_numbers.append(expression[begin:])
    for indx, elem in enumerate(lst_numbers):
        elem = elem.strip()
        if elem in '':
            raise ValueError('empty string between operator')
        if elem in CONSTANT:
            lst_numbers[indx] = CONSTANT[elem]
        else:
            try:
                lst_numbers[indx] = float(lst_numbers[indx])
            except ValueError:
                raise ValueError(lst_numbers[indx])
    replace_power(operations, lst_numbers)
    operations = operations.replace('^', '')
    total = lst_numbers[0]
    for indx, elem in enumerate(operations):
        total = ARITHMETIC_OPERATORS[elem](total, lst_numbers[indx+1])
    return total


def calculation_without_brackets(expression):
    lst_expression = plus_reject(expression)
    if len(lst_expression) == 1:
        return calculation(lst_expression[0])
    else:
        return sum(list(map(calculation, lst_expression)))


def find_brackets(expression):
    end = expression.find(')')
    if end != -1:
        begin = expression[:end].rfind('(')
        if begin != -1:
            indx = begin
            rad = expression[begin+1:end].split(',')
            val_1 = list(map(find_comparsion, rad))
            val_2 = list(map(calc_logical, val_1))
            expression = expression.replace(expression[begin:end+1], str(val_2)[1:-1], 1)
            expression = find_func(expression, indx, val_2)
            return find_brackets(expression)
        else:
            raise ValueError('brackets are not balanced')
    elif expression.find('(') != -1:
        raise ValueError('brackets are not balanced')
    else:
        return expression


def find_func(expression, indx, val):
    st = expression[indx-1::-1]
    i = indx
    for elem in st:
        if (elem not in ARITHMETIC_OPERATORS) and (elem not in ('>', '<', '=', '(')):
            i -= 1
        else:
            break
    st = expression[i:indx]
    st1 = st.strip()
    if st1 in '':
        return expression
    else:
        try:
            expression = expression.replace(st+str(val)[1:-1], str(FUNCTIONS[st1](val)), 1)
        except KeyError:
            raise KeyError('ERROR: unknown function {}'.format(st1))
        except TypeError:
            expression = expression.replace(st+str(val)[1:-1], str(FUNCTIONS[st1](*val)), 1)
        return expression


def total_calculation(expression):
    a = first_function(expression)
    result1 = find_brackets(a)
    compare = find_comparsion(result1)
    total = calc_logical(compare)
    return total
