import re
import tool
import config


def validation(string):
    pass


def remove_space_between_operators(string):
    array = list(string)
    for idx, token in enumerate(array):
        if token == ' ':
            index = idx
            for char in array[idx+1:]:
                array[index] = char
                index += 1
            array.pop()
    return ''.join(array)


def f_or_i(obj):
    if type(obj) == str:
        if obj[0] == '[':
            array = []
            for i in obj:
                if i.isdigit():
                    array.append(f_or_i(i))
            return array
        elif obj == 'True' or obj == 'False':
            return bool(obj)
        elif '.' in obj:
            return float(obj)
        return int(obj)
    return obj


def split_all_characters_and_numbers(string):
    array = []
    square_brackets = 0
    for idx, token in enumerate(string):
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
            if len(array) == 0:
                array.append(token)
            elif token == '/' and array[-1] == '/':
                array[-1] += token
            elif token == '-' or token == '+':
                if array[-1] == '-' or array[-1] == '+':
                    if len(array) == 1:
                        array[-1] += '1'
                        array.append('*')
                        array.append(token)
                    else:
                        if array[-2] == '(' or array[-2] in config.characters:
                            array[-1] += '1'
                            array.append('*')
                            array.append(token)
                        else:
                            array.append('1')
                            array.append('*')
                            array.append(token)
                else:
                    array.append(token)
            else:
                array.append(token)
        elif token == '.':
            if len(array) == 0:
                array.append('0.')
            elif array[-1][-1].isdigit():
                array[-1] += token
            elif array[-1] == '-':
                array[-1] = '-0.'
            else:
                array.append('0.')
        elif token.isdigit():
            if len(array) != 0:
                if re.match(r'^log', array[-1]) or re.match(r'^expm', array[-1]):
                    array[-1] += token
                    continue
            if len(array) == 0:
                array.append(token)
            elif len(array) == 1:
                if array[-1] == '-' or array[-1].isdigit() or array[-1][-1] == '.' or array[-1][-1].isdigit():
                    array[-1] += token
                elif array[-1] == '.':
                    array[0] = '0.' + token
                else:
                    array.append(token)
            else:
                if array[-1] == '-' or array[-1] == '+':
                    if array[-2] == '+' or array[-2] == '-':
                        array[idx-1] = '0'
                        array.append('-' + token)
                    elif array[-2] in config.characters or array[-2] == '(' or array[-2] == ',':
                        array[-1] += token
                    else:
                        array.append(token)
                elif array[-1].isdigit() or array[-1][-1].isdigit() or array[-1][-1] == '.':
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
            array.insert(idx, result)
    return array


def function_calculation(array):
    if ',' in array:
        index = array.index(',')
        result_first = calculation(array[2:index])
        result_second = calculation(array[index+1:-1])
        return tool.functions(f_or_i(result_first), array[0], f_or_i(result_second))
    else:
        result = calculation(array[2:-1])
        return tool.functions(f_or_i(result), array[0])


def brackets_calculation(array):
    while '(' in array:
        brackets_inside = {}
        last = ''
        index = 0
        for idx, token in enumerate(array):
            if token == '(' and last == token:
                index = idx
            elif token == ')' and last == '':
                continue
            elif token == ')':
                brackets_inside[index] = idx
                last = ''
                index = 0
            elif token == '(':
                last = token
                index = idx
        offset = 0
        for key, value in brackets_inside.items():
            if array[key - 1 - offset] in config.all_functions:
                result = function_calculation(array[key-offset-1:value-offset+1])
                if array[key - offset - 1] == 'frexp':
                    return result
                length = len(array[key-offset-1:value-offset+1])
                first_index = key - offset - 1
                for char in array[value+1-offset:]:
                    array[first_index] = char
                    first_index += 1
                for i in range(length):
                    array.pop()
                if len(array) != 0:
                    if array[key-offset-2] == '-' and (array[key-offset-3] == '(' or array[key-offset-3] in config.characters or array[key-offset-3] == ','):
                        array[key-offset-2] += str(result)
                    else:
                        array.insert(key-offset-1, str(result))
                else:
                    array.append(result)
                offset += length - 1
            else:
                result = calculation(array[key+1-offset:value-offset])
                first_index = key - offset
                length = len(array[key-offset:value+1-offset])
                for char in array[value+1-offset:]:
                    array[first_index] = char
                    first_index += 1
                for i in range(length):
                    array.pop()
                array.insert(key-offset, result)
                offset += length - 1
    return array


def calculation(array):
    if type(array) == tuple or type(array[0]) == list:
        return array
    if len(array) != 1:
        for token in config.characters:
            while token in array:
                idx = array.index(token)
                result = tool.arithmetic(f_or_i(array[idx-1]), f_or_i(array[idx+1]), token)
                if len(array) == 3:
                    return result
                index = idx
                for char in array[idx+2:]:
                    array[index-1] = char
                    index += 1
                for i in range(3):
                    array.pop()
                array.insert(idx - 1, result)
    else:
        return array[0]


def main(string):
    res = remove_space_between_operators(string)
    res = split_all_characters_and_numbers(res)
    res = constants_switch(res)
    res = brackets_calculation(res)
    res = calculation(res)
    return f_or_i(res)

