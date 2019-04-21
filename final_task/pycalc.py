# coding=utf-8

import argparse
import math
import string
from math import *

ap = argparse.ArgumentParser(description='Pure-python command-line calculator.')
ap.add_argument('EXPRESSION', type=str, help='expression string to evalute')
ap.add_argument('-m', '--MODULE', type=str, help='use modules MODULE [MODULE...] additional modules to use')
args = ap.parse_args()
xpr = args.EXPRESSION

funcset = {}
operset = {}
splitset = {}

split = ('^',       '/', '*', '%', '-', '+', '=',              '<', '>', '!',  '(', ')', ',')

funclist = dir(math)+['abs', 'round']      # list of math functions names
funcdict = math.__dict__          # dict of math functions
funcdict['abs'] = abs
funcdict['round'] = round
xprstr = ''
operator = ''
xprlst = []
a = 0.
b = 0.
result = 0.
funcset=set(funclist)

oper = ['^', '//', '/', '*', '%', '-', '+', '==', '<=', '>=', '<', '>', '!=']
operhi = ['^'] + funclist                   # 3
opermid = ['*', '/', '%']                        # 2
operlow = ['+', '-']                        # 1
operlowest = ['(', ')', '==', '<=', '>=', '<', '>', '!=']           # 0


# разбор строки на элементы списка
def parse(xprstr):
    word = ''

    # проверка недопустимых символов
    exset = {'"', '#', '$', '&', "'", ':', ';', '?', '@', '[', ']', '_', '`', '{', '|', '}', '~', '\\'}
    xprset = set(xprstr)
    if not exset.isdisjoint(xprset):
        print('ERROR: unknown symbol')
        exit(0)
    # проверка скобок в строке
    if xpr.count('(') != xpr.count(')'):
        print('ERROR: brackets are not balanced')
        exit(0)

    # проверка если состоит только из знаков пунктуации
    punctset = set(string.punctuation)
    xprset = set(xprstr)
    if xprset.issubset(punctset) or xprset.issubset(funcset):
        print('ERROR: no digits or functions')
        exit(0)

    xprstr = xprstr.replace(' -', '-')
    xprstr = xprstr.replace('--', '+')
    xprstr = xprstr.replace('++', '+')
    xprstr = xprstr.replace('+-', '-')
    xprstr = xprstr.replace('-+', '-')

    if xprstr[0] == '+':
        xprstr = xprstr[1:]

    # проверка пробелов
    if xpr.count(' ') > 0:
        print('ERROR: useles spaces')
        exit(0)

    # разбор строки
    for i, sym in enumerate(xprstr + ' '):     # добавлен дополнительный пробел
        if sym in split or i == len(xprstr):
            #  # print(word)
            if word == 'pi':
                xprlst.append(pi)
            elif word == 'e':
                xprlst.append(e)
            elif word in funclist:
                # # print(word, ' in math')
                xprlst.append(word)
            elif word.replace('.', '').isdigit() and word.count('.') < 2:
                xprlst.append(float(word))
            # elif word != '':
            elif word in split or word == '':
                pass
                #  # print('ok', word)
            else:
                print('ERROR: wrong symbol "', word, '"')
                exit(0)
            xprlst.append(sym)
            #  # print(xprlst)
            word = ''
        else:
            word = word + sym
            #  # print(word)
    xprlst.pop()    # удаляется добавленный пробел



    for i, data in enumerate(xprlst):
        if xprlst[i] == '/' and xprlst[i + 1] == '/':
            xprlst[i] = '//'
            xprlst.pop(i + 1)
        elif xprlst[i] == '>' and xprlst[i + 1] == '=':
            xprlst[i] = '>='
            xprlst.pop(i + 1)
        elif xprlst[i] == '<' and xprlst[i + 1] == '=':
            xprlst[i] = '<='
            xprlst.pop(i + 1)
        elif xprlst[i] == '=' and xprlst[i + 1] == '=' or xprlst[i] == '=':
            xprlst[i] = '=='
            xprlst.pop(i + 1)
        elif xprlst[i] == '!' and xprlst[i + 1] == '=':
            xprlst[i] = '!='
            xprlst.pop(i + 1)
        elif xprlst[i] == '-' and xprlst[i - 1] in ('^', '//', '/', '*', '%', '-', '+', '==', '<=', '>=', '<', '>', '!=', '=') and type(xprlst[i + 1]) == float:
            xprlst[i + 1] = xprlst[i + 1] * - 1
            xprlst.pop(i)
        elif (xprlst[i] == '-' and i == 0) or(xprlst[i] == '-' and xprlst[i - 1] in('*', '^', '+', '-', '(', '<', '>', '=')):
            xprlst[i] = -1
            xprlst.insert(i + 1, '*')
        elif xprlst[i] == '-' and xprlst[i - 1] == '/':
            xprlst[i - 1] = '*'
            xprlst[i] = -1
            xprlst.insert(i + 1, '/')
        elif type(xprlst[i]) == float or xprlst[i] in funclist or xprlst[i] in oper or xprlst[i] in split:
            pass

            #  # print('ok', i)
        else:
            print('ERROR: unknown', xprlst[i], i)


        xprset = set(xprlst)
        if xprset.issubset(funcset) or xprset.issubset(operset):
            print('ERROR: только функция')
            exit(0)




  #  # print(xprlst)

    return xprlst


