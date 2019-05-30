import math
import argparse
import pdb





_CONSTANTS = {
    'pi' : math.pi,
    'e' : math.e,
    'phi': (1 + 5 ** .5) / 2
}

_FUNCTIONS = {
    'abs': abs,
    'acos': math.acos,
    'asin': math.asin,
    'atan': math.atan,
    'atan2': math.atan2,
    'ceil': math.ceil,
    'cos': math.cos,
    'cosh': math.cosh,
    'degrees': math.degrees,
    'exp': math.exp,
    'fabs': math.fabs,
    'floor': math.floor,
    'fmod': math.fmod,
    'frexp': math.frexp,
    'hypot': math.hypot,
    'ldexp': math.ldexp,
    'log': math.log,
    'log10': math.log10,
    'modf': math.modf,
    'pow': math.pow,
    'radians': math.radians,
    'sin': math.sin,
    'sinh': math.sinh,
    'sqrt': math.sqrt,
    'tan': math.tan,
    'tanh': math.tanh
}

OPERATORS = {'+': (1, lambda x, y: x + y, '+'), 
             '-': (1, lambda x, y: x - y, '-'),
             '*': (2, lambda x, y: x * y, '*'),
             '/': (2, lambda x, y: x / y, '/'), 
             '^': (2, lambda x, y: x ** y, '^'), 
             '>': (1, lambda x, y: x > y, '>'),
             '<': (1, lambda x, y: x < y, '<'), 
             '>=': (1, lambda x, y: x >= y, '>='),
             '<=': (1, lambda x, y: x <= y, '<='), 
             '==': (1, lambda x, y: x == y, '=='), 
             '!=': (1, lambda x, y: x != y, '!='),}

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
             'abs': (2, lambda x: abs(x))}




def evaluate(expression, vars={}):
    try:
        p = Parser(expression, vars)
        value = p.getValue()
    except ValueError:
        tb = sys.exc_info()[2]
#         msg = ex.message
        raise Exception(tb)

    # Return an integer type if the answer is an integer
    if int(value) == value:
        return int(value)

    # If Python made some silly precision error
    # like x.99999999999996, just return x + 1 as an integer
    epsilon = 0.0000000001
    if int(value + epsilon) != int(value):
        return int(value + epsilon)
    elif int(value - epsilon) != int(value):
        return int(value)

    return value


def parse(formula_string):
        number = ''
        func = []
        op = ''
#         pdb.set_trace()
        for symbol in formula_string:
            if symbol in '1234567890.': 
                number += symbol  
            elif number: 
                yield float(number) 
                number = ''
            if symbol in OPERATORS.get(symbol, '<=>=!=='): 
                op += symbol
            elif op:    
                yield op
                op = ''
            if symbol.lower() in "abcdefghijklmnopqrstuvwxyz":
                func.append(symbol)
            elif func:
                var = ''.join(func)
                yield var
                var = ''
                func = []
            if symbol in "()":
                yield symbol
        if number:
            yield float(number)


def sh(parsed):
    output = []
    stack = []
#     pdb.set_trace()
    for t in parsed:
        if type(t) == float:
            output.append(t)
        elif t in FUNCTIONS:
            stack.append(t)
        elif t in OPERATORS:
            while stack and (stack[-1] != '(') and ((stack[-1] in FUNCTIONS) or (OPERATORS[stack[-1]][0] >= OPERATORS[t][0])):
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


def calculate(polish):
        stack = []
#         pdb.set_trace()
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
        return stack[0]

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument('to_eval', help='expression to evaluate', type=str, nargs='+')
    args = parser.parse_args()
    sss = "".join(args.to_eval)
    result = calculate(sh(parse(sss)))
    print(sss, result)


if __name__=="__main__":
    Main()
