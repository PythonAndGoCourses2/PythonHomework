import re
import tool
import config
import math
import validation
import sys


def validations(string):
    validation.main(string)


def remove_space_between_operators(string):
    array = list(string)
    for idx, token in enumerate(array):
        if token == ' ':
            array.pop(idx)
    return ''.join(array)


def object_type(obj):
    try:
        if type(obj) == str:
            if obj[0] == '[':
                array = []
                for token in obj:
                    if token.isdigit():
                        array.append(object_type(token))
                return array
            elif obj == 'True' or obj == 'False':
                return bool(obj)
            elif '.' in obj:
                return float(obj)
            return int(obj)
        return obj
    except ValueError:
        sys.exit('ERROR: unknown object - ' + obj)


def split_all_comparison_characters(string):
    array = ['']
    for idx, token in enumerate(string):
        if token in config.comparison_check and array[-1] in config.comparison_check:
            array[-1] += token
            array.append('')
        elif token in config.comparison_check:
            array.append(token)
        elif array[-1] in config.comparison_check:
            array.append(token)
        else:
            array[-1] += token
    return array


def comparison_calculation(string):
    for token in config.comparison_check:
        if token in string:
            array = split_all_comparison_characters(string)
            for idx in range(1, len(array), 2):
                try:
                    result = tool.comparison_calculation(main(array[idx-1]), main(array[idx+1]), array[idx])
                except SystemExit:
                    sys.exit('ERROR: no value to compare!')
                if not result:
                    return False
                return True


def replace_minus_plus_characters(string):
    array = list(string)
    for idx, token in enumerate(array):
        if token == '-' or token == '+':
            try:
                while array[idx+1] == '-' or array[idx+1] == '+':
                    array[idx] = config.minus_plus_characters[array[idx] + array[idx+1]]
                    array.pop(idx+1)
            except IndexError:
                sys.exit('ERROR: no value for expression!')
    return ''.join(array)


def insert_zero_before_point(string):
    array = list(string)
    for idx, token in enumerate(array):
        if idx == 0 and token == '.':
            array.insert(idx, '0')
        elif token == '.' and not array[idx-1].isdigit():
            array.insert(idx, '0')
    return ''.join(array)


def assembly_of_negative_numbers(array):
    for idx, token in enumerate(array):
        if (token == '-' or token == '+') and idx == 0 and array[idx+1][0].isdigit():
            array[idx] += array[idx+1]
            array.pop(idx+1)
        elif (token == '-' or token == '+') and array[idx+1][0].isdigit() and (array[idx-1] == '('
                                                                               or array[idx-1] == ','
                                                                               or array[idx-1] in config.characters):
            array[idx] += array[idx + 1]
            array.pop(idx + 1)
    return array


def split_all_characters_and_numbers(string):
    array, square_brackets = [], 0
    for idx, token in enumerate(string):
        if token in config.sqr_brackets or square_brackets:
            if token == ']':
                array[-1] += token
                square_brackets = 0
            elif square_brackets:
                array[-1] += token
            elif token == '[':
                array.append(token)
                square_brackets = 1
        elif token in config.brackets or token == ',':
            array.append(token)
        elif token in config.characters:
            if token == '/' and array[-1] == '/':
                array[-1] += token
            else:
                array.append(token)
        elif token == '.':
            if array[-1].isdigit():
                array[-1] += token
            else:
                array.append(token)
        elif token.isdigit():
            if len(array) == 0:
                array.append(token)
            elif array[-1][-1] == '.' or array[-1][-1].isdigit() or array[-1].isalpha():
                array[-1] += token
            else:
                array.append(token)
        elif token.isalpha():
            if len(array) == 0:
                array.append(token)
            else:
                if array[-1].isalpha() or re.match(r'^log1', array[-1]):
                    array[-1] += token
                else:
                    array.append(token)
    return array


def constants_switch(array):
    for token in config.constants:
        while token in array:
            idx = array.index(token)
            result = tool.constants_calculation(token)
            array.pop(idx)
            if len(array) == 0:
                array.insert(idx, result)
            elif array[idx-1] == '-' and (array[idx-2] in config.characters
                                          or array[idx-2] == '('
                                          or array[idx-2] == ','):
                array[idx-1] += str(result)
            else:
                array.insert(idx, result)
    return array


