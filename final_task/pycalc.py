import math
import argparse
import pdb
import setuptools





CONSTANTS = {
    'pi' : math.pi,
    'e' : math.e,
    'tau': math.tau
    }

_FUNCTIONS = {
    'acos': math.acos,
    'asin': math.asin,
    'atan': math.atan,
    'atan2': math.atan2,
    'ceil': math.ceil,
    'cosh': math.cosh,
    'degrees': math.degrees,
    'exp': math.exp,
    'fabs': math.fabs,
    'floor': math.floor,
    'fmod': math.fmod,
    'frexp': math.frexp,
    'hypot': math.hypot,
    'ldexp': math.ldexp,
    'modf': math.modf,
    'pow': math.pow,
    'radians': math.radians,
    'sinh': math.sinh,
    'sqrt': math.sqrt,
    'tan': math.tan,
    'tanh': math.tanh
}


OPERATORS = {'+': (1, lambda x, y: x + y, '+', "left"), 
             '-': (1, lambda x, y: x - y, '-', "left"),
             '*': (2, lambda x, y: x * y, '*', "left"),
             '/': (2, lambda x, y: x / y, '/', "left"), 
             '//': (2, lambda x, y: x // y, '//', "left"), 
             '^': (3, lambda x, y: x ** y, '^', "right"), 
             '>': (0, lambda x, y: x > y, '>', "left"),
             '<': (0, lambda x, y: x < y, '<', "left"), 
             '>=': (0, lambda x, y: x >= y, '>=', "left"),
             '<=': (0, lambda x, y: x <= y, '<=', "left"), 
             '==': (0, lambda x, y: x == y, '==', "left"), 
             '!=': (0, lambda x, y: x != y, '!=', "left"),
             '%': (2, lambda x, y: x % y, '%', "left")}

FUNCTIONS = {'sqrt': (2, math.sqrt), 
             'log': (2, math.log), 
             'sin': (2, math.sin), 
             'cos': (2, math.cos), 
             'tan': (2, math.tan), 
             'exp': (2, math.exp),
             'acos': (2, math.acos),
             'asin': (2, math.asin),
             'atan': (2, math.atan),
             'log': (2, math.log),
             'round': (2, lambda x: round(x)), 
             'abs': (2, lambda x: abs(x)), 
             'log10': (2, math.log10), 
             'log2': (2, math.log2), }


class ERROR(Exception): 
#     self.with_traceback()
    pass

def parse(formula_string):
    number = ''
    func = ''
    op = ''
    output = []
    for symbol in formula_string:
        if symbol in '1234567890.': 
            number += symbol  
        elif number: 
            output.append(float(number) )
            number = ''
        if symbol in OPERATORS.get(symbol, '<=>=!=='):
            op += symbol
        elif op:    
            output.append(op)
            op = ''
        if symbol.lower() in "abcdefghijklmnopqrstuvwxyz":
            func += symbol
        elif func:
            output.append(func)
            func = ''
        if symbol in "()":
            output.append(symbol)
            
    if number:
        output.append(float(number))
    if func:
        output.append(func)
    if op:
        raise SyntaxError("ERROR: operator in the end of expression")
    return output

def preproc(parsed):
    output = []
    if parsed.count("(") != parsed.count(")"):
        raise SyntaxError("ERROR: Unbalanced parenthesis")
    if parsed[0] in OPERATORS:
        parsed.insert(0, "(")
        parsed.append(")")
    if parsed[0]=="-":
        parsed.insert(0, 0.0)
#     pdb.set_trace()
    
    i = 0
    while i < len(parsed):
        if parsed[i] in FUNCTIONS and type(parsed[i+1])==float:
            to_app = str(parsed[i])+str(int(parsed[i+1]))
            if to_app not in FUNCTIONS:
                raise SyntaxError("ERROR: Wrong function")
            output.append(to_app)
            i += 2
        if parsed[i] == "--":
            output.append('+')
            i += 1
        if parsed[i] == "-" and (parsed[i-1] == "(" or parsed[i-1] in OPERATORS) and (parsed[i+1] in FUNCTIONS):
#             to_app = parsed[i]+str(parsed[i+1])
            output.append(-1.0)
            output.append('*')
#             parsed.remove(parsed[i])
            i += 1
        if parsed[i] == "-" and (parsed[i-1] == "(" or parsed[i-1] in OPERATORS):
            to_app = parsed[i]+str(parsed[i+1])
            output.append(float(to_app))
            i += 2
            
        else: 
            output.append(parsed[i])
            i += 1
    return output            

def sh(parsed):
    output = []
    stack = []
    for t in parsed:
        if type(t) == float:
            output.append(t)
        elif t in FUNCTIONS:
            stack.append(t)
        elif t in CONSTANTS:
            output.append(CONSTANTS[t])
        elif t in OPERATORS:
            while stack and (stack[-1] != '(') and ((stack[-1] in FUNCTIONS) or (OPERATORS[t][3] == 'left' and OPERATORS[stack[-1]][0] >= OPERATORS[t][0])):
                output.append(stack.pop())
            stack.append(t)
        elif t == '(':
            stack.append(t)
        elif t == ")":
            while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    output.append(x)        
    while stack:
            f = stack.pop()
            output.append(f)
    return output


def calc(polish):
        stack = []
        for t in polish:
            if t in FUNCTIONS:
                x = stack.pop()
                to_app = FUNCTIONS[t][1](x)
                stack.append(to_app)             
            elif t in OPERATORS:
                y, x = stack.pop(), stack.pop()
                stack.append(OPERATORS[t][1](x, y))
            else:
                stack.append(t)
        if type(stack[0]) == bool:
            return stack[0]
        if stack[0]-int(stack[0])==0:
            return int(stack[0])
        else: return stack[0]

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('to_eval', help='expression to evaluate', type=str, nargs='+')
    args = parser.parse_args()
    sss = "".join(args.to_eval)
    try:
        result = calc(sh(preproc(parse(sss))))
        print(result)
    except Exception as error:
        print('ERROR: ', error)


if __name__=="__main__":
    Main()
