import re
import math


import definitions

# basic error
def CorrectorError(Exception):
    pass

class Corrector(object):
    def __init__(self):
        self._expr = ""
        self._funcPos = []
        
        self.constantR = '(' + '|'.join( \
            [ re.escape(const) for const in sorted(definitions._constants, key=lambda const: len(const), reverse=True)] \
                                   ) + ')'
        self.functionR = '(' + '|'.join( \
            [ re.escape(func) for func in sorted(definitions._functions, key=lambda func: len(func), reverse=True)] \
                                   ) + ')'
        self.numberR = definitions._number.regex
        self.constantM = re.compile(self.constantR)
        self.functionM = re.compile(self.functionR)
        self.numberM = re.compile(self.numberR)


    def _findFunc(self):
        self._funcPos = []
        for result in re.finditer(self.functionM, self._expr):
            for pos in range(result.start(), result.end()):
                self._funcPos.append(pos)

    def _shortMultiplication(self):       
        self._findFunc()
        # contains insert positions
        insertPos = []
        
        numberOBracketM = re.compile(self.numberR + re.escape('('))
        for result in re.finditer(numberOBracketM, self._expr):
            if result.start() not in self._funcPos:
                insertPos.append(result.end() - 1)

        constOBracketM = re.compile(self.constantR + re.escape('('))
        for result in re.finditer(constOBracketM, self._expr):
            if result.start() not in self._funcPos:
                insertPos.append(result.end() - 1)


        cBracketNumberM = re.compile(re.escape(')') + self.numberR)
        for result in re.finditer(cBracketNumberM, self._expr):
            if result.start() not in self._funcPos:
                insertPos.append(result.start() + 1)

        cBracketConstM = re.compile(re.escape(')') + self.constantR)
        for result in re.finditer(cBracketConstM, self._expr):
            if result.start() not in self._funcPos:
                insertPos.append(result.start() + 1)

        cBracketOBracketM = re.compile(re.escape(')('))
        for result in re.finditer(cBracketOBracketM, self._expr):
            insertPos.append(result.start() + 1)

        numberConstM = re.compile(self.numberR + self.constantR)
        for result in re.finditer(numberConstM, self._expr):
            # find end of first component
            firstComponentEndPos = self.numberM.match(self._expr, result.start()).end()
            insertPos.append(firstComponentEndPos)

        constNumberM = re.compile(self.constantR + self.numberR)
        for result in re.finditer(constNumberM, self._expr):
            # find end of first component
            firstComponentEndPos = self.constantM.match(self._expr, result.start()).end()
            insertPos.append(firstComponentEndPos)

        constConstM = re.compile(self.constantR + self.constantR)
        for result in finditerOverlap(constConstM, self._expr):
            if result.start() not in self._funcPos:
                # find end of first component
                firstComponentEndPos = self.constantM.match(self._expr, result.start()).end()
                insertPos.append(firstComponentEndPos)

        numberFunctionM = re.compile(self.numberR + self.functionR)
        for result in re.finditer(numberFunctionM, self._expr):
            # find end of first component
            firstComponentEndPos = self.numberM.match(self._expr, result.start()).end()
            insertPos.append(firstComponentEndPos)
            
        _exprList = list(self._expr)
        for offset, pos in enumerate(sorted(insertPos)):
            # print add, pos
            _exprList.insert(pos + offset, '*')

        self._expr = "".join(_exprList)
        
            
    def _constInterpolation(self):
        # update info about function positions 
        self._findFunc()

        offset = 0        
        # don't want to change input string
        _exprStr = self._expr
        for result in re.finditer(self.constantM, self._expr):
            if result.start() not in self._funcPos:
                curConstant = self._expr[result.start():result.end()]
                curConstantValue = str(definitions._constants[curConstant].value) 

                _exprStr = _exprStr[:result.start() + offset] + \
                            curConstantValue + \
                           _exprStr[result.end() + offset:]
                # offset += length of constant substitution - length of constant name
                offset += len(curConstantValue) - (result.end() - result.start())
        self._expr = _exprStr

    def _plusMinusReduce(self):
        plusMinusM = re.compile('[' + re.escape('+') + re.escape('-') + ']+')
        offset = 0
        _exprStr = self._expr
        for result in re.finditer(plusMinusM, self._expr):
            curPlusMinusExpr = self._expr[result.start():result.end()]
            minusCount = 0
            for sign in curPlusMinusExpr:
                if sign == '-':
                    minusCount += 1
            if (minusCount % 2 == 1): # minus
                _exprStr = _exprStr[:result.start() + offset] + \
                           '-' + \
                           _exprStr[result.end() + offset:]
                # offset += 1 - length of plus-minus expression
                offset += 1 - (result.end() - result.start())
            else: #plus
                _exprStr = _exprStr[:result.start() + offset] + \
                           '+' + \
                           _exprStr[result.end() + offset:]
                # offset += 1 - length of plus-minus expression
                offset += 1 - (result.end() - result.start())

        self._expr = _exprStr

    def _unaryPlusReduce(self):
        plusPredecessors = []
        # add operators
        plusPredecessors.extend(
            [ re.escape(op) for op in sorted(definitions._operators, key=lambda op: len(op), reverse=True) ])
        # add beginning of the string
        plusPredecessors.append(r'\A')
        # add open bracket
        plusPredecessors.append(re.escape('('))
        unaryPlusR = '(' + '|'.join(plusPredecessors) + ')' + re.escape('+')
        unaryPlusM = re.compile(unaryPlusR)

        _exprStr = self._expr
        offset = 0
        for result in re.finditer(unaryPlusM, self._expr):
            _exprStr = _exprStr[:result.end() + offset - 1] + _exprStr[result.end() + offset:]
            offset -= 1

        self._expr = _exprStr

    def _unaryMinusReduce(self):
        minusPredecessors = []
        # add operators
        minusPredecessors.extend(
            [ re.escape(op) for op in sorted(definitions._operators, key=lambda op: len(op), reverse=True) ])
        # add beginning of string
        minusPredecessors.append(r'\A')
        # add open bracket
        minusPredecessors.append(re.escape('('))

        # without brackets
        unaryMinusBasicR = '(' + '|'.join(minusPredecessors) + ')' + \
                           re.escape('-') + self.numberR
        unaryMinusBasicM = re.compile(unaryMinusBasicR)
        minusPredecessorsM = re.compile('|'.join(minusPredecessors))

        offset = 0
        for result in re.finditer(unaryMinusBasicM, self._expr):
            # print result.end(), ':', offset, ':', self._expr
            curUnaryMinusPos = 0
            if result.start() > 0:
                curUnaryMinusPos = minusPredecessorsM.match( \
                self._expr, result.start() + offset).end()
            self._expr = self._expr[:curUnaryMinusPos] + '(0' + \
                         self._expr[curUnaryMinusPos:]
            offset += 2
            self._expr = self._expr[:result.end() + offset] + ')' + \
                         self._expr[result.end() + offset:]
            offset += 1

        # with brackets
        minusSuccessors = []
        minusSuccessors.extend(
            [ re.escape(func + '(') for func in sorted(definitions._functions, key=lambda func: len(func), reverse=True) ])
        minusSuccessors.append(re.escape('('))

        unaryMinusBracketR = '(' + '|'.join(minusPredecessors) + ')' + \
                           re.escape('-') + \
                           '(' + '|'.join(minusSuccessors) + ')'
        unaryMinusBracketM = re.compile(unaryMinusBracketR)

        # have to use while because self._expr
        # changes after each substitution
        result = unaryMinusBracketM.search(self._expr)
        while result:
            curUnaryMinusPos = 0
            if result.start() > 0:
                curUnaryMinusPos = minusPredecessorsM.match(self._expr, result.start()).end() 
            self._expr = self._expr[:curUnaryMinusPos] + '(0' + \
                         self._expr[curUnaryMinusPos:]
            offset = 2
            # find balanced brackets end position
            lastBracketPos = result.end() + offset
            bracketCounter = 1
            while bracketCounter > 0:
                if self._expr[lastBracketPos] == '(':
                    bracketCounter += 1
                elif self._expr[lastBracketPos] == ')':
                    bracketCounter -= 1
                lastBracketPos += 1
            self._expr = self._expr[:lastBracketPos] + ')' + \
                         self._expr[lastBracketPos:]
            result = unaryMinusBracketM.search(self._expr)

    def correct(self, iExpr):
        self._expr = iExpr.replace(' ', '').lower()
        self._shortMultiplication()
        self._constInterpolation()
        self._plusMinusReduce()
        self._unaryPlusReduce()
        self._unaryMinusReduce()

        
        return self._expr


def finditerOverlap(matcher, iExpr):
    result = matcher.search(iExpr)
    while result:
        yield result
        result = matcher.search(iExpr, result.start() + 1)