def function_calculation(array):
    index, arguments = 0, []
    for idx, token in enumerate(array):
        if token in config.brackets or token == ',':
            if index == 0:
                index = idx
            else:
                result = calculation(array[index+1:idx])
                arguments.append(object_type(result))
                index = idx
    return tool.functions(array[0], *arguments)


def search_for_all_atomic_brackets(array):
    brackets_inside = []
    last = ''
    index = 0
    for idx, token in enumerate(array):
        if token == '(' and last == token:
            index = idx
        elif token == ')' and last == '':
            continue
        elif token == ')':
            brackets_inside.append(index)
            brackets_inside.append(idx)
            last = ''
            index = 0
        elif token == '(':
            last = token
            index = idx
    return brackets_inside


def pop_calculated_items(array, first_index, second_index, length):
    index = first_index
    for token in array[second_index:]:
        array[index] = token
        index += 1
    for i in range(length):
        array.pop()
    return array


def brackets_calculation(array):
    while '(' in array:
        brackets_inside = search_for_all_atomic_brackets(array)
        for second_index in brackets_inside[::-2]:
            first_index = brackets_inside[brackets_inside.index(second_index) - 1]
            if array[first_index - 1] in config.all_functions:
                result = function_calculation(array[first_index - 1:second_index + 1])
                if array[first_index - 1] == 'frexp':
                    return result
                length = len(array[first_index - 1:second_index + 1])
                array = pop_calculated_items(array, first_index-1, second_index+1, length)
                if len(array) != 0:
                    if array[first_index - 2] == '-' or array[first_index - 2] == '+':
                        if result < 0:
                            array[first_index - 2] = '+' if array[first_index - 2] == '-' else '-'
                            array.insert(first_index - 1, str(math.fabs(result)))
                        else:
                            array.insert(first_index - 1, str(result))
                    else:
                        array.insert(first_index - 1, str(result))
                else:
                    array.append(result)
            else:
                result = calculation(array[first_index + 1:second_index])
                length = len(array[first_index:second_index + 1])
                array = pop_calculated_items(array, first_index, second_index + 1, length)
                array.insert(first_index, str(result))
    return array


def replace_minus_and_negative_numbers(array):
    for idx, token in enumerate(array):
        if token == '-' and array[idx+1][-1].isdigit():
            array[idx] = '+'
            array[idx+1] = str(-object_type(array[idx+1]))
    return array


def calculation(array):
    if type(array) == tuple or type(array[0]) == list:
        return array
    if array[0] in config.characters:
        array.insert(0, '0')
    if len(array) == 3:
        result = tool.arithmetic(object_type(array[0]), object_type(array[2]), array[1])
        return result
    elif len(array) == 1:
        return array[0]
    else:
        for token in config.characters:
            while token in array:
                if token == '^':
                    i = 1
                    while i <= len(array):
                        if array[-i] == token:
                            result = tool.arithmetic(object_type(array[-i-1]), object_type(array[-i+1]), token)
                            if len(array) == 3:
                                return result
                            index = -i
                            for i in range(2):
                                array.pop(index+1)
                            array[index+1] = str(result)
                        i += 1
                else:
                    idx = array.index(token)
                    array = replace_minus_and_negative_numbers(array)
                    result = tool.arithmetic(object_type(array[idx - 1]), object_type(array[idx + 1]), array[idx])
                    if len(array) == 3:
                        return result
                    index = idx
                    for char in array[idx + 2:]:
                        array[index - 1] = char
                        index += 1
                    for i in range(3):
                        array.pop()
                    array.insert(idx - 1, str(result))
        return array[0]


def main(string):
    validations(string)
    res = remove_space_between_operators(string)
    bool_result = comparison_calculation(res)
    if type(bool_result) == bool:
        return bool_result
    res = insert_zero_before_point(res)
    res = replace_minus_plus_characters(res)
    res = split_all_characters_and_numbers(res)
    res = assembly_of_negative_numbers(res)
    res = constants_switch(res)
    res = brackets_calculation(res)
    res = calculation(res)
    return object_type(res)
