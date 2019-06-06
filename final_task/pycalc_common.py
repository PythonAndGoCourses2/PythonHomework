import re
import calculate_math_parameters
import parse_brackets
import calculate_expression
import math


def pcalc(value):
    value = value.replace('pi', str(math.pi)).replace('e', str(math.e))
    left_bracket = re.findall(r'\(', value)
    right_bracket = re.findall(r'\)', value)
    if len(left_bracket) != len(right_bracket):
        return 'error: missing bracket'

    math_parameters_from_expression = re.findall(r'(\w+)\s*\((.+)\)', value)
    result = value
    if len(math_parameters_from_expression):
        result = "".join(calculate_math_parameters.calc_math_parameter(value))
    result = parse_brackets.parse_brackets(result)
    result = calculate_expression.calculate(result)
    return result
