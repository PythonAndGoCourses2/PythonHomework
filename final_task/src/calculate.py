import re
import math
import inspect
from collections import namedtuple
from collections.abc import Iterable
from src.config import STANDART_FUNCTIONS, PRIORITIES, REGEX_SPEC_SYMBOLS
from src.stack import Stack


FuncWithPriority = namedtuple('Func', ['func', 'priority'])


def executeOnce(func):
    """Decorate to execute function only once."""
    result = []

    def wrapper(*args, **kwargs):
        nonlocal result
        if not result:
            result.append(func(*args, **kwargs))
        return result[0]
    return wrapper


@executeOnce
def getMathFuncDict(functions=None):
    """Create mathematical functions dictionary.

    Parameters
    ----------
    functions : module
         User-specified module containing functions (default is None)

    Returns
    -------
    dict
        dictionary with keys of name of functions and values of functions.
    
    """
    mathFunctions = {attr: getattr(math, attr) for attr in dir(math) if callable(
        getattr(math, attr))}
    externalFunctions = {attr: getattr(functions, attr) for attr in dir(functions) if callable(
        getattr(functions, attr))}
    return {**mathFunctions, **externalFunctions, 'abs': abs, 'round': round}


@executeOnce
def getStandartFuncDict():
    """Create dictionary of standart mathematical operators.

    Returns
    -------
    dict
        dictionary with keys of operators names and values of FuncWithPriority

    """
    return {funcKey: FuncWithPriority(func, priority) for (funcKey, func), (priorityKey, priority) in zip(STANDART_FUNCTIONS.items(), PRIORITIES.items())}


@executeOnce
def getConstDict(functions=None):
    """Create dictionary of constants.

    Parameters
    ----------
    functions : module
        User-specified module containing constants (default is None)

    Returns
    -------
    dict
        Dictionary with keys of constant names and values of their values
    
    """
    mathConsts = {attr: getattr(math, attr) for attr in dir(
        math) if type(getattr(math, attr)) in (int, float, complex)}
    externalConsts = {attr: getattr(functions, attr) for attr in dir(
        functions) if type(getattr(functions, attr)) in (int, float, complex)}
    return {**mathConsts, **externalConsts}


@executeOnce
def getNumRegex():
    """Create regexp object for matching any valid numbers.

    Returns
    -------
    regular expression object
        regexp object that mathes any valid number

    """
    return re.compile(r"\d+[.]?\d*|[.]\d+")


@executeOnce
def getStandartFuncRegex():
    """Create regexp object that matches standart mathematical operators.

    Returns
    -------
    regular expression object
        regexp object that mathes any valid mathematical operator

    """
    keys = list(getStandartFuncDict().keys())
    keys.sort(reverse=True)
    standartFuncStr = str('|').join(keys)
    for symbol in REGEX_SPEC_SYMBOLS:
        standartFuncStr = standartFuncStr.replace(symbol, "\\"+symbol)
    return re.compile(standartFuncStr)


@executeOnce
def getConstsRegex(functions=None):
    """Create regexp object that matches any constants from math module and user-defined module.

    Parameters
    ----------
    functions : module
        User-specified module containing functions (default is None)

    Returns
    -------
    regular expression object
        regexp object that mathes any valid mathematical operator

    """
    return re.compile(str('|').join(getConstDict(functions).keys()))


def findClosingBracket(expression):
    """Check expression for valid brackets and finds the position of closing one.

    Parameters
    ----------
    expression : str
        String where to find closing bracket

    Returns
    -------
    int
        position of last balanced closing bracket in expression

    """
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
    """Parse string expression to postfix polish notation.

    Parameters
    ----------
    expression : str
        expression string to parse into polish notation
    functions : module
        user-defined module with functions and constants. Will overwrite standart functions if needed (default is None)

    Returns
    -------
    list
        Postfix polish notation expression, where mathematical functions have been already calculated. List contains of numbers and functions, that represents mathematical operators
    
    """
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
        while expression[searchPos] == ' ':
            searchPos += 1
        match = numRegex.match(expression, searchPos)
        if expression[searchPos] == '(':
            operators.push(FuncWithPriority('(', -1))
            prevPushed = '('
            searchPos += 1
        elif expression[searchPos] == ')':
            lastItem = operators.pop()
            while lastItem.func != '(' and not operators.isEmpty():
                ppnExp.append(lastItem.func)
                lastItem = operators.pop()
            if lastItem.func != '(':
                raise Exception("Brackets are not balanced!")
            searchPos += 1
        elif match:
            prevPushed = float(match.string[match.start():match.end()])
            ppnExp.append(prevPushed)
            searchPos = match.end()
        else:
            match = standartFuncRegex.match(expression, searchPos)
            if match:
                matchStr = match.string[match.start(): match.end()]
                if matchStr in ('-', '+') and (isinstance(prevPushed, Iterable) or prevPushed == '(' or prevPushed is None):
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
                        mathFuncEnd = match.end() + \
                            findClosingBracket(expression[match.end():])
                        innerExpression = expression[match.end(
                        )+1:mathFuncEnd]
                        paramStrs = [innerExpression]
                        if re.match(r"[^(]*(\(([^()])*\))*,(\(([^()])*\))*[^)]*", innerExpression):
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
    """Calculate mathematical expression from string.

    Parameters
    ----------
    expression : str
        expression string to parse into polish notation
    functions : module
        user-defined module with functions and constants. Will overwrite standart functions if needed (default is None)

    Returns
    -------
    float, bool
        value of calculated expression

    """
    expression = expression.strip(' ')
    ppnExpression = parseExpression(expression, functions)
    calcStack = Stack()
    for item in ppnExpression:
        if callable(item):
            args = []
            for arg in inspect.getfullargspec(item).args:
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
