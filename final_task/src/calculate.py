import re
import math
from collections import namedtuple
from collections.abc import Iterable
import inspect
import functools
from src.config import standartFunctions, priorities, regexSpecialSymbols
from src.stack import Stack


funcWithPriority = namedtuple('Func', ['func', 'priority'])


def executeOnce(func):
    result = []

    def wrapper(*args, **kwargs):
        nonlocal result
        if not result:
            result.append(func(*args, **kwargs))
        return result[0]
    return wrapper


@executeOnce
def getMathFuncDict(functions=None):
    mathFunctions = {attr: getattr(math, attr) for attr in dir(math) if callable(
        getattr(math, attr))}
    externalFunctions = {attr: getattr(functions, attr) for attr in dir(functions) if callable(
        getattr(functions, attr))}
    return {**mathFunctions, **externalFunctions, 'abs': abs, 'round': round}


@executeOnce
def getStandartFuncDict():
    return {funcKey: funcWithPriority(func, priority) for (funcKey, func), (priorityKey, priority) in zip(standartFunctions.items(), priorities.items())}


@executeOnce
def getConstDict(functions=None):
    mathConsts = {attr: getattr(math, attr) for attr in dir(
        math) if type(getattr(math, attr)) in (int, float, complex)}
    externalConsts = {attr: getattr(functions, attr) for attr in dir(
        functions) if type(getattr(functions, attr)) in (int, float, complex)}
    return {**mathConsts, **externalConsts}


@executeOnce
def getNumRegex():
    return re.compile('\d+[.]?\d*|[.]\d+')

#TODO wrong interpreting of >=, because of > matched first
@executeOnce
def getStandartFuncRegex():
    keys = list(getStandartFuncDict().keys())
    keys.sort(reverse = True)
    standartFuncStr = str('|').join(keys)
    for symbol in regexSpecialSymbols:
        standartFuncStr = standartFuncStr.replace(symbol, "\\"+symbol)
    return re.compile(standartFuncStr)


@executeOnce
def getConstsRegex(functions=None):
    return re.compile(str('|').join(getConstDict(functions).keys()))


def findClosingBracket(expression):
    brackets = Stack()
    for pos, symbol in enumerate(expression):
        if symbol == '(':
            brackets.push('(')
        elif symbol == ')':
            if brackets.isEmpty():
                raise Exception("Brackets are not balanced!")
            brackets.pop()
        if brackets.isEmpty():
            return pos
    if not brackets.isEmpty():
        raise Exception("Brackets are not balanced!")



def parseExpression(expression, functions=None):
    numRegex = getNumRegex()
    standartFuncRegex = getStandartFuncRegex()
    funcDict = getMathFuncDict(functions)
    constsDict = getConstDict(functions)
    standartFuncDict = getStandartFuncDict()
    strRegex = re.compile('[A-Z]|[a-z]+[0-9]*')
    operators = Stack()
    prevPushed = None
    ppnExp = []
    searchPos = 0
    while searchPos < len(expression):
        while searchPos<len(expression)-1 and expression[searchPos]==' ':
            searchPos+=1
        match = numRegex.match(expression, searchPos)
        if expression[searchPos] == '(':
            operators.push(funcWithPriority('(', -1))
            prevPushed = '('
            searchPos += 1
        elif expression[searchPos] == ')':
            lastItem = operators.pop()
            while lastItem.func != '(' and not operators.isEmpty():
                ppnExp.append(lastItem.func)
                lastItem = operators.pop()
            if lastItem.func != '(':
                raise Exception("Brackets are not balanced!")
            searchPos+=1
        elif match:
            prevPushed = float(match.string[match.start():match.end()])
            ppnExp.append(prevPushed)
            searchPos = match.end()
        else:
            match = standartFuncRegex.match(expression, searchPos)
            if match:
                matchStr = match.string[match.start(): match.end()]
                if matchStr in ('-', '+') and (isinstance(prevPushed, Iterable) or prevPushed == '(' or prevPushed == None):
                    if matchStr == '-':
                        operators.push(standartFuncDict['unary-'])
                        prevPushed = standartFuncDict['unary-']
                    else:
                        operators.push(standartFuncDict['unary+'])
                        prevPushed = standartFuncDict['unary+']
                elif operators.isEmpty() or (standartFuncDict[matchStr].priority > operators.lastItem().priority):
                    prevPushed = standartFuncDict[matchStr]
                    operators.push(prevPushed)
                elif matchStr == '^' and operators.lastItem() == standartFuncDict[matchStr]:
                    prevPushed = standartFuncDict[matchStr]
                    operators.push(prevPushed)
                else:
                    while not operators.isEmpty() and standartFuncDict[matchStr].priority <= operators.lastItem().priority:
                        ppnExp.append(operators.pop().func)
                    prevPushed = standartFuncDict[matchStr]
                    operators.push(prevPushed)
                searchPos = match.end()
            else:
                match = strRegex.match(expression, searchPos)
                if match:
                    matchStr = match.string[match.start(): match.end()]
                    if matchStr in funcDict.keys():
                        #TODO parse ,
                        mathFuncEnd = match.end() + \
                            findClosingBracket(expression[match.end():])
                        innerExpression = expression[match.end(
                        )+1:mathFuncEnd]
                        paramStrs = [innerExpression]
                        if re.match('[^(]+[,][^)]+', innerExpression):
                            paramStrs = innerExpression.split(',')
                        parameters = []
                        for exprs in paramStrs:
                            parameters.append(calculate(exprs))
                        prevPushed = funcDict[matchStr](*parameters)
                        ppnExp.append(prevPushed)
                        searchPos = mathFuncEnd+1
                    elif matchStr in constsDict.keys():
                        prevPushed = constsDict[matchStr]
                        ppnExp.append(prevPushed)
                        searchPos = match.end()
                    else:
                        raise Exception(
                            "Unknown expression at "+str(match.start()))
                else:
                    raise Exception("Unknown symbol at " + str(searchPos))

    while not operators.isEmpty():
        ppnExp.append(operators.pop().func)
    return ppnExp


def calculate(expression, functions=None):
    ppnExpression = parseExpression(expression, functions)
    calcStack = Stack()
    for item in ppnExpression:
        if callable(item):
            args = []
            for arg in inspect.getargspec(item).args:
                args.append(calcStack.pop())
            args.reverse()
            calcStack.push(item(*args))
        elif type(item) in (int, float, complex):
            calcStack.push(item)
        else:
            raise Exception("Brackets are not balanced")
    answer = calcStack.pop()
    if not calcStack.isEmpty():
        raise Exception("No operators between expressions!")
    return answer
try:
   print(calculate(r'((((( '))
except Exception as err:
   print("ERROR: {0}".format(err))