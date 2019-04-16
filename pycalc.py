#16.04.2019 12:00
# to master
import argparse
from math import pi,e,cos,sin,acos,asin,tan,atan,log,log10,sqrt,exp,factorial

ap = argparse.ArgumentParser(description = 'Pure-python command-line calculator.')
ap.add_argument('EXPRESSION', type=str, help='expression string to evalute')
ap.add_argument('-p', '--PRINT', default='n', choices=['y', 'n'], type = str, help = 'print evaluation process')
ap.add_argument('-m', '--MODULE', type = str, help = 'use modules MODULE [MODULE...] additional modules to use')
args = ap.parse_args()
##print(args.EXPRESSION)
##print(args.PRINT)
##print(args.MODULE)
xpr = args.EXPRESSION
show = args.PRINT
#show = 'y'

##xpr = modstr=args.MODULE
##xpr = 
##xpr = mod = __import__(modstr)
##xpr = print (modstr,'=',mod.myfunc(3))


##  Unary operators
##xpr = "-13"
##xpr = "6-(-13)"
##xpr = "1---1"
##xpr = "-+---+-1"
##  Operation priority
##xpr = "1+2*2"
##xpr = "1+(2+3*2)*3"
##xpr = "10*(2+1)"
##xpr = "10^(2+1)"
##xpr = "100/3^2"
##xpr = "100/3%2^2"
##  Functions and constants
##xpr = "pi+e"
##xpr = "log(e)"
##xpr = "sin(pi/2)"
##xpr = "log10(100)"
##xpr = "sin(pi/2)*111*6"
##xpr = "2*sin(pi/2)"
##xpr = "abs(-5)"
##xpr = "round(123.456789)"
##xpr = Associative
##xpr = "102%12%7"
##xpr = "100/4/3"
##xpr = "2^3^4"
##  Comparison operators
##xpr = "1+2*3==1+2*3"
##xpr = "e^5>=e^5+1"
##xpr = "1+2*4/3+1!=1+2*4/3+2"
##  Common tests
##xpr = "(100)"
##xpr = "666"
##xpr = "-.1"
##xpr = "1/3"
##xpr = "1.0/3.0"
##xpr = ".1 * 2.0^56.0"
##xpr = "e^34"
##xpr = "(2.0^(pi/pi+e/e+2.0^0.0))"
##xpr = "(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"
##xpr = "sin(pi/2^1) + log(1*4+2^2+1, 3^2)"
##xpr = "10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"
##xpr = "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)"
##xpr = "2.0^(2.0^2.0*2.0^2.0)"
## ошибка ? "sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))"
##xpr = "sin(e^log(e^e^sin(23.0)*45.0) + cos(3.0+log10(e^-e)))"
##xpr = Error cases
##xpr = ""
##xpr = "+"
##xpr = "1-"
##xpr = "1 2"
##xpr = "ee"
##xpr = "==7"
##xpr = "1 + 2(3 * 4))"
##xpr = "((1+2)"
##xpr = "1 + 1 2 3 4 5 6 "
##xpr = "log100(100)"
##xpr = "------"
##xpr = "5 > = 6"
##xpr = "5 / / 6"
##xpr = "6 < = 6"
##xpr = "6 * * 6"
##xpr = "((((("
##xpr = “pow(2, 3, 4)”

## EVAL TEST
##test=xpr
##test=test.replace('^','**')
##test=test.replace(' ','')
##test=test.replace(',','.')
##print ('EVAL:',test,'=',eval(test))
##print(xpr)

oper = ('!','^','//','/','*','%','-','+','(',')','==','<=','>=','<','>','!=','=')
digit = ('1','2','3','4','5','6','7','8','9','0','.')
func = ('sin','cos','tan','log10','log','exp','abs','round','sqrt')
stroka = ''
slovo = ''
operator = ''
spisok = []
a = 0.
b = 0.
result = 0.


