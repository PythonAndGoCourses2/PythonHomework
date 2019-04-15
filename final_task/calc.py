import math, unittest, re
import tool, config


def validation(string):
    pass


def remove_space_between_operators(string):
    array = list(string)
    for idx, chr in enumerate(array):
        if chr == ' ':
            index = idx
            for char in array[idx+1:]:
                array[index] = char
                index += 1
            array.pop()
    return ''.join(array)


def f_or_i(obj):
    if type(obj) == tuple:
        return obj
    elif type(obj) == str:
        if obj[0] == '[':
            array = []
            for i in obj:
                if i.isdigit():
                    array.append(f_or_i(i))
            return array
        elif '.' in obj:
                return float(obj)
        return int(obj)
    return obj


def split_all_characters_and_numbers(string):
    array = []
    array_brackets = 0
    for idx, chr in enumerate(string):
        if chr == ']':
            array[-1] += chr
            array_brackets = 0
        elif array_brackets:
            array[-1] += chr
        elif chr == '[':
            array.append(chr)
            array_brackets = 1
        elif chr in config.brackets or chr == ',':
            array.append(chr)
        elif chr in config.characters:
            if len(array) == 0:
                array.append(chr)
            elif chr == '/' and array[-1] == '/':
                    array[-1] += chr
            elif chr == '-' or chr == '+':
                if array[-1] == '-' or array[-1] == '+':
                    if len(array) == 1:
                        array[0] = -0
                        array.append(chr)
                    else:
                        array.append(0)
                        array.append(chr)
                else:
                    array.append(chr)
            else:
                array.append(chr)
        elif chr == '.':
            if len(array) == 0:
                array.append('0.')
            elif array[-1][-1].isdigit():
                array[-1] += chr
            elif array[-1] == '-':
                array[-1] = '-0.'
            else:
                array.append('0.')
        elif chr.isdigit():
            if len(array) != 0:
                if re.match(r'^log', array[-1]) or re.match(r'^expm', array[-1]):
                    array[-1] += chr
                    continue
            if len(array) == 0:
                array.append(chr)
            elif len(array) == 1:
                if array[-1] == '-' or array[-1].isdigit() or array[-1][-1] == '.' or array[-1][-1].isdigit():
                    array[-1] += chr
                elif array[-1] == '.':
                    array[0] = '0.' + chr
                else:
                    array.append(chr)
            else:
                if array[-1] == '-':
                    if array[-2] == '+' or array[-2] == '-':
                        array[idx-1] = 0
                        array.append('-' + chr)
                    elif array[-2] in config.characters or array[-2] == '(' or array[-2] == ',':
                        array[-1] += chr
                    else:
                        array.append(chr)
                elif array[-1].isdigit() or array[-1][-1].isdigit() or array[-1][-1] == '.':
                    array[-1] += chr
                else:
                    array.append(chr)
        elif chr.isalpha():
            if len(array) == 0:
                array.append(chr)
            else:
                if array[-1].isalpha() or re.match(r'^log1', array[-1]):
                    array[-1] += chr
                else:
                    array.append(chr)
    return array


def constants_switch(array):
    for chr in config.constants:
        while chr in array:
            idx = array.index(chr)
            result = tool.constants_calculation(chr)
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
        for idx, chr in enumerate(array):
            if chr == '(' and last == chr:
                index = idx
            elif chr == ')' and last == '':
                continue
            elif chr == ')':
                brackets_inside[index] = idx
                last = ''
                index = 0
            elif chr == '(':
                last = chr
                index = idx
        offset = 0
        for key, value in brackets_inside.items():
            if array[key - 1 - offset] in config.all_functions:
                result = function_calculation(array[key-offset-1:value-offset+1])
                if array[key - offset - 1] == 'frexp':
                    return result
                length = len(array[key-offset-1:value-offset+1])
                first_index = key - offset - 1
                for char in array[value +1 - offset:]:
                    array[first_index] = char
                    first_index += 1
                for i in range(length):
                    array.pop()
                array.insert(key - offset -1, result)
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
        for chr in config.characters:
            while chr in array:
                idx = array.index(chr)
                result = tool.arithmetic(f_or_i(array[idx-1]), f_or_i(array[idx+1]), chr)
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


@time_decorator
def main(string):
    res = remove_space_between_operators(string)
    res = split_all_characters_and_numbers(res)
    res = constants_switch(res)
    res = brackets_calculation(res)
    res = calculation(res)
    return f_or_i(res)

