import math
import re
import builtins
import calculate_expression, parse_brackets

math_param = dir(math)
additional_param = ['abs', 'round']
all_parameters = math_param + additional_param


def calc_math(name, value):
    if value.find(',') == -1:
        result = getattr(math, name)(
            float(calculate_expression.calculate("".join(parse_brackets.parse_brackets(value)))))
    else:
        new_value = value.split(',')
        result = getattr(math, name)(
            float(calculate_expression.calculate("".join(parse_brackets.parse_brackets(new_value[0])))),
            float(calculate_expression.calculate("".join(parse_brackets.parse_brackets(new_value[1])))))
    return result


def cal_additional_parameters(name, value):
    return getattr(builtins, name)(float(eval(value)))


# input: value -  string expression
# output: string with calculated parameters
def calculate_math_parameters(value):
    value = value.replace('pi', str(math.pi)).replace('e', str(math.e))

    math_parameters_from_expression = re.findall(r'(\w+)\s*\((.+)\)', value)
    value = value.replace(' (', '(')

    for items in math_parameters_from_expression:
        new_item_name = items[0]
        new_item_value = items[1]
        if new_item_name not in all_parameters:
            return 'Error: parameter "' + new_item_name + '" not found'
        if items[0] in additional_param:
            value = value.replace(items[0] + '(' + items[1] + ')',
                                  str(cal_additional_parameters(new_item_name, new_item_value)))
        else:
            value = value.replace(items[0] + '(' + items[1] + ')', str(calc_math(new_item_name, new_item_value)))

    return value


def calc_math_parameter(value):

    result = []
    temp = ""
    previous_element = ""
    for item in value:
        if re.match(r'[a-z]', item) and not re.match(r'[a-z]', previous_element):
            if len(temp) > 0:
                result.append(temp)
                temp = ""
        temp += item
        if item == ')':
            if len(temp) > 0:
                if temp.find('(') != -1 and temp.find(')') != -1:
                    count_left_bracket = re.findall(r'\(', temp)
                    count_right_bracket = re.findall(r'\)', temp)
                    if len(count_left_bracket) == len(count_right_bracket):
                        if len(result) > 0:
                            if result[-1].find('(') != -1:
                                temp = result[-1] + str(calculate_math_parameters(temp))
                                del result[-1]
                            else:
                                temp = str(calculate_math_parameters(temp))
                                result.append(temp)
                                temp = ""
                        else:
                            temp = str(calculate_math_parameters(temp))
                            result.append(temp)
                            temp = ""
                else:
                    result.append(temp)
                    temp = ""
        previous_element = item
    return result