#разбор строки на элементы списка
def parse(stroka):
    slovo=''
    #исправление неверно введенных знаков
    stroka = stroka.replace(' ','')
    stroka = stroka.replace(',','.')
    stroka = stroka.replace('--','+')
    stroka = stroka.replace('++','+')
    stroka = stroka.replace('+-','-')
    stroka = stroka.replace('-+','-')
    stroka = stroka.replace('<+','<')
    stroka = stroka.replace('>+','>')
    stroka = stroka.replace('=<','<=')
    stroka = stroka.replace('=>','>=')
    stroka = stroka.replace('==+','+')
    if stroka[0] == '+': stroka=stroka[1:]
    #print('parse:',stroka)

    #разбор строки
    for i,sym in enumerate(stroka + ' '):     #добавлен дополнительный пробел
        if sym in oper or i == len(stroka):
            #print(i,slovo,sym)
            if slovo == 'pi':
                spisok.append(pi)
            elif slovo == 'e':
                spisok.append(e)
            elif slovo in func:
                spisok.append(slovo)
            elif slovo.replace('.','').isdigit() and slovo.count('.')<2:
                spisok.append(float(slovo))
            elif slovo != '':
                print('ERROR: wrong symbol "',slovo,sym,'"')
                exit(0)
            spisok.append(sym)
            slovo = ''
            #print(sym)
            
        else:
            slovo = slovo + sym
        #print(i,sym,spisok)
    spisok.pop()    #удаляется добавленный пробел      
    
    for i,data in enumerate(spisok):
        if spisok[i] == '/' and spisok[i + 1] == '/':
            spisok[i] = '//'
            spisok.pop(i + 1)
        if spisok[i] == '>' and spisok[i + 1] == '=':
            spisok[i] = '>='
            spisok.pop(i + 1)
        if spisok[i] == '<' and spisok[i + 1] == '=':
            spisok[i] = '<='
            spisok.pop(i + 1)
        if spisok[i] == '=' and spisok[i + 1] == '=' or spisok[i] =='=':
            spisok[i] = '=='
            spisok.pop(i + 1)
        if spisok[i] == '!' and spisok[i + 1] == '=':
            spisok[i] = '!='
            spisok.pop(i + 1)
        if spisok[i] == '-' and spisok[i - 1] in ('^','//','/','*','%','-','+','==','<=','>=','<','>','!=','=') and type(spisok[i + 1]) == float:
            spisok[i + 1] = spisok[i + 1]* - 1
            spisok.pop(i)
        if (spisok[i] == '-' and i == 0) or(spisok[i] == '-' and spisok[i - 1] in('*','^','+','-','(','<','>','=') ):
            spisok[i] = -1
            spisok.insert(i + 1,'*')
        if spisok[i] == '-' and spisok[i - 1] == '/':
            spisok[i - 1] = '*'
            spisok[i] = -1
            spisok.insert(i + 1,'/')
    #print(spisok)        
    return(spisok)


def operate(operator,a,b):
    if operator == "+":
       result = a + b
    elif operator == "-":
       result = a - b
    elif operator == "*":
       result = a * b

    elif operator == "//":
        if b != 0:
            result = a // b
        else:
            print('ERROR: division by zero')
            exit(0)
    elif operator == "/":
        if b != 0:
            result = a / b
        else:
            print('ERROR: division by zero')
            exit(0)
    elif operator == "%":
       result = a % b
    elif operator == "^":
       result = a**b
    elif operator == "<=":
        result = a <= b
    elif operator == ">=":
        result = a >= b
    elif operator == "<":
        result = a < b
    elif operator == ">":
        result = a > b
    elif operator == "==":
        result = a == b
    elif operator == "!=":
        result = a != b
    elif operator == "abs":
        result = abs(a)
    elif operator == "round":
        result = round(a)
    elif operator == "cos":
        result = cos(a)
    elif operator == "sin":
        result = sin(a)
    elif operator == "tan":
        result = tan(a)
    elif operator == "log":
        result = log(a)
    elif operator == "log10":
        result = log10(a)
    elif operator == "sqrt":
        result = sqrt(a)
    elif operator == "cos":
        result = cos(a)
    elif operator == "exp":
        result = exp(a)
    elif operator == "!":
        result = factorial(a)
    else:
        print('ERROR: unknown math operator',operator)
        result = 0
    if show == 'y':
        if operator in oper:
            print('Operate:',a,operator,b,'=',result)
        elif operator in func:
            print('Operate:',operator,a,'=',result)
    return result

