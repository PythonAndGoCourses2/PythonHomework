from functions import priorities,regexSpecialSymbols
from inspect import signature
import re

class Functions:
    def __init__(self, functions, priority = priorities, regexSpecSymbols = regexSpecialSymbols):
        self.functions = functions
        self.priorities = priority
        self.regexSpecSymbols = regexSpecSymbols
    
    def getFuncCompiledRegexp(self):
        regexpStr = str("|").join(self.functions.keys())
        for symbol in self.regexSpecSymbols:
            regexpStr = regexpStr.replace(symbol, "\\"+symbol)
        return re.compile(regexpStr)
    
    def getPriority(self, func):
        return self.priorities.get(func, 6)
    
    def getFunc(self, func):
        result = self.functions[func]
        if not result:
            raise ValueError("Function is undefined")
        return result
    
    def getNumOperands(self, func):
        if type(func) == str:
            function = self.getFunc(func)
            return len(signature(function).parameters)
        elif callable(func):
            return len(signature(func).parameters)
        else:
            raise TypeError("Trying to get number of operands for "+func)
