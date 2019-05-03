# test 29 apr
import argparse
import math
import operator
from operator import *
import string
import importlib
import importlib.util
from math import *

ap = argparse.ArgumentParser(description='Pure-python command-line calculator.')
ap.add_argument('EXPRESSION', type=str, help='expression string to evalute')
ap.add_argument('-m', '--MODULE', type=str, help='use modules MODULE [MODULE...] additional modules to use')
args = ap.parse_args()
xpr = args.EXPRESSION
module = args.MODULE


# xprstr = ''
xprlst = []
split = ('^', '/', '*', '%', '-', '+', '=', '<', '>', '!',  '(', ')', ',')
splitset = set(split)
funclist = dir(math)+['abs', 'round', 'sum']  # list of math functions names
funcdic = math.__dict__  # dict of math functions
funcset = set(funclist)
opdic = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
        '//': floordiv,
        '%': mod,
        '^': pow,
        '==': eq,
        '<=': le,
        '>=': ge,
        '<': lt,
        '>': gt,
        '!=': ne,
        'abs': abs,
        'round': round,
        'sum': sum
        }
funcdic.update(opdic)
oper = ['^', '//', '/', '*', '%', '-', '+', '==', '<=', '>=', '<', '>', '!=', ',']
operset = set(oper)



def addfunc(module):
    """ добавляет новую функцию из модуля """
    if module is not None:  # если введено имя модуля
        try:
            spec = importlib.util.find_spec(module)
        except ImportError:
            print('ERROR: module ', module, 'not found, or unknown symbol')
            exit(0)
        if spec is None:  # проверка возможности импорта модуля
            print('ERROR: module {} not found'.format(module))
            exit(0)
        else:
            newfunc = importlib.import_module(module)  # импортирование нового модуля
            funcdic[module] = newfunc.main
            funclist.append(module)
            funcset.add(module)
    return