#вычисление выражения без скобок
def calculate(spisok):
    if show == 'y': print('Calculate:',spisok)
    # перебор списка функций 
    for f in func:
        for i in range(spisok.count(f)):
           #print(f,spisok.count(f))
            s = spisok.index(f)
            spisok[s] = (operate(f,spisok[s + 1],0))
            spisok[s + 1] = ''
            wipe(spisok)
            #print(*spisok,sep='')
            
    #вычисление возведение в степень с реверсом списка
    #print('^ count:',spisok.count('^'))
    if '^' in spisok:
        spisok.reverse()
        #print('reverse: ',spisok)
        while '^' in spisok:
            i = spisok.index('^')
            #print('i = ',i)
            spisok[i] = spisok[i + 1]**spisok[i - 1]
            #print(spisok[i + 1],'^',spisok[i - 1],'=',spisok[i])
            spisok[i - 1] = ''
            spisok[i + 1] = ''
            #print(spisok)
            wipe(spisok)
            #print(spisok)
        spisok.reverse()
        
    #перебор списка математических операций
    for j in oper:
        #print('operation = ',j)
        #print(spisok)
        i = 1
        while i < len(spisok):
            if spisok[i] == j:
                #print('calculate: ',*spisok,sep='')
                spisok[i] = operate(spisok[i],spisok[i - 1],spisok[i + 1])
                spisok[i - 1] = ''
                spisok[i + 1] = ''
                #print(spisok)
                wipe(spisok)
                i = i - 1
            i = i + 1
    #print('Stop calculate:',float(spisok[0]))
    wipe(spisok)
    #print(spisok)
    result = spisok[0]
    if len(spisok) > 1:
        print('ERROR: missed operator')
        #exit(0)
    return(result)

#очистка списка от пустых значений ''
def wipe(spisok):
    #print('WIPE:\n',spisok)
    while '' in spisok:
        i = spisok.index('')
        spisok.pop(i)
    #print('WIPED:\n',spisok)
    return(spisok)

#поиск начала и конца выражения в скобках()
def brktindx(spisok):
    bl = spisok.index('(')
    br = spisok.index(')')
    s = spisok[bl + 1:br]
    #print('BL BR ',bl + 1,' ',br,' ',*s,sep='')
    while '(' in s:
        if s.count('(') == s.count(')'):
            bl = spisok.index('(',bl + 1)
            br = spisok.index(')',bl + 1)
            s = spisok[bl + 1:br]
            #print('BL BR ',bl + 1,' ',br,' ', *s,sep='')
        else:
            br = spisok.index(')',br + 1)
            s = spisok[bl:br + 1]
    return(bl + 1,br)


# основная функция
def calc(xpr):
    #проверка скобок в строке
    if xpr.count('(') != xpr.count(')'):
        print('ERROR: brackets are not balanced')
        exit(0)

    #разбор строики в список
    spisok = parse(xpr)
    #print(*spisok,sep=',')





    #поиск скобок и вычисление в скобках
    while '(' in spisok:
        a,b = brktindx(spisok)
        #print('in brackets: ',*spisok[a:b],sep='')
        spisok[a - 1] = calculate(spisok[a:b])
        while a < b + 1:
            spisok[a] = ''
            a = a + 1
        wipe(spisok)
        #print(*spisok,sep='')

    #вычисление без скобок
    result = calculate(spisok)
    #print(result)
    return (result)

print (calc(xpr))