def logargs(*args):
    if len(args) == 1:
        res = log(args[0])
    else:
        res = log(args[0],args[2])
    return res


def operate(operator, *args):

    for i in args:
        if not (type(i) == float or type(i) == int):
            print('ERROR: operate non digits')
            exit(0)

    if operator in dir(math) and not operator in ['pow', 'log']:
        result = funcdict[operator](args[-1])
    elif operator == "pow":
        result = pow(args[-3], args[-1])
    elif operator == "log":
        result = logargs(*args)
    elif operator == "+":
        result = args[-2] + args[-1]
    elif operator == "-":
        result = args[-2] - args[-1]
    elif operator == "*":
        result = args[-2] * args[-1]
    elif operator == "//":
        if args[-1] != 0:
            result = args[-2] // args[-1]
        else:
            print('ERROR: division by zero')
            exit(0)
    elif operator == "/":
        if args[-1] != 0:
            result = args[-2] / args[-1]
        else:
            print('ERROR: division by zero')
            exit(0)
    elif operator == "%":
        result = args[-2] % args[-1]
    elif operator == "^":
        result = args[-2] ** args[-1]
    elif operator == "<=":
        result = args[-2] <= args[-1]
    elif operator == ">=":
        result = args[-2] >= args[-1]
    elif operator == "<":
        result = args[-2] < args[-1]
    elif operator == ">":
        result = args[-2] > args[-1]
    elif operator == "==":
        result = args[-2] == args[-1]
    elif operator == "!=":
        result = args[-2] != args[-1]
    else:
        print('ERROR: unknown math operator', operator)
        result = 0
    return result


def prior(op1, op2):
    priorset = [operlowest, operlow, opermid, operhi]
    for i, data in enumerate(priorset):
        # # print(op1, i,data,)
        if op1 in data:
            prior1 = i
        if op2 in data:
            prior2 = i
    # # print(prior1 <= prior2)
    return prior1 <= prior2





# основная функция
def main(xpr):


    # разбор строики в список
    xprlst = parse(xpr)
    # print(*xprlst, sep=' ')

    output=[]
    stack=[]
    for i in xprlst:
        # print('-----------------------------------')
        # print('i=',i)

        if type(i) == float or type(i) == int or i == ',':
            output.append(i)
            # print('output=',*output,sep=' ')
            # print('stack=',*stack,sep=' ')

        elif i in oper: # '^', '*', '/', '+', '-'

            # print('in oper',i)
            # print(oper)
            if stack == []: # если стек пуст
                # print('стек пуст. добваить оператор в стек')
                stack.append(i)
                # print('output=',*output,sep=' ')
                # print('stack=',*stack,sep=' ')
            elif stack[-1] == '(': # если стек содержит (
                # print('( положить в стек')
                stack.append(i)
                # print('output=',*output,sep=' ')
                # print('stack=',*stack,sep=' ')
            else:
                # print('оператор:',i, '<=stack', stack[-1], prior(i, stack[-1]))
                while stack[-1] in oper+funclist and prior(i, stack[-1]): # пока наверху стека оператор с большим или равным приоритетом
                        # print('пока на верху стэка оператор')
                        # print ( 'PRIOR',i, '<=', stack[-1], prior(i, stack[-1]))
                        output.append(stack.pop()) # переложить оператор из стека на выход
                        # print('output=',*output,sep=' ')
                        # print('stack=',*stack,sep=' ')
                        if stack == []: break
                stack.append(i) # иначе положить оператор в стек
                # print('output=',*output,sep=' ')
                # print('stack=',*stack,sep=' ')


        elif i == '(':
            stack.append(i)
            # print('output=',*output,sep=' ')
            # print('stack=',*stack,sep=' ')

        elif i == ')':
            # print(i)
            while stack[-1] != '(': # пока верх стека не равен (
                # print ('push stack', stack[-1])
                output.append(stack.pop())  # выталкиваем элемент из стека на выход. удаляя последний элемент в стеке
            stack.pop() # удаление из стека (
            # print('output=',*output,sep=' ')
            # print('stack=',*stack,sep=' ')
        elif i in funclist:
            # print(i,'IN FUNCLIST помещаем в стек')
            stack.append(i)
            # print('output=',*output,sep=' ')
            # print('stack=',*stack,sep=' ')
    # print('*******')
    # print('output=',*output,sep=' ')
    # print('stack=',*stack,sep=' ')

    stack.reverse()
    pol = output + stack # poland
    # print('POLAND:',pol)


    # print('START CALCULATE *****************')

    output = []
    stack = []

    for i in pol:
        # print('---------------')
        # print('i in pol = ',i)

        if i in oper+['pow','log']:

            if len(stack) < 2:
                print('ERROR: no argument')
                exit(0)

            tmp = operate(i, *stack)
            if ',' in stack:
                stack.pop()
                stack.pop()
                stack[0] = tmp
            else:
                stack.pop()
                stack[-1] = tmp
            # print('stack=',stack)
        elif i in funclist and not i in ['pow','log']:
            tmp = operate(i, *stack)
            stack[-1] = tmp
            # print('stack=',stack)
        # elif i in ['pow','log']:
        #     # print('DOBL')
        #     tmp = operate(i, *stack)
        #     stack.pop()
        #     stack.pop()
        #     stack[-1] = tmp
        #     # print('stack=',stack)


        else:
            stack.append(i)
            # print('stack=',stack)

    return stack[0]

print(main(xpr))
