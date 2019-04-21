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
    parser.add_argument('expression', help='expression string to evalute', type=str)
    args = parser.parse_args()
    return args


def first_function(stroka):
    stroka = stroka.strip()
    if stroka in '':
        raise ValueError('empty string')
    return stroka


def find_comparsion(stroka):
    begin = 0
    lst_expression = []
    comparsion = []
    tup = ('>', '<', '!', '=')
    if stroka[0] in tup or stroka[-1] in tup:
        raise ValueError
    for indx, elem in enumerate(stroka):
        if elem in '><=!':
            lst_expression.append(stroka[begin:indx])
            comparsion.append(elem)
            begin = indx + 1
    lst_expression.append(stroka[begin:])
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


def replace_power(stroka, lst_numbers):
    i = stroka.rfind('^')
    if i == -1:
        return stroka, lst_numbers
    else:
        if lst_numbers[i] < 0:
            power = (-lst_numbers[i]) ** lst_numbers[i+1]
            lst_numbers[i:i+2] = [-power]
            return replace_power(stroka[:i], lst_numbers)
        else:
            power = lst_numbers[i] ** lst_numbers[i+1]
            lst_numbers[i:i+2] = [power]
            return replace_power(stroka[:i], lst_numbers)


def del_space(stroka):
    for elem in '+-':
        lst = list(map(lambda x: x.strip(), stroka.split(elem)))
        stroka = elem.join(lst)
    return stroka


def replace_many_plus_minus(stroka):
    A = {'++': '+', '--': '+', '-+': '-', '+-': '-'}
    for key, value in A.items():
        if key in stroka:
            stroka = stroka.replace(key, value)
            return replace_many_plus_minus(stroka)
    return stroka


def plus_reject(stroka):
    A = {'+': 1, '-': 0}
    begin = 0
    lst_expression = []
    for indx, elem in enumerate(stroka):
        if elem in '+-' and stroka[indx-1] not in ('/', '%', '^', '*'):
            lst_expression.append(stroka[begin:indx])
            begin = indx+A[elem]
    lst_expression.append(stroka[begin:])
    if lst_expression[0] == '': lst_expression.remove('')
    return lst_expression


def calculation(stroka):
    lst_numbers = []
    operations = ''
    begin = 0
    for indx, elem in enumerate(stroka):
        if elem in '*/%^':
            operations += elem
            lst_numbers.append(stroka[begin:indx])
            begin = indx + 1
    lst_numbers.append(stroka[begin:])
    for indx, elem in enumerate(lst_numbers):
        elem = elem.strip()
        if elem in '': raise ValueError('empty string between operator')
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


def calculation_without_brackets(stroka):
    stroka = del_space(stroka)
    stroka = replace_many_plus_minus(stroka)
    lst_expression = plus_reject(stroka)
    if len(lst_expression) == 1:
        return calculation(lst_expression[0])
    else:
        return sum(list(map(calculation, lst_expression)))


def find_brackets(stroka):
    end = stroka.find(')')
    if end != -1:
        begin = stroka[:end].rfind('(')
        if begin != -1:
            indx = begin
            rad = stroka[begin+1:end].split(',')
            val_1 = list(map(find_comparsion, rad))
            val_2 = list(map(calc_logical,val_1))
            stroka = stroka.replace(stroka[begin:end+1], str(val_2)[1:-1], 1)
            stroka = find_func(stroka, indx, val_2)
            return find_brackets(stroka)
        else:
            raise ValueError('brackets are not balanced')
    elif stroka.find('(') != -1:
        raise ValueError('brackets are not balanced')
    else:
        return stroka


def find_func(stroka, indx, val):
    st = stroka[indx-1::-1]
    i = indx
    for elem in st:
        if (elem not in ARITHMETIC_OPERATORS) and (elem not in ('>', '<', '=', '(')):
            i -= 1
        else:
            break
    st = stroka[i:indx]
    st1 = st.strip()
    if st1 in '':
        return stroka
    else:
        try:
            stroka = stroka.replace(st+str(val)[1:-1], str(FUNCTIONS[st1](*val)), 1)
        except KeyError:
            raise KeyError('ERROR: unknown function', st1)
        return stroka
