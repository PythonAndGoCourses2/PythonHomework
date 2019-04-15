import math


def arithmetic(a, b, chr):
    if chr == '^':
        return a**b
    if chr == '*':
        return a*b
    if chr == '/':
        return a/b
    if chr == '//':
        return a//b
    if chr == '%':
        return a%b
    if chr == '+':
        return a+b
    if chr == '-':
        return a-b


def functions(a, func, b=None):
    if func == 'sin':
        return math.sin(a)
    if func == 'cos':
        return math.cos(a)
    if func == 'tan':
        return math.tan(a)
    if func == 'asin':
        return math.asin(a)
    if func == 'acos':
        return math.acos(a)
    if func == 'atan':
        return math.atan(a)
    if func == 'sinh':
        return math.sinh(a)
    if func == 'cosh':
        return math.cosh(a)
    if func == 'tanh':
        return math.tanh(a)
    if func == 'asinh':
        return math.asinh(a)
    if func == 'acosh':
        return math.acosh(a)
    if func == 'atanh':
        return math.atanh(a)
    if func == 'degrees':
        return math.degrees(a)
    if func == 'radians':
        return math.radians(a)
    if func == 'hypot':
        return math.hypot(a, b)
    if func == 'ceil':
        return math.ceil(a)
    if func == 'copysign':
        return math.copysign(a, b)
    if func == 'fabs':
        return math.fabs(a)
    if func == 'factorial':
        return math.factorial(a)
    if func == 'floor':
        return math.floor(a)
    if func == 'fmod':
        return math.fmod(a, b)
    if func == 'frexp':
        return math.frexp(a)
    if func == 'ldexp':
        return math.ldexp(a, b)
    if func == 'fsum':
        return math.fsum(a)
    if func == 'isfinite':
        return math.isfinite(a)
    if func == 'isinf':
        return math.isinf(a)
    if func == 'isnan':
        return math.isnan(a)
    if func == 'modf':
        return math.modf(a)
    if func == 'trunc':
        return math.trunc(a)
    if func == 'expm1':
        return math.expm1(a)
    if func == 'log':
        if b != None:
            return math.log(a, b)
        else:
            return math.log(a)
    if func == 'log1p':
        return math.log1p(a)
    if func == 'log10':
        return math.log10(a)
    if func == 'log2':
        return math.log2(a)
    if func == 'exp':
        return math.exp(a)
    if func == 'pow':
        return math.pow(a, b)
    if func == 'sqrt':
        return math.sqrt(a)
    if func == 'erf':
        return math.erf(a)
    if func == 'erfc':
        return math.erfc(a)
    if func == 'gamma':
        return math.gamma(a)
    if func == 'lgamma':
        return math.lgamma(a)
    if func == 'abs':
        return abs(a)
    if func == 'round':
        return round(a, b)


def constants_calculation(chr):
    if chr == 'pi':
        return math.pi
    if chr == 'e':
        return math.e