def parse(xprstr):
    """ парсинг строки математического выражения.
    на выходе список в инфиксной нотации"""
    word = ''
    exset = {'"', '#', '$', '&', "'", ':', ';', '?', '@', '[', ']', '_', '`', '{', '|', '}', '~', '\\'}
    xprset = set(xprstr)
    # проверка если строка выражения содержит недопустимые символы
    if not exset.isdisjoint(xprset):
        print('ERROR: unknown symbol')
        exit(0)
    # проверка скобок в строке
    if xpr.count('(') != xpr.count(')'):
        print('ERROR: brackets are not balanced')
        exit(0)
    # проверка если выражение состоит только из знаков пунктуации
    if xprset.issubset(string.punctuation) or xprset.issubset(funcset):
        print('ERROR: no digits or functions')
        exit(0)

    xprstr = xprstr.replace('  ', ' ')
    xprstr = xprstr.replace(', ', ',')
    xprstr = xprstr.replace(' *', '*')
    xprstr = xprstr.replace('* ', '*')
    xprstr = xprstr.replace(' +', '+')
    xprstr = xprstr.replace('+ ', '+')
    xprstr = xprstr.replace(' -', '-')
    xprstr = xprstr.replace('- ', '-')
    xprstr = xprstr.replace('--', '+')
    xprstr = xprstr.replace('++', '+')
    xprstr = xprstr.replace('+-', '-')
    xprstr = xprstr.replace('-+', '-')

    if xprstr[0] == '+':
        xprstr = xprstr[1:]

    # проверка лишних пробелов
    if xprstr.count(' ') > 0:
        print('ERROR: useles spaces')
        exit(0)

    # добавление скобок для возведения в степень 2^3^4
    lt = 0
    rt = len(xprstr)
    for x in range(xprstr.count('^')):
        rt = xprstr.rindex('^', 0, rt)
        # # print('rt=', rt, '   ', xprstr[:rt])
        if xprstr[:rt].count('^') == 0:
            break
        lt = xprstr.rindex('^', 0, rt)+1
        # # # print('lt=', lt, 'rt=', rt, '     ', xprstr[lt:rt])
        tmp = xprstr[lt:rt]
        # # # print('tmp=', tmp)
        tmpset = set(tmp)
        # # # print('tmpset', tmpset)
        # # # print('operset', operset)
        if (tmp[0] == '(' and tmp[-1] == ')') or (tmpset.isdisjoint(splitset)):
            # # # print('нада скобки для степени')
            xprstr = xprstr[:lt]+'('+xprstr[lt:]
            # # # print(xprstr)
            lt = rt+2
            # # # print(xprstr[l:])
            rt = len(xprstr)
            for i, data in enumerate(xprstr[lt:]):
                if data in split and data != '(':
                    rt = lt+i
                    break
            # # # print('lt=', lt, 'rt=', rt, '   ', xprstr[lt:rt])
            tmp = xprstr[lt:rt]
            # # # print(tmp)
            xprstr = xprstr[:rt]+')'+xprstr[rt:]
            # # # print(xprstr)
        else:
            # # # print('НЕ надо скобки', lt, rt)
            rt = lt

    # разбор строки
    for i, sym in enumerate(xprstr + ' '):     # добавлен дополнительный пробел
        if sym in split or i == len(xprstr):
            #  # # # print(word)
            if word == 'pi':
                xprlst.append(pi)
            elif word == 'e':
                xprlst.append(e)
            elif word in funclist:
                # # # # print(word, ' in math')
                xprlst.append(word)
            elif word.replace('.', '').isdigit() and word.count('.') < 2:
                xprlst.append(float(word))
            # elif word != '':
            elif word in split or word == '':
                pass
                #  # # # print('ok', word)
            else:
                addfunc(word)  # импортировать неизвестную функцию
                xprlst.append(word)
                # print('ERROR: wrong symbol "', word, '"')
                # exit(0)
            xprlst.append(sym)
            # print(xprlst)
            word = ''
        else:
            word = word + sym
            # print(word)
    xprlst.pop()    # удаляется добавленный пробел

    # print('поииск операторов составных')
    for i, data in enumerate(xprlst):
        if i == len(xprlst) - 1:
            break
        # print(i, data)
        if str(xprlst[i]) + str(xprlst[i+1]) in oper:
            # print(xprlst[i], xprlst[i+1])
            xprlst[i+1] = str(xprlst[i]) + str(xprlst[i+1])
            xprlst.pop(i)

        if xprlst[i] == '-' and xprlst[i-1] in oper+['('] and type(xprlst[i+1]) == float:
            # print('минус',xprlst[i-1],xprlst[i],xprlst[i+1])
            xprlst[i+1] = xprlst[i+1] * -1
            xprlst.pop(i)
            # print(*xprlst, sep='')

        if xprlst[i] == '-' and xprlst[i-1] == '(' and xprlst[i+1] in funclist:
            # print('минус',xprlst[i+1])
            xprlst[i] = -1
            xprlst.insert(i+1,'*')
            # print(*xprlst, sep='')



        # if xprlst[i] == '/' and xprlst[i + 1] == '/':
        #     xprlst[i] = '//'
        #     xprlst.pop(i + 1)
        # elif xprlst[i] == '>' and xprlst[i + 1] == '=':
        #     xprlst[i] = '>='
        #     xprlst.pop(i + 1)
        # elif xprlst[i] == '<' and xprlst[i + 1] == '=':
        #     xprlst[i] = '<='
        #     xprlst.pop(i + 1)
        # elif xprlst[i] == '=' and xprlst[i + 1] == '=' or xprlst[i] == '=':
        #     xprlst[i] = '=='
        #     xprlst.pop(i + 1)
        # elif xprlst[i] == '!' and xprlst[i + 1] == '=':
        #     xprlst[i] = '!='
        #     xprlst.pop(i + 1)

        # if xprlst[i] == '-' and xprlst[i - 1] in oper and type(xprlst[i + 1]) == float:
        #     xprlst[i + 1] = xprlst[i + 1] * - 1
        #     xprlst.pop(i)
        # elif (xprlst[i] == '-' and i == 0) or (xprlst[i] == '-' and xprlst[i - 1] in oper):
        #     xprlst[i] = -1
        #     xprlst.insert(i + 1, '*')
        # elif xprlst[i] == '-' and xprlst[i - 1] == '/':
        #     xprlst[i - 1] = '*'
        #     xprlst[i] = -1
        #     xprlst.insert(i + 1, '/')
        # elif type(xprlst[i]) == float or xprlst[i] in funclist or xprlst[i] in oper or xprlst[i] in split:
        #     pass
        #
        #     #  # # # print('ok', i)
        # else:
        #     print('ERROR: unknown', xprlst[i], i)
        # xprset = set(xprlst)
        # if xprset.issubset(funcset) or xprset.issubset(operset):
        #     print('ERROR: только функция')
        #     exit(0)
    # print (*xprlst, sep='|')
    return xprlst


