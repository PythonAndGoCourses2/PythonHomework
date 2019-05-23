"""Calculate string expression, input from command-line interface."""
import argparse
import math
import re

from collections import namedtuple


class InternalError(Exception):
    pass


math_functions = [getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))]
math_train = ['frexp', 'modf']
arith = namedtuple("arith", ("priority", "function"))
add = arith(1, lambda x, y: x + y)
sub = arith(1, lambda x, y: x - y)
div = arith(2, lambda x, y: x / y)
mul = arith(2, lambda x, y: x * y)
floordiv = arith(3, lambda x, y: x // y)
mod = arith(3, lambda x, y: x % y)
poww = arith(4, lambda x, y: x ** y)

comparis = namedtuple("comparis", "function")
lt = comparis(lambda x, y: x < y)
le = comparis(lambda x, y: x <= y)
eq = comparis(lambda x, y: x == y)
ne = comparis(lambda x, y: x != y)
ge = comparis(lambda x, y: x >= y)
gt = comparis(lambda x, y: x > y)

brackets = namedtuple("brackets", "count")
br = brackets(1)

ops_comparison = {
    "<=": le,
    "==": eq,
    "!=": ne,
    ">=": ge,
    ">": gt,
    "<": lt,
}
ops_calculation = {
    "+": add,
    "-": sub,
    "/": div,
    "*": mul,
    "//": floordiv,
    "%": mod,
    "^": poww,
    "(": br,
    ")": br
}


def brackets_count(expression):
    """Find quantity of brackets in expression.

    :return: expression.
    :raise: IndexError, TypeError.

    """

    try:
        brackets_amount = 0
        for element in expression:
            if element == '(':
                brackets_amount += 1
            elif element == ')':
                brackets_amount -= 1
        if brackets_amount == 0:
            return expression
        else:
            raise TypeError('not the correct quantity of brackets')
    except IndexError as e:
        print('ERROR: ', e)
        raise InternalError
    except TypeError as e:
        print('ERROR: ', e)
        raise InternalError


def transformathion_stack_expr(expression):
    """Convert the input expression into a list.

    :param: expression.
    :return: list with numbers ready for calculation and simple operations.

    """

    stack = []
    input_value = list(expression)
    if len(input_value) > 1:
        number = ''
        for index, element in enumerate(input_value):
            if len(input_value) == index + 1:
                number += input_value[index]
                stack.append(number)
                break
            if element == '(' and input_value[index + 1] == '-':
                stack.append(element)
                number += input_value[index + 1]
            elif element in set('0123456789.') and input_value[index + 1] in set('0123456789.'):
                number += element
            elif element in set('0123456789.') and input_value[index + 1] not in set('0123456789.'):
                number += element
                stack.append(number)
                stack.append(input_value[index + 1])
                number = ''
            elif element == ')' and input_value[index + 1] in ops_calculation:
                stack.append(input_value[index + 1])
    if input_value[0] == '-':
        number_negative = input_value[0] + stack[0]
        stack = stack[1:]
        stack.insert(0, number_negative)
    return stack


def replacement_signs(transformathion_stack_str):
    """Change characters in expression."""
    transformathion_stack_str = transformathion_stack_str.replace('--', '+')
    transformathion_stack_str = transformathion_stack_str.replace('-+', '-')
    transformathion_stack_str = transformathion_stack_str.replace('++', '+')
    transformathion_stack_str = transformathion_stack_str.replace('+-', '-')
    return transformathion_stack_str


def replacement_cleaning(expression_in_brackets_str, tr_stack, stack_number, stack_close_brackets, place):
    """Replacing a bracket expression with a number obtained by calculating this expression."""
    expression_in_brackets_str = ''.join(expression_in_brackets_str)
    transformathion_stack_str = ''.join(tr_stack)
    stack_number_str = ''.join(stack_number)
    transformathion_stack_str = transformathion_stack_str.replace(expression_in_brackets_str,
                                                                  stack_number_str)
    transformathion_stack_str = replacement_signs(transformathion_stack_str)
    stack_close_brackets.clear()
    place.clear()
    return transformathion_stack_str


def account(stack_operathion, stack_number):
    """Perform calculation operations on numbers."""
    try:
        operation = stack_operathion.pop()
        number_2 = stack_number.pop()
        number_1 = stack_number.pop()
        result = str(ops_calculation[operation].function(float(number_1), float(number_2)))
        return result
    except ZeroDivisionError as e:
        print('ERROR: ', e)
        raise InternalError
    except IndexError as e:
        print('ERROR: ', e)
        raise InternalError
    except ValueError as e:
        print('ERROR: ', e)
        raise InternalError


def calculate_expr(transformathion_stack_expr):
    """Calculating an expression consisting of numbers and simple operations."""
    stack_number = []
    stack_operathion = []
    if len(transformathion_stack_expr) == 1:
        return transformathion_stack_expr[0]
    else:
        for index, element in enumerate(transformathion_stack_expr):
            if len(transformathion_stack_expr) == index + 1:
                stack_number.append(element)
                if len(stack_operathion) == 1:
                    stack_number.append(account(stack_operathion, stack_number))
                else:
                    stack_number.append(account(stack_operathion, stack_number))
                    if len(stack_operathion) == 1:
                        stack_number.append(account(stack_operathion, stack_number))
            else:
                if element not in ops_calculation:
                    stack_number.append(element)
                elif element in ops_calculation:
                    if len(stack_operathion) == 0:
                        stack_operathion.append(element)
                    elif len(stack_operathion) >= 1:
                        if ops_calculation[element].priority > ops_calculation[stack_operathion[-1]].priority:
                            stack_operathion.append(element)
                        elif ops_calculation[element].priority <= ops_calculation[stack_operathion[-1]].priority:
                            stack_number.append(account(stack_operathion, stack_number))
                            stack_operathion.append(element)
        try:
            return stack_number[0]
        except IndexError as e:
            print('ERROR: ', e)
            raise InternalError


def pi_e(stack_math):
    """Replacing pi and e with numbers."""
    pi_math = getattr(math, 'pi')
    e_math = getattr(math, 'e')
    for index, element in enumerate(stack_math):
        if stack_math[index] == 'pi':
            stack_math[index] = str(pi_math)
        elif stack_math[index] == 'e':
            stack_math[index] = str(e_math)
    return stack_math


def subfinder(mylist, pattern) -> list:
    """Used to replace multiple items with one."""
    pattern_size = len(pattern)
    for index, element in enumerate(mylist):
        if mylist[index: index + pattern_size] == pattern:
            mylist = subfinder(mylist[:index] + [''.join(pattern)] + mylist[index + pattern_size:], pattern)
    return mylist


def stack_math_with_number(stack):
    """Used to replace multiple items from the math module with one."""
    stack_new = stack.copy()
    list_math_with_number = []
    for element in dir(math)[6:]:
        if element.isalpha() == False:
            list_math_with_number.append(element)
    list_split_math = []
    for element_math in list_math_with_number:
        try:
            r = re.compile("([a-zA-Z]+)([0-9]+)")
            math_func_split = r.match(element_math).groups()
            list_split_math.append(math_func_split)
        except Exception:
            r = re.compile("([a-zA-Z]+)([0-9]+)([a-zA-Z]+)")
            math_func_split = r.match(element_math).groups()
            list_split_math.append(math_func_split)

    for element in list_split_math:
        stack_new = subfinder(stack_new, list(element))
    return stack_new


def transformathion_stack(expression):
    """Convert the input expression into a list.

        :param: expression.
        :return: the list with the numbers ready for calculation and with
        operations as simple and with functions from the math module.

    """
    dicthionary = list(map(chr, range(97, 123)))
    stack = []
    input_value = list(expression)
    if len(input_value) > 1:
        number = ''
        math_ops = ''
        for index, element in enumerate(input_value):
            if len(input_value) == index + 1:
                if input_value[index] in set('0123456789)'):
                    number += input_value[index]
                    stack.append(number)
                    break
                elif input_value[index] in dicthionary:
                    math_ops += input_value[index]
                    stack.append(math_ops)
                    break
            elif element in ops_calculation:
                if element == '-' and input_value[index - 1] == '(' and input_value[index + 1] in set('0123456789.'):
                    number += element
                else:
                    stack.append(element)
            elif element in set('0123456789.') and input_value[index + 1] in set('0123456789.'):
                number += element
            elif element in set('0123456789.') and input_value[index + 1] not in set('0123456789.'):
                number += element
                stack.append(number)
                number = ''
            elif element in dicthionary and input_value[index + 1] in dicthionary:
                math_ops += element
            elif element in dicthionary and input_value[index + 1] not in dicthionary:
                math_ops += element
                stack.append(math_ops)
                math_ops = ''
            elif element == ',':
                stack.append(element)
            else:
                stack.append(element)
    elif len(input_value) == 1:
        if expression.isdigit() == True or expression == 'e':
            stack.append(expression)
        else:
            print('ERROR: not the correct value is entered 11')
            raise InternalError
    if len(stack) == 1:
        if stack[0].isalpha() == True:
            if stack[0] == 'pi' or stack[0] == 'e':
                pass
            else:
                print('ERROR: not the correct value is entered')
                raise InternalError

    try:
        if input_value[0] == '-' and input_value[1] in set('0123456789'):
            number_negative = input_value[0] + stack[1]
            stack = stack[2:]
            stack.insert(0, number_negative)
    except IndexError:
        print('ERROR: not the correct value is entered1')
        raise InternalError
    if 'pi' in stack or 'e' in stack:
        pi_e(stack)
    if len(stack) > 1:
        stack = stack_math_with_number(stack)
    return stack


def round_not_math(expression_in_brackets, tr_stack, place, stack_close_brackets, transformathion_stack_str_to_list):
    """Function for rounding of numbers."""
    number_round_finall = ''
    if ',' in expression_in_brackets:
        whole_expression = ''.join(expression_in_brackets)
        whole_expression_split_comma = whole_expression.split(',')
        expression_to_comma = whole_expression_split_comma[0]
        expression_after_comma = whole_expression_split_comma[1]
        one_value_to_comma = calculate_expr(transformathion_stack_expr(expression_to_comma))
        if '.' not in expression_after_comma and len(expression_after_comma) == 1:
            two_value_after_comma = int(expression_after_comma)
        else:
            two_value_after_comma = int(
                float(calculate_expr(transformathion_stack_expr(expression_after_comma))))
        one_value_to_comma_split = one_value_to_comma.split('.')
        if two_value_after_comma > 0:
            number_fixed = one_value_to_comma[:len(one_value_to_comma_split[0]) + two_value_after_comma + 1]
            if int(one_value_to_comma[len(number_fixed)]) >= 5:
                number_round_end = int(one_value_to_comma[len(number_fixed) - 1]) + 1
                number_round = number_fixed[:-1] + str(number_round_end)
                number_round_finall += number_round

            elif int(one_value_to_comma[len(number_fixed)]) < 5:
                number_round = number_fixed
                number_round_finall += number_round
        else:
            number_fixed = one_value_to_comma[:len(one_value_to_comma_split[0]) + two_value_after_comma]
            number_discard = one_value_to_comma_split[0][len(number_fixed):]
            number_null = number_discard.translate('0' * 256)
            if int(number_discard[0]) >= 5:
                number_round_end = int(number_fixed[-1]) + 1
                number_round = number_fixed[:-1] + str(number_round_end) + number_null
                number_round_finall += number_round
            elif int(number_discard[0]) < 5:
                number_round = number_fixed + number_null
                number_round_finall += number_round

    elif ',' not in expression_in_brackets:
        number_brack = calculate_expr(expression_in_brackets)
        if '.' in number_brack:
            number_brack_split = number_brack.split('.')
            if int(number_brack_split[1][0]) >= 5:
                number_fixed_end = int(number_brack_split[0][-1]) + 1
                number_round = number_brack_split[0][:-1] + str(number_fixed_end)
                number_round_finall += number_round
            elif int(number_brack_split[1][0]) < 5:
                number_round = number_brack_split[0]
                number_round_finall += number_round
        else:
            number_round = number_brack
            number_round_finall += number_round

    expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
    transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                              number_round_finall, stack_close_brackets,
                                                              place)
    return transformathion_stack_str_to_list


