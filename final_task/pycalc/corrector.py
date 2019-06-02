import re
import math
import definitions





class Corrector:

    """base class for correct input string for parsing """

    def __init__(self):
        """declare row(in regex) and compiled part of expression"""
        self._expr = ""
        self._funcPos = []

        self.constantR = (
            r"("
            + "|".join([re.escape(const) for const in definitions._constants])
            + ")"
        )
        self.functionR = (
            r"("
            + "|".join(
                [
                    re.escape(func)
                    for func in sorted(
                        definitions._functions, key=lambda func: len(func), reverse=True
                    )
                ]
            )
            + ")"
        )
        self.operatorR = (
            r"("
            + r"|".join(
                [re.escape(op)
                 for op in definitions._operators if op not in ["+", "-"]]
            )
            + r"|="
            r")"
        )

        self.numberR = definitions._number
        self.constantC = re.compile(self.constantR)
        self.functionC = re.compile(self.functionR)
        self.numberC = re.compile(self.numberR)
        self.operatorC = re.compile(self.operatorR)

    def findFuncPos(self):
        """find functions positions in expression """
        self._funcPos = []
        for result in re.finditer(self.functionC, self._expr):
            for pos in range(result.start(), result.end()):
                self._funcPos.append(pos)

    def constInterpolation(self):
        self.findFuncPos()
        strin = self._expr
        for result in re.finditer(self.constantC, self._expr):
            if result.start() not in self._funcPos:
                strin = re.sub(
                    result.group(),
                    str(definitions._constants.get(result.group()).value),
                    strin,
                )
        self._expr = strin

    def plusMinusReduce(self):
        strin = self._expr
        while (
            re.search(re.compile(r"\-\-"), strin)
            or re.search(re.compile(r"\+\+"), strin)
            or re.search(re.compile(r"\+\-"), strin)
            or re.search(re.compile(r"\-\+"), strin)
        ):
            strin = re.sub(r"\-\-", "+", strin)
            strin = re.sub(r"\+\+", "+", strin)
            strin = re.sub(r"\+\-", "-", strin)
            strin = re.sub(r"\-\+", "-", strin)
        self._expr = strin

    def spaceReduce(self):
        spaceC = re.compile(self.numberR + r"[\s]+" + self.numberR)
        spaceOC = re.compile(self.operatorR + r"[\s]+" + self.operatorR)
        strin = self._expr
        if re.search(spaceC, strin) or re.search(spaceOC, strin):
            raise ValueError("space beatwin operators")
        else:
            strin = re.sub(r"[\s]+", "", strin)
        self._expr = strin

    def unaryPlusReduce(self):
        strin = self._expr
        operatorMap = {(op + "+"): op for op in definitions._operators}
        operatorMapC = re.compile(
            r"(" + "|".join([re.escape(op) for op in operatorMap]) + ")"
        )
        # print(operatorMap)
        if re.search(re.compile(r"^\+"), strin):
            strin = re.sub(r"^\+", r"", strin)
        if re.search(re.compile(r"\(\+"), strin):
            strin = re.sub(r"\(\+", "(", strin)
        if re.search(re.compile(r"\,\+"), strin):
            strin = re.sub(r"\,\+", ",", strin)
        for result in re.finditer(operatorMapC, strin):
            strin = re.sub(
                re.compile(re.escape(result.group())),
                operatorMap.get(result.group()),
                strin,
            )
        self._expr = strin

    def unaryMinusReduce(self):
        minusPredecessors = []

        minusPredecessors.extend(
            [
                re.escape(op)
                for op in sorted(
                    definitions._operators, key=lambda op: len(op), reverse=True
                )
            ]
        )

        minusPredecessors.append(r"\A")

        minusPredecessors.append(re.escape("("))

        unaryMinusBasicR = (
            "(" + "|".join(minusPredecessors) + ")" +
            re.escape("-") + self.numberR
        )
        unaryMinusBasicM = re.compile(unaryMinusBasicR)
        minusPredecessorsM = re.compile("|".join(minusPredecessors))

        offset = 0
        for result in re.finditer(unaryMinusBasicM, self._expr):
            curUnaryMinusPos = 0
            if result.start() > 0:
                curUnaryMinusPos = minusPredecessorsM.match(
                    self._expr, result.start() + offset
                ).end()
            self._expr = (
                self._expr[:curUnaryMinusPos] +
                "(0" + self._expr[curUnaryMinusPos:]
            )
            offset += 2
            self._expr = (
                self._expr[: result.end() + offset]
                + ")"
                + self._expr[result.end() + offset:]
            )
            offset += 1

        minusSuccessors = []
        minusSuccessors.extend(
            [
                re.escape(func + "(")
                for func in sorted(
                    definitions._functions, key=lambda func: len(func), reverse=True
                )
            ]
        )
        minusSuccessors.append(re.escape("("))

        unaryMinusBracketR = (
            "("
            + "|".join(minusPredecessors)
            + ")"
            + re.escape("-")
            + "("
            + "|".join(minusSuccessors)
            + ")"
        )
        unaryMinusBracketM = re.compile(unaryMinusBracketR)

        result = unaryMinusBracketM.search(self._expr)
        while result:
            curUnaryMinusPos = 0
            if result.start() > 0:
                curUnaryMinusPos = minusPredecessorsM.match(
                    self._expr, result.start()
                ).end()
            self._expr = (
                self._expr[:curUnaryMinusPos] +
                "(0" + self._expr[curUnaryMinusPos:]
            )
            offset = 2

            lastBracketPos = result.end() + offset
            bracketCounter = 1
            while bracketCounter > 0:
                if self._expr[lastBracketPos] == "(":
                    bracketCounter += 1
                elif self._expr[lastBracketPos] == ")":
                    bracketCounter -= 1
                lastBracketPos += 1
            self._expr = self._expr[:lastBracketPos] + \
                ")" + self._expr[lastBracketPos:]
            result = unaryMinusBracketM.search(self._expr)

    def correct(self, iExpr):
        self._expr = iExpr
        self.spaceReduce()
        self.constInterpolation()
        self.plusMinusReduce()
        self.unaryPlusReduce()
        self.unaryMinusReduce()
        


        return self._expr
