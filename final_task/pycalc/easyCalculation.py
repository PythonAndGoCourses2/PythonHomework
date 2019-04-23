import re
import pycalc.operators as operators


class Calculator():

    def __calculation(self, expr):
        place = expr.rfind("^")

        while place != -1:

            expr = self.__binary_operation(place, expr)
            place = expr.rfind("^")

        place = re.search(r'/|\*|%|&', expr)

        while place is not None:

            expr = self.__binary_operation(place, expr)
            place = re.search(r'/|\*|%|&', expr)
            # добавить сравнение после суммы
        return self.__sum(expr)

    def __sum(self, expr):

        if expr[-1] == "+" or expr[-1] == "-":
            raise Exception("'+' or '-'mustn' be the last even in brackets")

        summing = 0
        number = 0
        while expr != "":
            find = re.search(r'[0-9]+([.][0-9]*)?|[.][0-9]+', expr)
            number = expr[:find.end()]
            if number.count("-") % 2 == 1:
                a = float("-" + find[0])
            else:
                a = float(find[0])
            expr = expr[find.end():]
            summing += a
        return '{:.15f}'.format(summing)

    def calculate(self, expr):
        expr = expr.replace(" ", "")
        # посмотреть где выскакивает лишний " "
        while "(" in expr:

            end = expr.find(")")
            if end != len(expr) - \
                    1 and expr[end + 1] not in operators.operators:
                Exception("no operator after brackets")

            begin = expr[:end].rfind("(")

            if begin != 0 and expr[begin - 1] not in operators.operators \
                    and expr[begin - 1] != '-' and expr[begin - 1] != '+':
                raise Exception("no operators before brackets")

            rezult = self.__calculation(expr[begin + 1:end])
            expr = expr[:begin] + str(rezult) + expr[end + 1:]

        rezult = self.__calculation(expr)

        return rezult

    def __binary_operation(self, place, expr):
        findBefore = re.search(
            r'[0-9]+([.][0-9]*)?|[.][0-9]+', expr[place::-1])
        findAfter = re.search(
            r'[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)', expr[place:])

        if findAfter is None or findAfter.start(
        ) != 1 or findBefore is None or findBefore.start() != 1:
            raise Exception(
                "the expression should be written in the following form 'number operator number'")

        rezult = '{:.15f}'.format(operators.operators[expr[place]](
            float(findBefore[0][::-1]), float(findAfter[0])))
        begin = expr[:place - len(findBefore[0])]
        expr = begin + rezult + expr[findAfter.end() + place:]
        return expr