def math_fsum(expression_in_brackets, attr_st, tr_stack, place, stack_close_brackets,
              transformathion_stack_str_to_list):
    """Calculation of the fsum function from the math module."""
    if ',' in expression_in_brackets:
        sequence_number_list = expression_in_brackets[1:-1]
        sequence_number_str = ''.join(sequence_number_list)
        split_sequence_number_list = sequence_number_str.split(',')
        number_tuple = []
        for index, element in enumerate(split_sequence_number_list):
            if element.isdigit():
                number_tuple.append(element)
            else:
                element_fsum = calculate_expr(transformathion_stack_expr(element))
                number_tuple.append(element_fsum)
        list_number_float_fsum = []
        for element in number_tuple:
            list_number_float_fsum.append(float(element))
        tuple_number_fsum = tuple(list_number_float_fsum)
        number_with_math = str(getattr(math, attr_st)(tuple_number_fsum))
        expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
        transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                  number_with_math,
                                                                  stack_close_brackets,
                                                                  place)
    elif ',' not in expression_in_brackets:
        number_list = expression_in_brackets[1:-1]
        list_num = []
        if len(number_list) == 1:
            list_num.append(float(number_list[0]))
        elif len(number_list) > 1:
            fsum_number_str = calculate_expr(transformathion_stack_expr(number_list))
            list_num.append(float(fsum_number_str))
        fsum_number_tuple = tuple(list_num)
        number_with_math = str(getattr(math, attr_st)(fsum_number_tuple))
        expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
        transformathion_stack_str_to_list += replacement_cleaning(
            expression_in_brackets_str, tr_stack, number_with_math, stack_close_brackets, place)
    return transformathion_stack_str_to_list