def logargs(*args):
    # # # print('START logoargs', args)
    if ',' in args:
        res = log(args[-3], args[-1])
    else:
        res = log(args[-1])
    # # # print('RETURN logoargs', res)
    return res


def operate(operator, args):
    # print('OPERATOR=',operator,'ARGS=',args)

    if operator in ['sum', 'fsum']:
        # print('OPERATOR=',operator,'ARGS=',args)
        try:
            result = funcdic[operator](args)
        except ArithmeticError:
            print('ERROR: invalid argument for ', operator)
            exit(0)
    elif operator in dir(math) + dir(operator)+['module'] and operator not in ['sum', 'fsum']:
        # print('OPERATOR=',operator,'ARGS=',args, '*ARGS=',args)
        if type(args) == float or type(args) == int or type(args) == bool:
            try:
                result = funcdic[operator](args)
            except ArithmeticError:
                print('ERROR: invalid argument for ', operator)
                exit(0)
            except TypeError:
                print('ERROR: invalid argument for ', operator)
                exit(0)
            except ValueError:
                print('ERROR: invalid argument for ', operator)
                exit(0)
        else:
            try:
                result = funcdic[operator](*args)
            except ArithmeticError:
                print('ERROR: invalid argument for ', operator)
                exit(0)
            except TypeError:
                print('ERROR: invalid argument for ', operator)
                exit(0)
            except ValueError:
                print('ERROR: invalid argument for ', operator)
                exit(0)
    # else:  # уже проверяется в парсинге и попыика импортировать модуль
        # print('ERROR: unknown math operator', operator)
        # result = 0
    return result


def prior(op1, op2):
    """ сравнивает приоритеты математических опрераторов и функций op1 <= op2, возвращает bool """
    operhi = ['^'] + funclist                                           # 3
    opermid = ['*', '/', '%', '//']                                     # 2
    operlow = ['+', '-']                                                # 1
    operlowest = ['(', ')', '==', '<=', '>=', '<', '>', '!=', ',']      # 0
    priorset = [operlowest, operlow, opermid, operhi]
    for i, data in enumerate(priorset):
        if op1 in data:
            pr1 = i
        if op2 in data:
            pr2 = i
    return pr1 <= pr2


