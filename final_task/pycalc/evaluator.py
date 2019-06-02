import definitions
import re
from collections import deque

class Evaluator(object):
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
    def evaluate(self, iExpr):
        func = self.func
        num = self.num
        op = self.op
        outputStack = []
        args = []
        for token in iExpr:
            if num.match(str(token)):
                outputStack.append(token)
                #print("num")
                #print(outputStack)
            elif op.match(token):
                operand2 = outputStack.pop()
                operand1 = outputStack.pop()
                outputStack.append(definitions._operators[token].func(operand1,operand2))
                #print("op")
                #print(outputStack)
            elif token ==",":
                outputStack.append(",")
            elif func.match(token):

                if "," in outputStack and num.match(str(outputStack[-3])) and outputStack[-2] == "," and num.match(str(outputStack[-1])):
                    operand2 = outputStack.pop()
                    comma = outputStack.pop()
                    operand1 = outputStack.pop()
                    outputStack.append(definitions._functions[token](operand1,operand2))
                else:
                    operand = outputStack.pop()
                    outputStack.append(definitions._functions[token](operand))
        if len(outputStack)==0:
            raise ValueError("empty expression")
        
        return outputStack[0]