def check_in_math(attr_st):
    """Check on entry of an element into the math module."""
    try:
        return getattr(math, attr_st) in math_functions
    except AttributeError:
        print('ERROR: function from the math module is incorrectly entered')
        raise InternalError


def calculate_brack(mylist_stack):
    """Calculation of expressions in brackets and functions from the math library."""
    tr_stack = mylist_stack.copy()
    while ')' in tr_stack:
        stack_close_brackets = []
        place = []
        for index_cl, element_cl in enumerate(tr_stack):
            if element_cl == ')':
                stack_close_brackets.append(index_cl)
        transformathion_stack_pl = tr_stack[:stack_close_brackets[0]]
        for index_pl, element_pl in enumerate(transformathion_stack_pl):
            if element_pl == '(':
                place.append(index_pl)
        expression_in_brackets = tr_stack[place[-1] + 1:stack_close_brackets[0]]
        attr_st = tr_stack[int(place[-1] - 1)]
        transformathion_stack_str_to_list = ''

        if attr_st in ops_calculation:
            stack_number = calculate_expr(expression_in_brackets)
            expression_in_brackets_str = tr_stack[place[-1]:stack_close_brackets[0] + 1]
            transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                      stack_number, stack_close_brackets, place)
        elif attr_st == 'fsum':
            try:
                transformathion_stack_str_to_list += math_fsum(expression_in_brackets, attr_st, tr_stack, place,
                                                               stack_close_brackets,
                                                               transformathion_stack_str_to_list)
            except IndexError:
                print('ERROR: the sequence is incorrectly entered')
                raise InternalError
        elif attr_st == 'abs':
            abs_number_str = calculate_expr(expression_in_brackets)
            if abs_number_str[0] == '-':
                new_abs_number_str = str(abs_number_str[1:])
                expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
                transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                          new_abs_number_str, stack_close_brackets,
                                                                          place)
            else:
                expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
                transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                          abs_number_str, stack_close_brackets,
                                                                          place)
        elif attr_st == 'round':

            transformathion_stack_str_to_list += round_not_math(expression_in_brackets, tr_stack, place,
                                                                stack_close_brackets, transformathion_stack_str_to_list)
        elif ',' in expression_in_brackets and getattr(math,
                                                       attr_st) in math_functions and attr_st != 'fsum':
            if len(expression_in_brackets) == 3:
                number_with_math = str(getattr(math, attr_st)(float(expression_in_brackets[0]),
                                                              float(expression_in_brackets[2])))

                expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
                transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                          number_with_math, stack_close_brackets,
                                                                          place)
            elif len(expression_in_brackets) > 3:
                whole_expression = ''.join(expression_in_brackets)
                whole_expression_split_comma = whole_expression.split(',')
                expression_to_comma = whole_expression_split_comma[0]
                expression_after_comma = whole_expression_split_comma[1]
                one_value_to_comma = calculate_expr(transformathion_stack_expr(expression_to_comma))
                two_value_after_comma = calculate_expr(transformathion_stack_expr(expression_after_comma))

                number_with_math = str(getattr(math, attr_st)(float(one_value_to_comma), float(two_value_after_comma)))

                expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
                transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                          number_with_math, stack_close_brackets,
                                                                          place)
        elif attr_st in math_train:
            try:
                stack_number_str = calculate_expr(expression_in_brackets)
                number_train = getattr(math, attr_st)(float(stack_number_str))
                if attr_st == 'frexp':
                    print('If the calculation will be carried out on the mantissa,'
                          ' enter 0, by the exponent of the number, enter 1:')
                    mant_exp = input()
                    if mant_exp == '0':
                        number_on_exit = str(number_train[0])
                        expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
                        transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                                  number_on_exit,
                                                                                  stack_close_brackets,
                                                                                  place)
                    elif mant_exp == '1':
                        number_on_exit = str(number_train[1])
                        expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
                        transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                                  number_on_exit,
                                                                                  stack_close_brackets,
                                                                                  place)
                    else:
                        print('You entered a wrong number')

                elif attr_st == 'modf':
                    print('If the calculation will be carried out on the fractional part,'
                          ' enter 0, for the whole part, enter 1:')
                    mant_exp = input()
                    if mant_exp == '0':
                        number_on_exit = str(number_train[0])
                        expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
                        transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                                  number_on_exit,
                                                                                  stack_close_brackets,
                                                                                  place)
                    elif mant_exp == '1':
                        number_on_exit = str(number_train[1])
                        expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
                        transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                                  number_on_exit,
                                                                                  stack_close_brackets,
                                                                                  place)
                    else:
                        print('You entered a wrong number')
            except ValueError as e:
                print('ERROR: ', e)
                raise InternalError

        elif check_in_math(attr_st):
            stack_number_str = calculate_expr(expression_in_brackets)
            number_float = str(getattr(math, attr_st)(float(stack_number_str)))
            expression_in_brackets_str = tr_stack[place[-1] - 1:stack_close_brackets[0] + 1]
            transformathion_stack_str_to_list += replacement_cleaning(expression_in_brackets_str, tr_stack,
                                                                      number_float,
                                                                      stack_close_brackets,
                                                                      place)
        tr_stack = transformathion_stack(transformathion_stack_str_to_list)
        if ')' in tr_stack:
            continue
        else:
            tr_stack_str = ''.join(tr_stack)
            tr_stack_str = replacement_signs(tr_stack_str)
            tr_stack = transformathion_stack(tr_stack_str)
            return tr_stack


