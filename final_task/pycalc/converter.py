from . import definitions
from collections import deque
import re


class ConvertError(Exception):
    """class for error"""

    def __str__(self):
        return "cannot convert expression to RPN due to mismatched parentheses"


class Converter:
    def __init__(self):
        self.func = re.compile(
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
        self.num = re.compile(definitions._number)
        self.op = re.compile(
            r"|".join(
                [
                    re.escape(op)
                    for op in sorted(
                        definitions._operators, key=lambda func: len(func), reverse=True
                    )
                ]
            )
        )

    def convert(self, iExpr):
        """
        function for converting parsed expression in RPN
        """
        func = self.func
        num = self.num
        op = self.op
        pos = 0
        operatorStack = deque()
        outputStack = deque()
        

        while pos < len(iExpr):
            if num.match(iExpr, pos):
                numM = num.match(iExpr, pos)
                if "." in numM.group():
                    outputStack.append(float(numM.group()))
                else:
                    outputStack.append(int(numM.group()))
                pos = numM.end()
            elif iExpr[pos] == "(":
                operatorStack.appendleft("(")
                pos += 1
            elif iExpr[pos] == ")":
                if len(operatorStack) == 0:
                    raise ConvertError()
                top = operatorStack.popleft()
                while top != "(" and not len(operatorStack) == 0:
                    outputStack.append(top)
                    top = operatorStack.popleft()
                if top != "(":
                    raise ConvertError()
                pos += 1

            elif func.match(iExpr, pos):
                funcM = func.match(iExpr, pos)
                flag = False
                try:
                    a = iExpr[funcM.end()+1] != "("
                except IndexError:
                    flag = True

                if not flag and iExpr[funcM.end()] != "(":
                    raise ValueError("unknown function")
                if flag:
                    raise ValueError("no argument in function")
                operatorStack.appendleft(funcM.group())
                pos = funcM.end()

            elif iExpr[pos] == ",":
                if operatorStack:
                    top = operatorStack.popleft()
                    if op.match(top) and "(" in operatorStack:
                        while operatorStack:
                            outputStack.append(top)
                            top = operatorStack.popleft()
                            if top == "(":
                                operatorStack.appendleft(top)
                                break
                    elif not op.match(top):
                        break
                    else:
                        raise ConvertError()
                    outputStack.append(",")
                pos += 1

            elif op.match(iExpr, pos):
                match = op.match(iExpr, pos)
                if len(operatorStack) != 0:
                    top = operatorStack.popleft()

                    cond = (
                        func.match(top)
                        or (
                            op.match(top)
                            and (
                                definitions._operators[top].priority
                                > definitions._operators[match.group()].priority
                            )
                        )
                        or (
                            op.match(top)
                            and (
                                definitions._operators[top].priority
                                == definitions._operators[match.group()].priority
                                and definitions._operators[top].LAssos
                            )
                        )
                    ) and top != "("
                    if not cond:
                        operatorStack.appendleft(top)
                        operatorStack.appendleft(match.group())
                        pos = pos + len(match.group())

                    while cond:

                        outputStack.append(top)
                        if len(operatorStack) != 0:
                            top = operatorStack.popleft()
                            cond = (
                                func.match(top)
                                or (
                                    op.match(top)
                                    and (
                                        definitions._operators[top].priority
                                        > definitions._operators[match.group()].priority
                                    )
                                )
                                or (
                                    op.match(top)
                                    and (
                                        definitions._operators[top].priority
                                        == definitions._operators[
                                            match.group()
                                        ].priority
                                        and definitions._operators[top].LAssos
                                    )
                                )
                            ) and top != "("

                        else:
                            break
                        if not cond:
                            operatorStack.appendleft(top)
                            break

                else:

                    operatorStack.appendleft(match.group())
                    pos = pos + len(match.group())

        while len(operatorStack) != 0:
            outputStack.append(operatorStack.popleft())
        # print(outputStack)
        if "(" in outputStack or ")" in outputStack:
            raise ConvertError()

        return outputStack
