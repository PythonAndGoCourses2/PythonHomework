import re
import definitions
numberR = definitions._number.regex
constantR = '(' + '|'.join([re.escape(const) for const in sorted(definitions._constants, key=lambda const: len(const), reverse=True)]) + ')'
functionR = '(' + '|'.join([re.escape(func) for func in sorted(definitions._functions, key=lambda func: len(func), reverse=True)]) + ')'
functionC = re.compile(functionR)
#print(constantR)
#print(functionR)
_expr="10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5"
insertPos = []
_funcPos = []
for result in re.finditer(functionC, _expr):
    for pos in range(result.start(), result.end()):
        _funcPos.append(pos)
numberOfBracketO = re.compile(numberR + re.escape('('))
for result in re.finditer(numberOfBracketO, _expr):
    if result.start() not in _funcPos:
        insertPos.append(result.end() - 1)
print(insertPos)