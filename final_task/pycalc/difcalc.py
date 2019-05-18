import re
import pycalc.easyCalculation as easyCalculation
import math
from numbers import Number


class ComplexCalc():
    def __init__(self):
        self.const = {
            attr: getattr(
                math,
                attr) for attr in dir(math) if isinstance(
                getattr(
                    math,
                    attr),
                Number)}
        self.const["True"] = 1
        self.const["False"] = 0

    calc = easyCalculation.Calculator()

    math_functions = {**{attr: getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))},
                      **{"abs": lambda a: abs(a),
                         "round": lambda a: round(a),
                         "pow": lambda a, b: pow(a, b)}}

    def expression_search(self, expr):

        while True:

            func = re.search(r'[A-ZAa-z]+1?0?', expr)

            if func is None:
                return self.calc.calculate(expr)

            afterExpr = func.end()
            k = func.start()
            if func[0] in self.const:

                s = self.const[func[0]]
                expr = expr[:k] + str(s) + expr[afterExpr:]
                continue

            searcher = 0
            count = 1
            for one in expr[afterExpr + 1:]:

                searcher += 1
                if one == ")":
                    count -= 1
                if one == "(":
                    count += 1
                if count == 0:
                    break
            end = searcher + afterExpr
        # выкинуть если конец строки
            if expr[afterExpr] != '(':

                raise Exception(
                    "the expression must be written in the following way 'function(expression)'")

            else:

                a = self.__find_replacement(func[0], expr[afterExpr + 1:end])
                expr = expr[:k] + a + expr[end + 1:]
                if float(a) < 0:
                    end = k + len(a) - 1
                    expr = self.calc._calc_if_power(expr, k, end)

    def __find_replacement(self, func, expr):

        if func in ComplexCalc.math_functions:
            allargs = self.__commasplit(expr)

            k = []
            for each in allargs:
                k.append(float(self.expression_search(each)))

            a = '{:.15f}'.format(ComplexCalc.math_functions[func](*k))

        else:

            raise Exception("Indefined function")
        return str(a)

    def __commasplit(self, expr):
        breketscounter = 0
        preve = 0
        count = 1
        split = []
        for each in expr:
            if breketscounter == 0 and each == ",":
                split.append(expr[preve:count - 1])
                preve = count

            elif each == "(":
                breketscounter += 1
            elif each == ")":
                breketscounter -= 1
            count += 1

        split.append(expr[preve:count])

        return split
    compare = {

        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
        "==": lambda a, b: a == b,
        "<": lambda a, b: a < b,
        "!=": lambda a, b: a != b


    }

    def calculate(self, expr):

        place = re.search(r'(>=)|(>)|(<=)|(<)|(!=)|(==)', expr)

        while place is not None:
            after = re.search(r'(>=)|(>)|(<=)|(<)|(!=)|(==)',
                              expr[place.end():])
            a = self.expression_search(expr[:place.start()])
            if after is None:
                b = self.expression_search(expr[place.end():])
            else:
                b = self.expression_search(
                    expr[place.end():after.start() + place.end()])
            if a and b:

                rezult = ComplexCalc.compare[place[0]](a, b)
                end = ""
                if after is not None:
                    end = expr[after.end() + place.end():]
                expr = str(rezult) + end
            else:
                raise Exception(
                    "uncorrect expression must be 'expr' operator 'expr'")
            place = re.search(r'(>=)|(>)|(<=)|(<)|(!=)|(==)', expr)
            if place is None:
                return bool(self.expression_search(expr))
        return self.expression_search(expr)
