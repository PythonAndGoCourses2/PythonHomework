import argparse
import config as c


def create_parser():
    """Created with argparse lib. Has 'help' parameter for --help"""
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator")
    parser.add_argument('EXPRESSION', help="expression string to evaluate")
    return parser


def calc_logic(formula):
    """Main solving function"""
    fst_formula, sec_formula, sign = comparisons_check(formula)
    fst_formula = dividing_to_symbols(formula)
    function_check(fst_formula)
    nums_check(fst_formula)
    constants_check(fst_formula)

    unar_operations(fst_formula)
    sign_check(fst_formula)
    operands_check(fst_formula)
    errors_check(fst_formula)
    seperated_formula = polish_check(fst_formula)
    fnl_result1 = count_result(seperated_formula)
    if sec_formula:
        sec_formula = dividing_to_symbols(formula)
        function_check(sec_formula)
        nums_check(sec_formula)
        constants_check(sec_formula)
        unar_operations(sec_formula)
        sign_check(sec_formula)
        operands_check(sec_formula)
        errors_check(sec_formula)
        seperated_formula = polish_check(sec_formula)
        fnl_result2 = count_result(seperated_formula)
        fnl_result1 = compare(fnl_result1, fnl_result2, sign)

    return fnl_result1


def is_function(formula):
    """"""
    counter = 1
    for idx, value in enumerate(formula):
        if str(value) in c.function or str(value)[1:] in c.function:
            formula = formula[idx+1:]
            return counter, formula
        elif value == ",":
            counter += 1


def comparisons_check(lst_of_syms):
    """Checks the availability of comparisons"""
    fst_formula, sec_formula = '', ''
    sign = ''
    for idx, sym in enumerate(lst_of_syms):
        if sym in c.comparison:
            sign += sym
            if idx == 0 or idx == -1:
                raise SyntaxError("ERROR: Incorrect expression")
            elif lst_of_syms[idx+1] in c.comparison:
                sign += lst_of_syms[idx+1]
                lst_of_syms[idx] += lst_of_syms[idx+1]
                lst_of_syms.pop(idx+1)
                fst_formula, sec_formula = lst_of_syms[:idx], lst_of_syms[idx+1:]
                break
            else:
                if lst_of_syms[idx+2] in c.comparison:
                    raise SyntaxError("ERROR: Incorrect expression")
        else:
            fst_formula = lst_of_syms
            sec_formula = ''

    return fst_formula, sec_formula, sign


def compare(fst_form, sec_form, sym):
    """"""
    comparison = {'>': fst_form > sec_form,
                  '<': fst_form < sec_form,
                  '>=': fst_form >= sec_form,
                  '<=': fst_form <= sec_form,
                  '==': fst_form == sec_form,
                  '!=': fst_form != sec_form
                  }
    return comparison[sym]


def sign_check(formula):
    """Convert positive number to negative if there is a '-' before the nums"""
    idx = 0
    while idx != len(formula):
        if (type(formula[idx]) != str or formula[idx] in c.function) and formula[idx-1] == "-" and \
            ((idx-1) == 0 or (formula[idx-2] in c.operands and formula[idx-2] not in "+-") or formula[idx-2] == "("):
            if type(formula[idx]) == str:
                formula[idx] = "-" + formula[idx]
            else:
                formula[idx] *= -1
            formula.pop(idx - 1)
            idx -= 1
            continue
        idx += 1


def function_check(formula):
    """Search for functions"""
    idx = len(formula)-1
    tmp_func = ""
    while idx > -1:
        if formula[idx] == "(":
            idx -= 1
            while formula[idx] not in "()" and (formula[idx] not in c.operands):
                tmp_func += formula[idx]

                if tmp_func[::-1] in c.function and tmp_func[::-1] not in c.constants:
                    index = 1
                    while formula[idx+index] != "(":
                        formula[idx] += formula[idx+index]
                        formula.pop(idx + index)

                    if idx == 0:
                        break
                idx -= 1
            else:
                if tmp_func[::-1] not in c.function:
                    raise SyntaxError("ERROR: Unknown expression")
                tmp_func = ""
        else:
            idx -= 1



def constants_check(formula):
    """"""
    idx = 0
    tmp_func = ""
    while idx != len(formula):
        tmp_index = idx
        while str(formula[idx]) not in c.function and str(formula[idx]) not in "()" and str(formula[idx]).isalpha():
            tmp_func += formula[idx]
            if tmp_func in c.constants:
                formula[tmp_index] = tmp_func
                while idx != tmp_index:
                    formula.pop(idx)
                    idx -= 1


                formula[idx] = c.constants[formula[idx]]
                tmp_func = ""

            if idx != len(formula)-1:
                idx += 1
            else:
                break
        else:
            idx += 1
    else:
        if tmp_func in c.function:
            raise SyntaxError("ERROR: Incorrect expression")

def nums_check(formula):
    """"""
    idx = 0
    tmp_nums = ""
    while idx != len(formula):
        if (formula[idx].isdigit() or formula[idx] == "."):
            if idx == len(formula) - 1:
                if tmp_nums:
                    tmp_nums += formula.pop()
                    if "." in tmp_nums:
                        formula[idx - 1] = float(tmp_nums)
                    else:
                        formula[idx - 1] = int(tmp_nums)
                    break
                else:
                    tmp_nums = formula[idx]
                    if "." in tmp_nums:
                        formula[idx] = float(tmp_nums)
                    else:
                        formula[idx] = int(tmp_nums)
                break

            if not tmp_nums:
                tmp_nums = formula[idx]
                idx += 1
            else:
                tmp_nums += formula.pop(idx)
                continue
        else:
            if tmp_nums:

                if "." in tmp_nums:
                    formula[idx-1] = float(tmp_nums)
                else:
                    formula[idx-1] = int(tmp_nums)
                tmp_nums = ""
            idx += 1