def calculate(calculate_brackets):
    """Calculation of expression after conversion
    of brackets and functions from the math module."""
    calculate_brackets = ''.join(calculate_brackets)
    calculate_brackets = replacement_signs(calculate_brackets)
    stack_number = calculate_expr(transformathion_stack(calculate_brackets))
    return stack_number


def entry(string_input):
    """Search of operation of comparison in expression."""
    level_1 = []
    level_2 = []
    sep_operation = ['<', '>', '!', '=']
    for index, element in enumerate(string_input):
        for sep in sep_operation:
            if sep == element:
                if string_input[index + 1] == '=':
                    new_operation = sep + string_input[index + 1]
                    level_1.append(index)
                    level_2.append(new_operation)
                else:
                    level_1.append(index)
                    level_2.append(element)
    res = level_1, level_2
    return res


def value(res, input_string):
    """Splitting expression on comparison operation."""
    if len(res[0]) > 1:
        value_1 = input_string[:int(res[0][0])]
        value_2 = input_string[int(res[0][1]) + 1:]
        keys = value_1, value_2
        return keys

    elif len(res[0]) < 2:
        value_1 = input_string[:int(res[0][0])]
        value_2 = input_string[int(res[0][0]) + 1:]
        keys = value_1, value_2
        return keys


def comparasion(res, keys):
    """Comparison expression."""
    operation_comparison = res[1][0]
    operation_comparison_str = ''.join(operation_comparison)
    if operation_comparison_str in ops_comparison:
        result = ops_comparison[operation_comparison_str].function(keys[0], keys[1])
        return result


