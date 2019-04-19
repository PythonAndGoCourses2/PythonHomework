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

split = ('^', '//', '/', '*', '%', '-', '+', '(', ')', '==', '<=', '>=', '<', '>', '!=', '=', ',','!')
oper = ('!', '^', '//', '/', '*', '%', '-', '+', '(', ')', '==', '<=', '>=', '<', '>', '!=', '=')

funclist = dir(math)+['abs', 'round']      # list of math functions names
funcdict = math.__dict__          # dict of math functions
funcdict['abs'] = abs
funcdict['round'] = round


# print(func)
xprstr = ''
# word = ''
operator = ''
xprlst = []
a = 0.
b = 0.
result = 0.


# разбор строки на элементы списка
def parse(xprstr):
    word = ''
    # исправление неверно введенных знаков

    xprstr = xprstr.replace(' ', '')
    xprstr = xprstr.replace('--', '+')
    xprstr = xprstr.replace('++', '+')
    xprstr = xprstr.replace('+-', '-')
    xprstr = xprstr.replace('-+', '-')
    xprstr = xprstr.replace('<+', '<')
    xprstr = xprstr.replace('>+', '>')
    xprstr = xprstr.replace('=<', '<=')
    xprstr = xprstr.replace('=>', '>=')
    xprstr = xprstr.replace('==+', '+')
    if xprstr[0] == '+':
        xprstr = xprstr[1:]
    # print('parse:', xprstr)

    # разбор строки
    for i, sym in enumerate(xprstr + ' '):     # добавлен дополнительный пробел
        if sym in split or i == len(xprstr):
            if word == 'pi':
                xprlst.append(pi)
            elif word == 'e':
                xprlst.append(e)
            elif word in funclist:
                # print(word, ' in math')
                xprlst.append(word)
            elif word.replace('.', '').isdigit() and word.count('.') < 2:
                xprlst.append(float(word))
            # elif word != '':
            # else:
            #    print('ERROR: wrong symbol "', word, sym, '"')
            #    exit(0)
            xprlst.append(sym)
            word = ''
        else:
            word = word + sym
         #   print(word)

    xprlst.pop()    # удаляется добавленный пробел

  #  print(xprlst)
    punctset = set(string.punctuation)
    xprset = set(xprstr)
    if xprset.issubset(punctset):
        print('ERROR: no digits or functions')
        exit(0)




    for i, data in enumerate(xprlst):
        if xprlst[i] == '/' and xprlst[i + 1] == '/':
            xprlst[i] = '//'
            xprlst.pop(i + 1)
        if xprlst[i] == '>' and xprlst[i + 1] == '=':
            xprlst[i] = '>='
            xprlst.pop(i + 1)
        if xprlst[i] == '<' and xprlst[i + 1] == '=':
            xprlst[i] = '<='
            xprlst.pop(i + 1)
        if xprlst[i] == '=' and xprlst[i + 1] == '=' or xprlst[i] == '=':
            xprlst[i] = '=='
            xprlst.pop(i + 1)
        if xprlst[i] == '!' and xprlst[i + 1] == '=':
            xprlst[i] = '!='
            xprlst.pop(i + 1)
        if xprlst[i] == '-' and xprlst[i - 1] in ('^', '//', '/', '*', '%', '-', '+', '==', '<=', '>=', '<', '>', '!=', '=') and type(xprlst[i + 1]) == float:
            xprlst[i + 1] = xprlst[i + 1] * - 1
            xprlst.pop(i)
        if (xprlst[i] == '-' and i == 0) or(xprlst[i] == '-' and xprlst[i - 1] in('*', '^', '+', '-', '(', '<', '>', '=')):
            xprlst[i] = -1
            xprlst.insert(i + 1, '*')
        if xprlst[i] == '-' and xprlst[i - 1] == '/':
            xprlst[i - 1] = '*'
            xprlst[i] = -1
            xprlst.insert(i + 1, '/')
#    print(xprlst)



#    ss=set(xprstr)
#    digitsset = set(string.digits)
#    funcset = set(funclist)
#    digitsset.union(funcset)

#    print(digitsset.union(funcset))
 #   print(ss)
  #  print('!!!!!!!!!!!!!!!!!!', ss.isdisjoint(digitsset))


    return xprlst


