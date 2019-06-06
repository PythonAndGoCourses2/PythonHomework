import arithmetic
import re


def calculate(value):
    """ It is a calculator. It can be use Math operation"""

    if type(value) is not str:
        print('It expected str got ' + type(value).__name__)

    access_operators = ['+', '-', '*', '/', '//', '%', '**']
    operators = re.findall(r'(\D*[^-.?\d?])', value)
    digits = re.findall(r'(-*\.*\d+\.*\d*)', value)
    if len(operators) == len(digits):
        return "Error: you miss digits"
    # check accessible operators
    for operator in operators:
        format_operator = operator.replace(' ', '')
        if format_operator not in access_operators:
            return "Error: not accessible operator '" + operator + "'"

    counter = 0
    result = 0
    rest_operator = []
    rest_digits = []
    check = False
    #     look for priority operators
    for operator in operators:
        format_operator = operator.replace(' ', '')

        if format_operator == '/' or format_operator == '*' or format_operator == '//' or format_operator == '%' \
                or format_operator == '**':
            first_parameter = digits[counter]
            if check:
                first_parameter = rest_digits[-1]
            if format_operator == '*':
                result = arithmetic.multiply(first_parameter, digits[counter + 1])
            elif format_operator == '/':
                result = arithmetic.division(first_parameter, digits[counter + 1])
                if type(result) is str:
                    return result
            elif format_operator == '//':
                result = arithmetic.integer_division(first_parameter, digits[counter + 1])
            elif format_operator == '%':
                result = arithmetic.modulo_division(first_parameter, digits[counter + 1])
            elif format_operator == '**':
                result = arithmetic.power(first_parameter, digits[counter + 1])
            if counter != 0:
                rest_digits[-1] = result
            else:
                rest_digits.append(result)
            check = True
        else:
            rest_operator.append(format_operator)
            if counter == 0:
                rest_digits.append(digits[counter])
            rest_digits.append(digits[counter + 1])
            check = False
        counter += 1
    if len(rest_operator) == 0:
        # return value
        if len(rest_digits) > 0:
            return rest_digits[0]
        else:
            return value
    else:
        result = rest_digits[0]
        counter2 = 0
        for operator in rest_operator:
            format_operator = operator.replace(' ', '')
            if format_operator == '+':
                result = arithmetic.add(result, rest_digits[counter2 + 1])
            elif format_operator == '-':
                result = arithmetic.subtraction(result, rest_digits[counter2 + 1])
            counter2 += 1
    return result
