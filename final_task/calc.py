import argparse
import math

def create_parser():
    """Created with argparse lib. Has 'help' parameter for --help"""
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator")
    parser.add_argument('EXPRESSION', help="expression string to evaluate")
    return parser
def math_data_cheacker(formula):
    """Convert string to math date if needed"""
    for index, element in enumerate(formula):
        if str(element) in "epitau":#in math lib we got 'e, pi, tau'
            formula[index] = getattr(math, element)
def function_exist(formula):
    """"""
    for index, element in enumerate(formula):
        if not (str(element) in dir(math) or str(element) in "absround()" or str(element) in "+-//^*%>=<=!==" or
        type(element) == int or type(element) == float):
            raise NameError("ERROR: Unknown function '{}'".format(element))
def errors_check(formula):
    """The exit is made by 'raise SystemExit'"""
    opened_breacket_counter = 0
    closed_breacket_counter = 0

    for index, element in enumerate(formula):
        if element == "(":
            opened_breacket_counter += 1
        elif element == ")":
            closed_breacket_counter += 1
        elif formula[index-1] == "/" and element == "0":
            raise ZeroDivisionError("ERROR: Division by zero")
        elif (str(element) in "+-*//^%" and formula[index-1] in "+-*//^%") and not (element == "/" and
                                                                                formula[index-1] == "/"):
            raise SyntaxError("ERROR: you have two operands staying together")

    if opened_breacket_counter != closed_breacket_counter:
        raise SyntaxError("ERROR: brackets are not balanced")
def solution(symbol, fst_num, sec_num):
    """Simple function that operates all the needed operands"""
    operands = {'+': fst_num + sec_num,
                '-': fst_num - sec_num,
                '/': fst_num / sec_num,
                '//': fst_num // sec_num,
                '*': fst_num * sec_num,
                '%': fst_num % sec_num,
                '^': fst_num ** sec_num,
                '>': fst_num > sec_num,
                '>=': fst_num >= sec_num,
                '<': fst_num < sec_num,
                '<=': fst_num <= sec_num,
                '==': fst_num == sec_num,
                '!=': fst_num != sec_num,
                }
    return operands[symbol]
def choosing_the_solution(formula):
    """As calculator should compare values(>, <, !=, etc) we need to know: do we have comparison or not"""
    for index, element in enumerate(formula):
        if element in ">=<=!==":
            seperated_formula_1 = seperating_main_string(formula[:index])
            seperated_formula_2 = seperating_main_string(formula[index:])

            final_formula_1 = polish_check(seperated_formula_1)
            final_formula_2 = polish_check(seperated_formula_2)

            result_1 = count_result(final_formula_1)
            result_2 = count_result(final_formula_2)

            final_result = solution(seperated_formula_2[0], result_1, result_2)
            return final_result

    nums = []
    operands = []

    seperated_formula = seperating_main_string(formula)
    final_formula = polish_check(seperated_formula)
    final_result = count_result(final_formula)
    return final_result
def seperating_main_string(formula):
    """Seperating elements of main string to int; float; keywords like abs, round; math functions; etc"""
    sep_formula = []
    tmp_number = ''
    tmp_symbol = ''

    errors_check(formula)

    for index, symbol in enumerate(formula):
        if symbol.isdigit() or symbol == '.' or (symbol == '-' and formula[index+1].isdigit()):
            tmp_number += symbol

            if index == len(formula) - 1:
                if '.' in tmp_number:
                    sep_formula.append(float(tmp_number))
                else:
                    sep_formula.append(int(tmp_number))
                break

            if not (formula[index + 1].isdigit() or formula[index + 1] == '.'):
                if '.' in tmp_number:
                    sep_formula.append(float(tmp_number))
                else:
                    sep_formula.append(int(tmp_number))
                tmp_number = ''
        else:
            if symbol == '(' or symbol == ')':
                sep_formula.append(symbol)
                continue
            elif symbol in "+-*%^/":
                if symbol == "/" and formula[index+1] == "/":
                    sep_formula.append("//")
                    continue
                elif sep_formula[-1] == "//" and symbol == "/":
                    continue
                sep_formula.append(symbol)
                continue
            elif symbol == ',':
                continue

            tmp_symbol += symbol

            if index == len(formula) - 1:
                sep_formula.append(tmp_symbol)
                break

            if formula[index + 1].isdigit() or \
                    formula[index + 1] == '.' or \
                    formula[index + 1] == '(' or \
                    formula[index + 1] == ')' or \
                    (tmp_symbol in "e pi tau" and formula[index + 1] in "+-//%*><!="):

                sep_formula.append(tmp_symbol)
                tmp_symbol = ''

    function_exist(sep_formula)
    math_data_cheacker(sep_formula)

    return sep_formula
def polish_check(formula):
    """Removes all the breckets and set the priority """
    nums = []
    operands = []
    for index, element in enumerate(formula):
        if type(element) == int or type(element) == float:
            nums.append(element)
        else:
            if not operands:
                operands.append(element)
            elif (operands[-1] in "*//%" and element in "+-") or (operands[-1] in "*//%" and element in "*//%") or \
                    (operands[-1] in "^" and element in "+-//%*") or \
                    ((operands[-1] in dir(math) or operands[-1] == "abs" or operands[-1] == "round") and element in "*//%+-"):
                nums.append(operands.pop())
                operands.append(element)
            elif element == ")":
                tmp_operands = []
                for i, value in reversed(list(enumerate(operands))):
                    if value == "(":
                        tmp_operands.extend(operands[:i])
                        operands = operands[i+1:]
                        nums.extend(operands[::-1])
                        operands = tmp_operands
                        break
            else:
                operands.append(element)

        if index == len(formula) - 1:
            nums.extend(operands[::-1])

    return nums
def count_result(formula):
    """Takes list without brackets and count the result"""
    fst_elem = 0
    sec_elem = 0
    lst_for_result = []

    for index, element in enumerate(formula):
        if type(element) == int or type(element) == float:
            if not fst_elem:
                fst_elem = element
            else:
                lst_for_result.append(element)
                fst_elem = lst_for_result[-2]
                sec_elem = lst_for_result[-1]
                continue
            lst_for_result.append(element)
            continue
        else:
            if element in "+-*//%^":
                result = solution(element, fst_elem, sec_elem)
                lst_for_result.pop()
                lst_for_result[-1] = result
            elif element == "frexp":
                try:
                    result = getattr(math, element)(float(fst_elem), int(sec_elem))
                    lst_for_result.pop()
                    lst_for_result[-1] = result
                except:
                    raise TypeError("ERROR: parametr should be pair (m, e)")

            elif element in dir(math):
                try:
                    result = getattr(math, element)(fst_elem, sec_elem)
                    lst_for_result.pop()
                    lst_for_result[-1] = result
                except ValueError:
                    print("ERROR: out of func domain")
                except:
                    lst_for_result[-1] = getattr(math, element)(fst_elem)

            elif element in "abs":
                lst_for_result[-1] = abs(lst_for_result[-1])
            elif element in "round":
                lst_for_result[-1] = round(lst_for_result[-1])

            if not index == len(formula) - 1:
                if 0 == len(lst_for_result)-1:
                    fst_elem = lst_for_result[-1]
                else:
                    fst_elem = lst_for_result[-2]
                    sec_elem = lst_for_result[-1]
    return lst_for_result[-1]

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    formula = args.EXPRESSION

    final_result = choosing_the_solution(formula)

    print(final_result)