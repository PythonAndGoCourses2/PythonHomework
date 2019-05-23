import re
import pycalc.operators as operators


class Calculator():

    def __calculation(self, expr):
        place = expr.rfind("^")

        while place != -1:
            findBefore = self.search_simple_number(expr[:place])
            begin = place - findBefore.end()
            findAfter = self.search_number_from_begin(expr[place:])
            end = place + findAfter.end()
            expr = self.__binary_operation(expr, begin, place, end)

            place = expr.rfind("^")

        place = re.search(r'/|\*|%|&', expr)

        while place:
            point = place.start()
            findBefore = self.search_number_from_end(expr[:point])
            begin = point - findBefore.end() + 1
            findAfter = self.search_number_from_begin(expr[point:])
            end = point + findAfter.end()
            expr = self.__binary_operation(expr, begin, point, end)
            place = re.search(r'/|\*|%|&', expr)

        return self.sum(expr)

    def sum(self, expr):

        if expr[-1] == "+" or expr[-1] == "-":
            raise Exception("'+' or '-'mustn' be the last even in brackets")

        summing = 0
        number = 0
        while expr != "":
            find = re.search(r'([+-]+)?([0-9]+([.][0-9]*)?|[.][0-9]+)', expr)
            if find.start() != 0:
                raise Exception("Undefine operator")
            number = find[0]

            expr = expr[find.end():]
            a = self.unary_rezult(number)
            summing += a
        return summing

    def unary_rezult(self, number):
        minus = number.count("-")
        plus = number.count("+")
        real_number = number[plus + minus:]
        if minus % 2 == 1:
            real_number = float("-" + real_number)
        else:
            real_number = float(real_number)
        return real_number

    def search_brakets(self, expr):
        expr = expr.replace(" ", "")

        while "(" in expr:

            end = expr.find(")")
            if end != len(expr) - \
                    1 and expr[end + 1] not in operators.operators:
                Exception("no operator after brackets")

            begin = expr[:end].rfind("(")
            if begin + 1 == end:
                raise Exception("no Number in brakets")

            if begin != 0 and expr[begin - 1] not in operators.operators \
                    and expr[begin - 1] != '-' and expr[begin - 1] != '+':
                raise Exception("no operators before brackets")

            rezult = self.__calculation("+" + expr[begin + 1:end])
            expr = expr[:begin] + str(rezult) + expr[end + 1:]

            if rezult < 0:
                end = begin + len(str(rezult)) - 1
                expr = self._calc_if_power(expr, begin, end)

        rezult = self.__calculation("+" + expr)

        return rezult

    def _calc_if_power(self, expr, begin, braket):
        place = braket + 1
        if braket is not len(expr) - 1 and expr[place] is "^":
            findAfter = self.search_number_from_begin(expr[place:])
            end = place + findAfter.end()
            expr = self.__binary_operation(expr, begin, place, end)
        return expr

    def __binary_operation(self, expr, begin, place, end):
       # вынести ту проверку которая есть в сумме в отдельный файл и добавть в
       # сюда вместо изменения флот на вот это вот все
        rezult = '{:.15f}'.format(operators.operators[expr[place]](
            self.unary_rezult(expr[begin:place]), self.unary_rezult(expr[place + 1:end])))

        before = expr[:begin]
        after = expr[end:]
        expr = before + rezult + after
        return expr

    def search_number_from_begin(self, expr):

        number = re.search(
            r'([+-]+)?([0-9]+([.][0-9]*)?|[.][0-9]+)', expr)

        if not number or number.start() != 1:
            raise Exception(
                "the expression should be written in the following form 'number operator number'")

        return number

    def search_number_from_end(self, expr):
        number = re.search(
            r'(([0-9]*[.])?[0-9]+|[0-9]+[.])([+-]+)?', expr[::-1])

        if not number or number.start() != 0:
            raise Exception(
                "the expression should be written in the following form 'number operator number'")

        return number

    def search_simple_number(self, expr):
        number = re.search(r'(([0-9]*[.])?[0-9]+|[0-9]+[.])', expr[::-1])
        return number
