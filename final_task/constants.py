import operator
import math

OPERATORS = {'+': (1, operator.add),
             '-': (1, operator.sub),
             '*': (2, operator.mul),
             '/': (2, operator.truediv),
             '//': (2, operator.floordiv),
             '%': (2, operator.mod),
             '^': (3, operator.pow)}
COMPARISON_OPERATORS = {'>=': operator.ge,
                        '<=': operator.le,
                        '!=': operator.ne,
                        '==': operator.eq,
                        '>': operator.gt,
                        '<': operator.lt}
MATH_FUNC, MATH_CONST = {}, {}
MATH_FUNC["abs"], MATH_FUNC["round"] = abs, round


def add_attr_to_dict():
    for attr in dir(math):
        if type(getattr(math, attr)) != float:
            if callable(getattr(math, attr)):
                MATH_FUNC[attr] = getattr(math, attr)
        else:
            MATH_CONST[attr] = getattr(math, attr)


add_attr_to_dict()
