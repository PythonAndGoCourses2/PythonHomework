import re
import tool
import config
import math
import validation
import sys
import argparse


def validations(string):
    """Validation in advance using the module validation.py."""
    validation.main(string)


def remove_space_between_operators(string):
    """Removes spaces from the string."""
    array = list(string)
    for idx, token in enumerate(array):
        if token == ' ':
            array.pop(idx)
    return ''.join(array)


def split_all_comparison_characters(string):
    """
    Splits a string by comparative characters.

    :return: array
    """
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
    """
     Calculation logical expression.

     Description: the cycle goes through the list comparing logical pairs. If False returns from the pair,
     the cycle is interrupted.

    :return: bool
    """
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
    """
    Replaces possible variations of minus-plus pairs. Simulate the multiplication of numbers
    with the specified characters.
    """
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
    """Insert a zero in front of the point if necessary"""
    array = list(string)
    for idx, token in enumerate(array):
        if idx == 0 and token == '.':
            array.insert(idx, '0')
        elif token == '.' and not array[idx-1].isdigit():
            array.insert(idx, '0')
    return ''.join(array)


def assembly_of_negative_numbers(array):
    """
    The function replaces a pair of elements in the array with a minus number by a negative number.

    Example: ['(','-','3','+','2',')'] --> ['(','-3','+','2',')']
    """
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
    """
    The main function. Converting string expressions into a list divided by elements.

    Description: a loop passes a string defining the type of each element. A set of conditions
    determines how to place this element in the final list.

    :return: array
    """
    array, square_brackets = [], 0
    for idx, token in enumerate(string):
        # array allocation
        if token in config.sqr_brackets or square_brackets:  # '[1, 2, 3]'
            if token == ']':
                array[-1] += token
                square_brackets = 0
            elif square_brackets:
                array[-1] += token
            elif token == '[':
                array.append(token)
                square_brackets = 1
        # brackets allocation
        elif token in config.brackets or token == ',':
            array.append(token)
        # array allocation
        elif token in config.characters:
            if token == '/' and array[-1] == '/':  # '4 // 2'
                array[-1] += token
            else:
                array.append(token)
        # point allocation
        elif token == '.':
            if array[-1].isdigit():
                array[-1] += token  # 3 --> 3.
            else:
                array.append(token)
        # number allocation
        elif token.isdigit():
            if len(array) == 0:
                array.append(token)
            elif array[-1][-1] == '.' or array[-1][-1].isdigit() or array[-1].isalpha():
                array[-1] += token  # 3. --> 3.3
            else:
                array.append(token)
        # letter allocation
        elif token.isalpha():
            if len(array) == 0:
                array.append(token)
            else:
                if array[-1].isalpha() or re.match(r'^log1', array[-1]):  # function - log1p
                    array[-1] += token
                else:
                    array.append(token)
    return array


def constants_switch(array):
    """Replaces all constants in the list with their values."""
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
    """Receives an array with a function and its arguments and performs calculations."""
    index, arguments = 0, []
    for idx, token in enumerate(array):
        if token in config.brackets or token == ',':
            if index == 0:
                index = idx
            else:
                result = calculation(array[index+1:idx])
                arguments.append(tool.object_type(result))
                index = idx
    return tool.functions(array[0], *arguments)


def search_for_all_atomic_brackets(array):
    """Searches for atomic brackets. Compiles the final array with the data indexes of the brackets."""
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


def brackets_calculation(array):
    """
    Calculation slices with brackets.

    Description: Gets the indices of atomic brackets from the function "search_for_all_atomic_brackets".
    Checks parentheses for math functions. Calculates by function function_calculation.
    Inserts a total value into the list.
    """
    while '(' in array:
        brackets_inside = search_for_all_atomic_brackets(array)
        for second_index in brackets_inside[::-2]:
            first_index = brackets_inside[brackets_inside.index(second_index) - 1]
            if array[first_index - 1] in config.all_functions:
                # function brackets
                result = function_calculation(array[first_index - 1:second_index + 1])
                if array[first_index - 1] == 'frexp':  # function frexp - input array
                    return result
                length = len(array[first_index - 1:second_index + 1])
                array = tool.pop_calculated_items(array, first_index-1, second_index+1, length)
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
                array = tool.pop_calculated_items(array, first_index, second_index + 1, length)
                array.insert(first_index, str(result))
    return array


def calculation(array):
    """Calculation of simple expressions"""
    if type(array) == tuple or type(array[0]) == list:
        return array
    if array[0] in config.characters:
        array.insert(0, '0')
    if len(array) == 3:
        result = tool.arithmetic(tool.object_type(array[0]), tool.object_type(array[2]), array[1])
        return result
    elif len(array) == 1:
        return array[0]
    else:
        for token in config.characters:
            while token in array:
                # exponentiation counts from the end
                if token == '^':
                    i = 1
                    while i <= len(array):
                        if array[-i] == token:
                            result = tool.arithmetic(tool.object_type(array[-i-1]),
                                                     tool.object_type(array[-i+1]), token)
                            if len(array) == 3:
                                return result
                            index = -i
                            for i in range(2):
                                array.pop(index+1)
                            array[index+1] = str(result)
                        i += 1
                else:
                    idx = array.index(token)
                    array = tool.replace_minus_and_negative_numbers(array)
                    result = tool.arithmetic(tool.object_type(array[idx - 1]),
                                             tool.object_type(array[idx + 1]), array[idx])
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
    """Main function determining the order of calculations."""
    validations(string)
    result = remove_space_between_operators(string)
    bool_result = comparison_calculation(result)
    if type(bool_result) == bool:
        return bool_result
    result = insert_zero_before_point(result)
    result = replace_minus_plus_characters(result)
    result = split_all_characters_and_numbers(result)
    result = assembly_of_negative_numbers(result)
    result = constants_switch(result)
    result = brackets_calculation(result)
    result = calculation(result)
    return tool.object_type(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='pycalc [-h] EXPRESSION',
        description='Pure-python command-line calculator.'
    )
    parser.add_argument('EXPRESSION', help='expression string to evaluate')
    args = parser.parse_args()
    print(main(args.EXPRESSION))
