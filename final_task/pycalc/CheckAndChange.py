import re
import pycalc.operators as operators
import pycalc.difcalc as difcalc
from numbers import Number


class CheckAndChange():

    def do_all_changes(self, expr, module):
        expr = expr.replace("//", "&")
        self.correct_brackets(expr)
        self.correct_spaces(expr)
        expr = expr.replace(" ", "")
        self.addargs(module)
        return expr

    def addargs(self, modul):
        if modul is not None:
            if modul[-3:] == ".py":
                module = __import__(modul[:-3])
                new_functions = {
                    attr: getattr(
                        module,
                        attr) for attr in dir(module) if callable(
                        getattr(
                            module,
                            attr))}
                difcalc.ComplexCalc.math_functions.update(new_functions)
                new_const = {
                    attr: getattr(
                        module,
                        attr) for attr in dir(module) if isinstance(
                        getattr(
                            module,
                            attr),
                        Number)}
                difcalc.ComplexCalc.const.update(new_const)
            else:
                raise Exception("wrong file extension")

    def correct_spaces(self, expr):
        searcher = expr.find(" ")
        expression = expr

        while searcher != -1 and expression != "":
            if searcher != len(expression) - 1 and searcher != 0:
                if expression[searcher -
                              1].isdigit() and expression[searcher + 1].isdigit():
                    raise Exception("must not be 'digit' 'space' 'digit'")

                if expression[searcher - 1] in operators.operators \
                        and expression[searcher + 1] in operators.operators:
                    raise Exception(
                        "must not be 'operator' 'space' 'operator'")

                if expression[searcher - 1] in difcalc.ComplexCalc.compare \
                        and expression[searcher + 1] in difcalc.ComplexCalc.compare:
                    raise Exception("Check your spaces1")

                expression = expression[searcher + 1:]
                searcher = expression.find(" ")
            else:
                if searcher == len(expression) - 1:
                    break
                if searcher == 0:
                    expression = expression[1:]

    def correct_brackets(self, expr):

        if re.search(
                r'[0-9]+', expr) is None and re.search(r'[A-ZAa-z]+', expr) is None:
            raise Exception("No Numbers in expression")

        i = 0
        for one in expr:

            if one == "(":
                i += 1
            elif one == ")":
                i -= 1
            if i < 0:
                raise Exception("check brackets! ")
        else:
            if i != 0:
                raise Exception("check brackets! ")

# доделать всякие исключения, есть ли исключение на пустые скобки
