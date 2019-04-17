from dataStructures.stack import Stack
from dataStructures.queue import Queue
from functions import functions, priorities, regexSpecialSymbols
from functionsWorker import Functions
import re
import math
from inspect import signature
# TODO check exceptions
class Expression:
    def __init__(self, expression):
        """Initialization of expression object, optional parameter [expression] defines expression string"""
        self.ppnExpression = []
        self._operatorsStack = Stack()
        self.definedFuncs = Functions(functions)
        self.prevPriority = 0
        if not expression:
            raise ValueError("Expression is empty")
        self._parseToPPN(expression)

    def _pushBracket(self, bracket):
        if bracket == "(":
            self._operatorsStack.push(bracket)
            self.prevPriority = prevPrior = 0
        elif bracket == ")":
            if self._operatorsStack.isEmpty():
                    raise Exception("Brackets are not balanced")
            item = self._operatorsStack.pop()
            while item != "(":
                if self._operatorsStack.isEmpty():
                    raise Exception("Brackets are not balanced")
                self.ppnExpression.append(item)
                item = self._operatorsStack.pop()
        else: 
            raise Exception("pushBracket: Passed symbol is not a bracket")


    def _pushFunc(self, func):
        global prevPrior
        funcPrior = self.definedFuncs.getPriority(func)
        function = self.definedFuncs.getFunc(func)
        if funcPrior < self.prevPriority:
            self.ppnExpression.append(self._operatorsStack.pop())
        self._operatorsStack.push(function)
        self.prevPriority = funcPrior
    
    def _parseToPPN(self, expression):
        funcRegexp = Functions(functions).getFuncCompiledRegexp()# regular expression for ALL functions
        numRegexp = re.compile('[0-9]+[.]?[0-9]*') # regular expression for numbers
        searchPos = 0 # use this variable to track last position regular expressions were applied
        while searchPos < len(expression):
            if expression[searchPos] in {'(', ')'}:
                self._pushBracket(expression[searchPos]) # pushing bracket in operators stack
                searchPos+=1
            else:
                match = numRegexp.match(expression, searchPos) # match is used futher for changing searchPos
                if match:
                    self.ppnExpression.append(float(match.string[match.start():match.end()]))
                else:
                    match = funcRegexp.match(expression, searchPos)
                    if match:
                        self._pushFunc(match.string[match.start():match.end()])
                    else:
                        raise ValueError("Undefined tokens "+funcRegexp.split(expression[searchPos:])[0])
                searchPos = match.end()
        while not self._operatorsStack.isEmpty():
            self.ppnExpression.append(self._operatorsStack.pop())
    

    def calculate(self):
        calcStack = Stack()
        for item in self.ppnExpression:
            if item in {"(", ")"}:
                raise ValueError("Brackets are not balanced")
            elif callable(item):
                funcOperands = self.definedFuncs.getOperands(item)
                operands = []
                for operand in funcOperands:
                    operands.append(calcStack.pop())
                operands.reverse()
                calcStack.push(item(*operands))
            else:
                calcStack.push(item)
        return calcStack.pop()



        
        
