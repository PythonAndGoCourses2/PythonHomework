from dataStructures.stack import Stack
from dataStructures.queue import Queue
from functions import functions, priorities
import re
import math
from inspect import signature


operators = Stack()
output = Queue()
prevPrior = 0
prevOutput = 10
reSpecSymbols = ["*", "+", "^"]

def pushFunc(func):
    global prevPrior
    funcPrior = priorities.get(func, 6)
    function = functions[func]
    if function == None:
        raise Exception("pushFunc: " + func + " is undefined function")
    elif funcPrior == None:
        raise Exception("pushFunc: " + func + " priority is undefined")
    if funcPrior < prevPrior:
        output.push(operators.pop())
    operators.push(function)
    prevPrior = funcPrior

def pushBracket(bracket):
    global prevPrior
    if bracket == "(":
        operators.push(bracket)
        prevPrior = 0
    elif bracket == ")":
        if operators.isEmpty():
                raise Exception("Brackets are not balanced")
        item = operators.pop()
        while item != "(":
            if operators.isEmpty():
                raise Exception("Brackets are not balanced")
            output.push(item)
            item = operators.pop()
    else: 
        raise Exception("pushBracket: Passed symbol is not a bracket")
    
        

def parseToPPN(expression=""):
    numRegexp = re.compile('[0-9]+[.]?[0-9]*')
    funcRegexpStr = str("|").join(functions.keys())
    for symbl in reSpecSymbols:
        funcRegexpStr = funcRegexpStr.replace(symbl, "\\"+symbl)
    funcRegexp = re.compile(funcRegexpStr)
    searchPos = 0
    while searchPos < len(expression):
        match = numRegexp.match(expression, searchPos)
        if match != None:
            output.push(float(match.string[match.start():match.end()]))
        else:
            match = funcRegexp.match(expression, searchPos)
            if match != None:
                pushFunc(match.string[match.start():match.end()])
            elif expression[searchPos] in {'(', ')'}:
                pushBracket(expression[searchPos])
            else:
                raise Exception("Undefined function " + funcRegexp.split(expression[searchPos:])[0])
        if match != None:
            searchPos = match.end()
        else: 
            searchPos+=1
    while not operators.isEmpty():
        output.push(operators.pop())     

def getNumOperands(func):
    return len(signature(func).parameters)

def calculate():
    calcStack = Stack()
    item = output.pop()
    if item in {"(", ")"}:
        raise Exception("Brackets are not balanced")
    elif callable(item):
        raise Exception("Wrong order of operators and operands")
    calcStack.push(item)
    while not output.isEmpty():
        item = output.pop()
        if item in {"(", ")"}:
            raise Exception("Brackets are not balanced")
        elif callable(item):
            numOperands = getNumOperands(item)
            operands = []
            for i in range(1, numOperands+1):
                operands.append(calcStack.pop())
            operands.reverse()
            calcStack.push(item(*operands))
        elif type(item) == float:
            calcStack.push(item)
        else:
            raise Exception("Unknown type of item "+ item)
    return calcStack.pop()