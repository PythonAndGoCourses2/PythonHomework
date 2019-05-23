import re
import pycalc.operators as operators
import pycalc.difcalc as difcalc
from numbers import Number
import importlib.util
from os import path


class CheckAndChange():

    def do_all_changes(self, expr, module):

        if not re.search(
                r'[0-9]+', expr) and not re.search(r'[A-ZAa-z]+', expr):
            raise Exception("No Numbers in expression")

        expr = expr.replace("//", "&")
        self.correct_brackets(expr)
        self.correct_spaces(expr)
        expr = expr.replace(" ", "")
        self.add_args(module)
        return expr

    def add_args(self, modul):
        if modul:
            base = path.basename(modul)

            module_name = path.splitext(base)[0]
            spec = importlib.util.spec_from_file_location(module_name, modul)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            new_functions = {
                attr: getattr(module,attr) for attr in dir(module) if callable(getattr(module,attr))
                }
            difcalc.ComplexCalc.math_functions.update(new_functions)

            new_const = {
                attr: getattr(module,attr) for attr in dir(module)if isinstance(getattr(module,attr), Number)
                }             
            difcalc.ComplexCalc.const.update(new_const)

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
                    raise Exception("Check your spaces betwin")

                expression = expression[searcher + 1:]
                searcher = expression.find(" ")
            else:
                if searcher == len(expression) - 1:
                    break
                if searcher == 0:
                    expression = expression[1:]

    def correct_brackets(self, expr):
        counter = 0
        for one in expr:

            if one == "(":
                counter += 1
            elif one == ")":
                counter -= 1
            if counter < 0:
                raise Exception("check brackets! ")
        else:
            if counter != 0:
                raise Exception("check brackets! ")
