import re
import math
import definitions


class Corrector(object):

    """base class for correct input string for parsing """

    def __init__(self):
        """declare row(in regex) and compiled part of expression"""
        self._expr = ""
        self._funcPos = []

        self.constantR = '(' + '|'.join(
            [re.escape(const) for const in sorted(
                definitions._constants, key=lambda const: len(const), reverse=True)]
        ) + ')'
        self.functionR = '(' + '|'.join(
            [re.escape(func) for func in sorted(
                definitions._functions, key=lambda func: len(func), reverse=True)]
        ) + ')'
        self.numberR = definitions._number.regex
        self.constantC = re.compile(self.constantR)
        self.functionC = re.compile(self.functionR)
        self.numberC = re.compile(self.numberR)

    def _findFunc(self):
        """find functions in expression """
        self._funcPos = []
        for result in re.finditer(self.functionC, self._expr):
            for pos in range(result.start(), result.end()):
                self._funcPos.append(pos)

    def _constInterpolation(self):
        self._findFunc()
        offset = 0
        _exprStr = self._expr
        for result in re.finditer(self.constantC, self._expr):
            if result.start() not in self._funcPos:
                curConstant = self._expr[result.start():result.end()]
                curConstantValue = str(
                    definitions._constants[curConstant].value)

                _exprStr = _exprStr[:result.start() + offset] + \
                    curConstantValue + \
                    _exprStr[result.end() + offset:]
                # offset += length of constant substitution - length of constant name
                offset += len(curConstantValue) - \
                    (result.end() - result.start())
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
            if (minusCount % 2 == 1):  # minus
                _exprStr = _exprStr[:result.start() + offset] + \
                    '-' + \
                    _exprStr[result.end() + offset:]
                # offset += 1 - length of plus-minus expression
                offset += 1 - (result.end() - result.start())
            else:  # plus
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
            [re.escape(op) for op in sorted(definitions._operators, key=lambda op: len(op), reverse=True)])
        # add beginning of the string
        plusPredecessors.append(r'\A')
        # add open bracket
        plusPredecessors.append(re.escape('('))
        unaryPlusR = '(' + '|'.join(plusPredecessors) + ')' + re.escape('+')
        unaryPlusM = re.compile(unaryPlusR)

        _exprStr = self._expr
        offset = 0
        for result in re.finditer(unaryPlusM, self._expr):
            _exprStr = _exprStr[:result.end() + offset - 1] + \
                _exprStr[result.end() + offset:]
            offset -= 1

        self._expr = _exprStr

    def _unaryMinusReduce(self):
        minusPredecessors = []
        # add operators
        minusPredecessors.extend(
            [re.escape(op) for op in sorted(definitions._operators, key=lambda op: len(op), reverse=True)])
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
                curUnaryMinusPos = minusPredecessorsM.match(
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
            [re.escape(func + '(') for func in sorted(definitions._functions, key=lambda func: len(func), reverse=True)])
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
                curUnaryMinusPos = minusPredecessorsM.match(
                    self._expr, result.start()).end()
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
