import math
import operator
import argparse

A = {'*': operator.mul, '%': operator.mod, '//': operator.floordiv, '^': operator.pow,
     '/': operator.truediv, '+': operator.add, '-': operator.sub}
Compare = {'>': operator.gt, '<': operator.lt, '!=': operator.ne, '==': operator.eq,
           '>=': operator.ge, ' <=': operator.le}
Const = {'e': math.e, 'pi': math.pi, 'tau': math.tau, '-e': -math.e, '-pi': -math.pi,
         '-tau': -math.tau, '+e': math.e, '+pi': math.pi, '+tau': math.tau}
F = dict([(attr, getattr(math, attr)) for attr in dir(math) if callable(getattr(math, attr))])
F['abs'], F['round'] = abs, round


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
    i1 = 0
    lst = []
    op = []
    tup = ('>', '<', '!', '=')
    if stroka[0] in tup or stroka[-1] in tup:
        raise ValueError
    for elem in stroka:
        if '><=!'.find(elem) != -1:
            i2 = stroka.find(elem, i1)
            lst.append(stroka[i1:i2])
            op.append(elem)
            i1 = i2 + 1
    lst.append(stroka[i1:])
    col = lst.count('')
    while col != 0:
        i = lst.index('')
        del lst[i]
        op[i-1:i+1] = [op[i-1]+op[i]]
        col -= 1
    return [op, lst]


def replace_power(stroka, lst):
    i = stroka.rfind('^')
    if i == -1:
        return stroka, lst
    else:
        if lst[i] < 0:
            power = (-lst[i]) ** lst[i+1]
            lst[i:i+2] = [-power]
            return replace_power(stroka[:i], lst)
        else:
            power = lst[i] ** lst[i+1]
            lst[i:i+2] = [power]
            return replace_power(stroka[:i], lst)


def del_space(stroka):
    for elem in '+-':
        lst = list(map(lambda x: x.strip(), stroka.split(elem)))
        stroka = elem.join(lst)
    return stroka


def replace_many_plus_minus(stroka):
    if stroka.find('++') != -1:
        stroka = stroka.replace('++', '+')
    elif stroka.find('--') != -1:
        stroka = stroka.replace('--', '+')
    elif stroka.find('+-') != -1:
        stroka = stroka.replace('+-', '-')
    elif stroka.find('-+') != -1:
        stroka = stroka.replace('-+', '-')
    else:
        return stroka
    return replace_many_plus_minus(stroka)


def plus_reject(stroka):
    A = {'+': 1, '-': 0}
    i1 = 0
    lst = []
    for idx, elem in enumerate(stroka):
        if '+-'.find(elem) != -1 and stroka[idx-1] not in ('/', '%', '^', '*'):
            lst.append(stroka[i1:idx])
            i1 = idx+A[elem]
    lst.append(stroka[i1:])
    return lst


def result(stroka):
    s = []
    o = ''
    i1 = 0
    for elem in stroka:
        if '*/%^'.find(elem) != -1:
            i2 = stroka.find(elem, i1)
            o += elem
            s.append(stroka[i1:i2])
            i1 = i2 + 1
    s.append(stroka[i1:])
    for idx, elem in enumerate(s):
        elem = elem.strip()
        if elem in Const:
            s[idx] = Const[elem]
        else:
            try:
                s[idx] = float(s[idx])
            except ValueError:
                raise ValueError(s[idx])
    replace_power(o, s)
    o = o.replace('^', '')
    res = s[0]
    for idx, elem in enumerate(o):
        res = A[elem](res, s[idx+1])
    return res


def calc(stroka):
    stroka = '0+' + stroka
    stroka = del_space(stroka)
    stroka = replace_many_plus_minus(stroka)
    lst = plus_reject(stroka)
    return sum(list(map(result, lst)))


def find_brackets(stroka):
    global indx, valbr
    i = stroka.find(')')
    if i != -1:
        i2 = stroka[:i].rfind('(')
        if i2 != -1:
            indx = i2
            rad = stroka[i2+1:i].split(',')
            valbr = list(map(calc, rad))
            stroka = stroka.replace(stroka[i2:i+1], str(valbr)[1:-1], 1)
            stroka2 = find_func(stroka, indx, valbr)
            return find_brackets(stroka2)
        else:
            raise ValueError('brackets are not balanced')
    elif stroka.find('(') != -1:
        raise ValueError('brackets are not balanced')
    else:
        return stroka


def find_func(stroka, idx, val):
    st = stroka[idx-1::-1]
    i = idx
    for elem in st:
        if (elem not in A) and (elem not in ('>', '<', '=', '(')):
            i -= 1
        else:
            break
    st = stroka[i:idx]
    st1 = st.strip()
    if st1 in '':
        return stroka
    else:
        try:
            stroka = stroka.replace(st+str(val)[1:-1], str(F[st1](*val)), 1)
        except KeyError:
            raise KeyError('ERROR: unknown function', st1)
        return stroka
