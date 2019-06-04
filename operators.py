import math


class Operators:

    @staticmethod
    def sum(a, b):
        return a + b

    @staticmethod
    def sub(a, b):
        return a - b

    @staticmethod
    def mul(a, b):
        return a * b

    @staticmethod
    def div(a, b):
        return a / b

    @staticmethod
    def fdiv(a, b):
        return a // b

    @staticmethod
    def less(a, b):
        return a < b

    @staticmethod
    def less_or_eql(a, b):
        return a <= b

    @staticmethod
    def eql(a, b):
        return a == b

    @staticmethod
    def not_eql(a, b):
        return a != b

    @staticmethod
    def gr_or_eql(a, b):
        return a >= b

    @staticmethod
    def greater(a, b):
        return a > b


operators = {'+': Operators.sum, '-': Operators.sub, '*': Operators.mul, '/': Operators.div,
             '//': Operators.fdiv, '%': getattr(math, 'fmod'), '^': getattr(math, 'pow'), '<': Operators.less,
             '<=': Operators.less_or_eql, '==': Operators.eql, '!=': Operators.not_eql,
             '>=': Operators.gr_or_eql, '>': Operators.greater, 'abs': abs, 'round': round}

inf_func = {'^': 1,
            '*': 2, '/': 2, '//': 2, '%': 2,
            '+': 3, '-': 3,
            '<=': 4, '>=': 4, '<': 4, '>': 4,
            '<>': 5, '==': 5, '!=': 5}

post_func = {'!': 5}
parentheses = {'(': 3, ')': 3}
list_of_op = list(inf_func.keys()) + list(post_func.keys()) + list(parentheses.keys())



if __name__ == "__main__":
    Operators()