def calculathion_on_functhions(expression_input):
    """Choosing a transformation path followed by calculating the expression."""
    result_value = []
    if '(' in expression_input and ')' in expression_input:
        result_value.append(calculate(calculate_brack(transformathion_stack(brackets_count(expression_input)))))
    else:
        result_value.append(calculate(transformathion_stack(expression_input)))
    return result_value[0]


def calculathion_comparison_of_expression(input_value):
    """Viewing of expression on existence of operation of comparison with the subsequent its calculation."""

    answer = []
    index_before_operathion = entry(input_value)
    if len(index_before_operathion[1]) == 0:
        answer.append(calculathion_on_functhions(input_value))
    else:
        value_before_after_ops = value(index_before_operathion, input_value)
        value_before = calculathion_on_functhions(value_before_after_ops[0])
        value_after = calculathion_on_functhions(value_before_after_ops[1])
        answer.append(comparasion(index_before_operathion, (value_before, value_after)))
    return answer[0]


def main():
    """Main endpoint for call in packege"""
    parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    parser.add_argument('expression', type=str, help='expression string to evaluate')
    args = parser.parse_args()

    try:
        if calculathion_comparison_of_expression(args.expression) == None:
            pass
        else:
            print(calculathion_comparison_of_expression(args.expression))

    except InternalError:
        pass


if __name__ == '__main__':
    main()
