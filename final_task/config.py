import math
import operator
import string

LETTERS = tuple(string.ascii_lowercase + string.ascii_uppercase)
DIGITS = tuple(string.digits)

UNARY_OPERATORS = {'+': (1, operator.add),
                   '-': (1, operator.sub),
                   }

BINARY_OPERATORS = {'*': (2, operator.mul),
                    '/': (2, operator.truediv),
                    '//': (2, operator.floordiv),
                    '%': (2, operator.imod),
                    '^': (3, operator.ipow),
                    '<': (0, operator.lt),
                    '<=': (0, operator.le),
                    '>': (0, operator.gt),
                    '>=': (0, operator.ge),
                    '==': (0, operator.eq),
                    '!=': (0, operator.ne),
                    }

OPERATORS = UNARY_OPERATORS.copy()
OPERATORS.update(BINARY_OPERATORS)

PARENTHESES = ('(', ')')

OPERATORS_BEGIN = ('+', '-', '*', '/', '%', '^', '<', '>', '=', '!',)

DOUBLE_OPER_PART1 = ('/', '<', '>', '=', '!',)
DOUBLE_OPER_PART2 = ('/', '=',)

BUILT_IN_FUNCTIONS = ('abs', 'round')
NOT_SUPPORTED_MATH_FUNCTIONS = ('frexp', 'isclose', 'isinf', 'isfinite', 'isnan')
MATH_CONSTS = ('e', 'pi', 'inf', 'nan', 'tau')
MATH_FUNCTIONS = tuple([func for func in dir(math) if not func.startswith('_') and
                        func not in (MATH_CONSTS + NOT_SUPPORTED_MATH_FUNCTIONS)])

ALL_FUNCTIONS = BUILT_IN_FUNCTIONS + MATH_FUNCTIONS
ALL_FUNCTIONS_AND_CONSTS = ALL_FUNCTIONS + MATH_CONSTS

ALL_FUNCTIONS_DICT = {el: (4,) for el in ALL_FUNCTIONS}
ALL_FUNCTIONS_AND_OPERATORS_DICT = ALL_FUNCTIONS_DICT.copy()
ALL_FUNCTIONS_AND_OPERATORS_DICT.update(OPERATORS)


DELIMETERS = ('.', ',', ' ')
ALLOWED_TOKENS = OPERATORS_BEGIN + LETTERS + DIGITS + PARENTHESES + DELIMETERS