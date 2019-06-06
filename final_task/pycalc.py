import argparse
import re
import pycalc_common
# from math import *

parser = argparse.ArgumentParser()
parser.add_argument("EXPRESSION", type=str,  help="expression is the string you use here")
parser.add_argument("-m", "--use-modules", help="additional modules to use", action="store_true")
args = parser.parse_args()
if args.EXPRESSION:
    print(pycalc_common.pcalc(args.EXPRESSION))

# print(pycalc_common.pcalc('sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e)))'))
# def pcalc(value):
#     left_bracket = re.findall(r'\(', value)
#     right_bracket = re.findall(r'\)', value)
#     if len(left_bracket) != len(right_bracket):
#         return 'error: missing bracket'
#
#     result_calculate = calculate_math_parameters.calculate_math_parameters(value)
#
#     print('result_calculate', result_calculate)
#     if len(left_bracket) or len(right_bracket):
#         result = parse_brackets.parse_brackets(result_calculate)
#     else:
#         result = eval(value)
#     # print('eval_result:', eval(value))
#     print('my_result:', result)
#     return result


# print(pcalc('sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e)))'))
# print(sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e))))
# print(calculate_expression.calculate('2.718281828459045**2.718281828459045**-0.8462204041751706'))
# print(2.718281828459045**2.718281828459045**-0.8462204041751706)
# print(2.718281828459045**-0.8462204041751706)
# print(2.718281828459045**0.4290334443756452)
# print(calculate_expression.calculate('5**2'))
# print(calc_math('sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0)'))
# print(sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0))
# print(parse_brackets.parse_brackets('sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e)))'))
# print(calculate_math_parameters.calculate_math_parameters('e + .3 + e '))
# print(pcalc('7+((4+e) + log(8)*8)/cos((log(8) - 4)*2)'))

def calculate(value):
    parameters_level_one = ['**']
    parameters_level_two = ['/', '*', '//', '%']
    parameters_level_three = ['+', '-']
    all_parameters = parameters_level_one + parameters_level_two + parameters_level_three
    # get_numbers = []
    # get_operators = []
    # temp = ""
    # prev_item = ""
    # value = value.replace(' ', '')
    # for item in value:
    #     if re.match(r'\d', item):
    #         get_number.append('item')
    #     if not re.match(r'\d]', item):
    operators = re.findall(r'(\D*[^.?\d?])', value)
    digits = re.findall(r'(\.*\d+\.*\d*)', value)
    counter = 0
    get_first_number = 0
    get_second_number = 0
    for item in operators:
        item = item.replace(' ', '')
        if len(digits) > counter:
            get_first_number = digits[counter]
        if len(digits) > counter + 1:
            get_second_number = digits[counter + 1]
        if item not in all_parameters:
            minus = re.findall('-', item)

            elements = re.findall(r'[^-+\s]', item)
            print(len(minus) % 2)
            if len(minus) % 2 == 0:
                get_second_number = '-' + get_second_number
            print('elements:', elements)
            if len(minus) == 0:
                return "Error: not accessible operator '" + item + "'"
            get_parameter = re.findall(r'(\D*[^-+.?\d?])', value)
        counter += 1
        print(get_first_number)
        print(get_second_number)
        print('result:', float(get_first_number) * float(get_second_number))

    print(operators)
    print(digits)
