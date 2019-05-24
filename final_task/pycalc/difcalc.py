import re
import pycalc.easyCalculation as easyCalculation
import math
from numbers import Number

class ComplexCalc(easyCalculation.Calculator):

    const = {
        **{attr: getattr(math,attr) for attr in dir(math) if isinstance(getattr(math,attr),Number)},
        **{"True": 1,"False": 0}
        }
    math_functions = {
        **{attr: getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))},
        **{"abs": lambda a: abs(a),
           "round": lambda a: round(a),
           "pow": lambda a, b: pow(a, b)}
           }

    def expression_search(self, expr):

        while True:

            func = re.search(r'[A-ZAa-z]+1?0?', expr)

            if func is None:
                return self.search_brakets(expr)

            afterExpr = func.end()
            place = func.start()
            if func[0] in self.const:

                rezult = self.const[func[0]]
                expr = expr[:place] + str(rezult) + expr[afterExpr:]
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

                rezult = self._find_replacement(func[0], expr[afterExpr + 1:end])
                expr = expr[:place] + rezult + expr[end + 1:]
                if float(rezult) < 0:
                    end = place + len(rezult) - 1
                    expr = self._calc_if_power(expr, place, end)

    def _find_replacement(self, func:str, expr:str):

        if func in ComplexCalc.math_functions:
            allargs = self._commasplit(expr)

            float_args = []
            for each in allargs:
                float_args.append(float(self.expression_search(each)))

            rezult = '{:.15f}'.format(ComplexCalc.math_functions[func](*float_args))

        else:

            raise Exception("Indefined function")
        return str(rezult)

    def _commasplit(self, expr:str):
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

    def calculate(self, expr:str):
        #передалать с меньшим числом иф
        place = re.search(r'(>=)|(>)|(<=)|(<)|(!=)|(==)', expr)
        
        while place:
            after = re.search(r'(>=)|(>)|(<=)|(<)|(!=)|(==)',expr[place.end():])
            number_one = self.expression_search(expr[:place.start()])

            if not after :
                number_two = self.expression_search(expr[place.end():])
            else:
                number_two = self.expression_search(expr[place.end():after.start() + place.end()])

            if number_one is not None and number_two is not None:
                rezult = ComplexCalc.compare[place[0]](number_one, number_two)
                end = ""

                if after:
                    if after.start() == 0:
                        raise Exception("no symbols between compare")
                    end = expr[after.end() + place.end():]
                    expr = str(rezult) + after[0] + end
                else:
                    return bool(rezult)

            else:
                raise Exception(
                    "uncorrect expression must be 'expr' operator 'expr'")
            place = re.search(r'(>=)|(>)|(<=)|(<)|(!=)|(==)', expr)
            
        return self.expression_search(expr)