def postfix(xprlst):
    """
    преобразование инфиксной нотации в постфиксную
    на входе список элементов выражения инфиксной нотации, на выходе список элементов постфиксной нотации
    """
    # print('START CONVERT TO POSTFIX *********************')
    output = []
    stack = []
    for i in xprlst:
        # # # print('-----------------------------------')
        # # # print('i=', i)
        if type(i) == float or type(i) == int:
            output.append(i)
            # # # print('output=', *output, sep=' ')
            # # # print('stack=', *stack, sep=' ')
        if i == ',':
            if stack != []:
                while stack[-1] in oper+funclist and prior(i, stack[-1]):
                    # пока наверху стека оператор с большим или равным приоритетом
                    # # # print('пока на верху стэка оператор')
                    # # # print ( 'PRIOR', i, '<=', stack[-1], prior(i, stack[-1]))
                    output.append(stack.pop())  # переложить оператор из стека на выход
                    # # # print('output=', *output, sep=' ')
                    # # # print('stack=', *stack, sep=' ')
                    if stack == []:
                        break
            output.append(i)
            # # # print('output=', *output, sep=' ')
            # # # print('stack=', *stack, sep=' ')

        elif i in oper and i != ',':  # '^', '*', '/', '+', '-'
            # # # print('in oper', i)
            # # # print(oper)
            if stack == []:  # если стек пуст
                # # # print('стек пуст. добваить оператор в стек')
                stack.append(i)
                # # # print('output=', *output, sep=' ')
                # # # print('stack=', *stack, sep=' ')
            elif stack[-1] == '(':  # если стек содержит (
                # # # print('( положить в стек')
                stack.append(i)
                # # # print('output=', *output, sep=' ')
                # # # print('stack=', *stack, sep=' ')
            else:
                # # # print('оператор:', i, '<=stack', stack[-1], prior(i, stack[-1]))
                while stack[-1] in oper+funclist and prior(i, stack[-1]):
                        # пока наверху стека оператор с большим или равным приоритетом
                        # # # print('пока на верху стэка оператор')
                        # # # print ( 'PRIOR', i, '<=', stack[-1], prior(i, stack[-1]))
                        output.append(stack.pop())  # переложить оператор из стека на выход
                        # # # print('output=', *output, sep=' ')
                        # # # print('stack=', *stack, sep=' ')
                        if stack == []:
                            break
                stack.append(i)  # иначе положить оператор в стек

                # if i ==', ':
                #     output.append(i) # если это , то на выход
                # else:
                #     stack.append(i) # иначе положить оператор в стек
                # # # print('output=', *output, sep=' ')
                # # # print('stack=', *stack, sep=' ')

        elif i == '(':
            stack.append(i)
            # # # print('output=', *output, sep=' ')
            # # # print('stack=', *stack, sep=' ')

        elif i == ')':
            # # # print(i)
            while stack[-1] != '(':  # пока верх стека не равен (
                # # # print ('push stack', stack[-1])
                output.append(stack.pop())
                # выталкиваем элемент из стека на выход. удаляя последний элемент в стеке
            stack.pop()  # удаление из стека (
            # # # print('output=', *output, sep=' ')
            # # # print('stack=', *stack, sep=' ')
        elif i in funclist:
            # # # print(i, 'IN FUNCLIST помещаем в стек')
            stack.append(i)
            # # # print('output=', *output, sep=' ')
            # # # print('stack=', *stack, sep=' ')
    # # # print('*******')
    # # # print('output=', *output, sep=' ')
    # # # print('stack=', *stack, sep=' ')

    stack.reverse()
    return output + stack


def evalpostfix(xprpstfx):
    """
    вычисление выражения в постфиксной нотации
    на входе список элементов выражения
    """
    # print('START EVALUATE POSTFIX ********************')
    stack = []
    args = []
    for i in xprpstfx:
        # # # print('---------------')
        # # print('EVAL i = ', i, 'STACK=',stack)
        if i in funclist and i != ',':
            if len(stack) < 2:
                stack[0] = operate(i, stack[0])
            else:
                j = len(stack)-2
                args.append(stack[-1])
                while stack[j] == ',':
                    args.append(stack[j-1])
                    stack.pop()
                    stack.pop()
                    j = j - 2
                stack.pop()
                args.reverse()
                tmp = operate(i, args)
                # print('TMP=',tmp)
                args = []
                stack.append(tmp)
        elif i in oper and i != ',':
            tmp = operate(i, stack[-2:])
            stack.pop()
            stack.pop()
            stack.append(tmp)
        else:
            stack.append(i)
    return stack[0]


def main(xpr):
    # попытка добавления внешней функции если указана -m module
    addfunc(module)

    # разбор строики вырыжения в список
    xprlst = parse(xpr)
    # print(*xprlst, sep=' ')

    # преобразование инфиксного списка в постфиксных список
    xprlst = postfix(xprlst)
    # print(*xprlst, sep=' ')

    # вычисление постфиксного списка
    res = evalpostfix(xprlst)
    # print(res)
    return res


print(main(xpr))