def operate(operator, *args):

    #print('def operate', operator, args)
    if operator in dir(math):
        result = funcdict[operator](*args)
    elif operator == "+":
        result =  args[0] +  args[1]
    elif operator == "-":
        result =  args[0] -  args[1]
    elif operator == "*":
        result =  args[0] *  args[1]
    elif operator == "//":
        if args[1] != 0:
            result =  args[0] //  args[1]
        else:
            print('ERROR: division by zero')
            exit(0)
    elif operator == "/":
        if args[1] != 0:
            result =  args[0] /  args[1]
        else:
            print('ERROR: division by zero')
            exit(0)
    elif operator == "%":
        result =  args[0] %  args[1]
    elif operator == "^":
        result = a**b
    elif operator == "<=":
        result =  args[0] <=  args[1]
    elif operator == ">=":
        result =  args[0] >=  args[1]
    elif operator == "<":
        result =  args[0] <  args[1]
    elif operator == ">":
        result =  args[0] >  args[1]
    elif operator == "==":
        result =  args[0] ==  args[1]
    elif operator == "!=":
        result =  args[0] !=  args[1]
    else:
        print('ERROR: unknown math operator', operator)
        result = 0


#    if operator in oper:
#        print('Operate:', a, operator, b, '=', result)
#    elif operator in funclist:
#        print('Operate:', operator, a, '=', result)


    return result


# вычисление выражения без скобок
def calculate(xprlst):
 #   print('Calculate:', xprlst)
    # перебор списка функций
    for f in funclist:
        for i in range(xprlst.count(f)):
            #print(f,'in funclist')
            # print(f, xprlst.count(f))
            s = xprlst.index(f)
            if ',' in xprlst:
                #print (f,xprlst[s + 1], xprlst[s + 3])
                xprlst[s] = (operate(f, xprlst[s + 1], xprlst[s + 3]))
                xprlst[s + 1] = ''
                xprlst[s + 2] = ''
                xprlst[s + 3] = ''
            else:
                #print('norm')
                #print (f,xprlst[s + 1])
                xprlst[s] = (operate(f, xprlst[s + 1]))
                xprlst[s + 1] = ''
            wipe(xprlst)


    # вычисление возведение в степень с реверсом списка
    # print('^ count:', xprlst.count('^'))
    if '^' in xprlst:
        xprlst.reverse()
        # print('reverse: ', xprlst)
        while '^' in xprlst:
            i = xprlst.index('^')
            # print('i=', i)
            xprlst[i] = xprlst[i + 1]**xprlst[i - 1]
            # print(xprlst[i + 1], '^', xprlst[i - 1], '=', xprlst[i])
            xprlst[i - 1] = ''
            xprlst[i + 1] = ''
            # print(xprlst)
            wipe(xprlst)
            # print(xprlst)
        xprlst.reverse()

    # перебор списка математических операций
    for j in oper:
      #   print('operation=', j)
        # print(xprlst)
        i = 1
        while i < len(xprlst):
            if xprlst[i] == j:
                #print(xprlst[i-1], j, xprlst[i+1])
                xprlst[i] = operate(xprlst[i], xprlst[i - 1], xprlst[i + 1])
                xprlst[i - 1] = ''
                xprlst[i + 1] = ''
               # print(xprlst)
                wipe(xprlst)
                i = i - 1
            i = i + 1
    # print('Stop calculate:', float(xprlst[0]))
    wipe(xprlst)
    #print(xprlst)

 #   if len(xprlst) > 1:
  #      print('ERROR: missed operator')
   #     #exit(0)
    return xprlst


# очистка списка от пустых значений ''
def wipe(xprlst):
    # print('WIPE:\n', xprlst)
    while '' in xprlst:
        i = xprlst.index('')
        xprlst.pop(i)
    # print('WIPED:\n', xprlst)
    return xprlst


# поиск начала и конца выражения в скобках()
def brktindx(xprlst):
    bl = xprlst.index('(')
    br = xprlst.index(')')
    s = xprlst[bl + 1:br]
    # print('BL BR ', bl + 1, ' ', br, ' ', *s, sep='')
    while '(' in s:
        if s.count('(') == s.count(')'):
            bl = xprlst.index('(', bl + 1)
            br = xprlst.index(')', bl + 1)
            s = xprlst[bl + 1:br]
            # print('BL BR ', bl + 1, ' ', br, ' ', *s, sep='')
        else:
            br = xprlst.index(')', br + 1)
            s = xprlst[bl:br + 1]
    return(bl + 1, br)






# основная функция
def main(xpr):
    # проверка скобок в строке
    if xpr.count('(') != xpr.count(')'):
        print('ERROR: brackets are not balanced')
        exit(0)

    # разбор строики в список
    xprlst = parse(xpr)
    # print(*xprlst, sep=', ')

    # поиск скобок и вычисление в скобках
    while '(' in xprlst:
        a, b = brktindx(xprlst)
        inbrackets = xprlst[a:b]
        #print('in brackets to oper: ', inbrackets)
        tmp = calculate(xprlst[a:b])
        #print (tmp)
        xprlst = xprlst[0:a-1] + tmp + xprlst[b+1:]

        #print(xprlst)


    # вычисление без скобок
    result = calculate(xprlst)
    # print(result)
    return (result[0])


print(main(xpr))