def operands_check(formula):
    """"""
    for idx, value in enumerate(formula):
        if value == "/" and formula[idx-1] == "/":
            formula[idx-1] += formula.pop(idx)


def dividing_to_symbols(string):
    """Divides all string to symbols"""
    lst_of_syms = []


    for idx, sym in enumerate(string):
        if sym == " ":
            if string[idx+1] == string[idx-1] and lst_of_syms[-1] not in '+- ':
                raise SyntaxError("ERROR: extra space")
            elif string[idx+1].isdigit() and string[idx-1].isdigit():
                raise SyntaxError("ERROR: Incorrect expression")
            continue

        lst_of_syms.append(sym)

    return lst_of_syms


def unar_operations(formula):
    """Convert nums depending on the operand before it(+ or -)"""
    index = 0
    while index != len(formula) - 1:
        if str(formula[index]) in "+-" and str(formula[index + 1]) in "+-":
            while str(formula[index + 1]) in "+-":
                if formula[index + 1] == '-' and formula[index] == '-':
                    formula[index + 1] = '+'
                elif formula[index + 1] == '-' and formula[index] == '+':
                    formula[index + 1] = '-'
                else:
                    formula[index + 1] = formula[index]

                formula.pop(index)

        else:
            index += 1

    return formula


def polish_check(formula):
    """Removes all the brackets and set the priority """
    nums = []
    operands = []

    for index, element in enumerate(formula):
        if type(element) != str:
            nums.append(element)
        else:
            if not operands:
                operands.append(element)
            elif (operands[-1] in "*//%" and element in "+-") or (operands[-1] in "*//%" and element in "*//%") or \
                (operands[-1] in "^" and element in "+-//%*") or ((operands[-1] in c.function) and element in "*//%+-"):
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
                        if operands:
                            if operands[-1] in c.function or operands[-1][1:] in c.function:
                                nums.append(operands.pop())
                            break
            elif element == ",":
                while operands[-1] != "(":
                    nums.append(operands.pop())
                operands.append(element)

            else:
                operands.append(element)


        if index == len(formula) - 1:
            nums.extend(operands[::-1])
        if len(operands) > 1:
            if element in c.operands and operands[-2] in c.operands:
                if element == "^" and operands[-2] == "^":
                    continue
                elif c.priorities[operands[-1]] <= c.priorities[operands[-2]]:
                    nums.append(operands.pop(-2))


    return nums


def count_result(formula):
    fst_elem = 0
    sec_elem = 0
    lst_for_result = []
    tmp_formula = formula[:]

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
                result = c.operands[element](fst_elem, sec_elem)
                lst_for_result.pop()
                lst_for_result[-1] = result
            elif element == ",":
                continue
            elif element in c.function or element[1:] in c.function:
                try:
                    result = c.function[element]
                    tmp_sign = "+"
                except:
                    result = c.function[element[1:]]
                    tmp_sign = "-"
                tmp_params, tmp_formula = is_function(tmp_formula)
                if tmp_params == 1:
                    try:
                        lst_for_result[-1] = result(lst_for_result[-1])
                        if tmp_sign == "-":
                            lst_for_result[-1] *= -1
                    except:
                        raise AttributeError("ERROR: Wrong number of parametrs in '{}' function".format(element))
                elif tmp_params == 2:
                    try:
                        lst_for_result[-2] = result(fst_elem, sec_elem)
                        if tmp_sign == "-":
                            lst_for_result[-2] *= -1
                        lst_for_result.pop()
                    except:
                        raise AttributeError("ERROR: Wrong number of parametrs in '{}' function".format(element))
                else:
                    raise AttributeError("ERROR: Wrong number of parametrs in '{}' function".format(element))

            if not index == len(formula) - 1:
                if 0 == len(lst_for_result)-1:
                    fst_elem = lst_for_result[-1]
                else:
                    fst_elem = lst_for_result[-2]
                    sec_elem = lst_for_result[-1]


    return lst_for_result[-1]


def errors_check(formula):
    """"""
    open_bracks = 0
    closed_bracks = 0
    is_num = False
    for idx, val in enumerate(formula):
        if val in c.function and formula[idx+1] != "(":
            raise SyntaxError("ERROR: Need bracket before '{}'".format(val))
        if formula[-1] in c.operands:
            raise SyntaxError("ERROR: Incorrect expression")
        if val in c.constants or type(val) == float or type(val) == int:
            is_num = True
        if val == "(":
            if formula[idx+1] == ")":
                raise SyntaxError("ERROR: Empty brackets")
            open_bracks += 1
        elif val == ")":
            closed_bracks += 1
    if not is_num:
        raise SyntaxError("ERROR: Need nums")
    elif open_bracks != closed_bracks:
        raise SyntaxError("ERROR: Brackets are not balanced")

def main():
    parser = create_parser()
    args = parser.parse_args()
    formula = args.EXPRESSION
    if not formula:
        raise SyntaxError("ERROR: Formula is empty")
    elif formula.isdigit() or formula in c.operands:
        raise SyntaxError("ERROR: Incorrect function")
    print(calc_logic(formula))


if __name__ == '__main__':
    main()

    
