import argparse
import os
import math
import sys


def chek_minus(list_of_elements):
    """Checks the list of elements
    and remove the extra plus and minus
    """
    index = 0
    letters = set('qwertyuiopasdfghjklzxcvbnm')
    previously = ''
    while index < len(list_of_elements):
        element = list_of_elements[index]
        temp = str(element)
        if element is "+" or element is "-":
            if previously is "+" or previously is "-":
                if previously is "+" and previously == element:
                    list_of_elements.pop(index)
                elif previously is "-" and previously == element:
                    list_of_elements.pop(index)
                    list_of_elements.pop(index-1)
                    list_of_elements.insert(index-1, "+")
                elif previously != element:
                    list_of_elements.pop(index)
                    list_of_elements.pop(index-1)
                    list_of_elements.insert(index-1, "-")
                index -= 1
                previously = list_of_elements[index]
            else:
                previously = element
        elif not letters.isdisjoint(temp) and previously is "-":
            list_of_elements[index - 1] = -1
            list_of_elements.insert(index, '*')
            index += 1
        else:
            previously = ""
        index += 1
    index = 0
    last_two = ["", ""]
    while index < len(list_of_elements):
        element = list_of_elements[index]
        temp = str(element)
        temp = temp.replace('-', '', 1)
        if temp.replace('.', '', 1).isdigit():
            if last_two[1] is "+" or last_two[1] is "-":
                temp = str(last_two[0])
                temp = temp.replace('-', '', 1).replace('.', '', 1)
                if temp is '' or (temp.isdigit() is False and temp != ')'):
                    if last_two[1] is "-":
                        list_of_elements[index] = element*(-1)
                    list_of_elements.pop(index-1)
                    index -= 1
        if len(list_of_elements) > 1:
            last_two[0] = last_two[1]
            last_two[1] = list_of_elements[index]
        index += 1
    return list_of_elements


def write_in_not(list_of_elements):
    """writes the elements of the list in reverse Polish notation
    required for the calculation by the function calculate()
    """
    precedence = {
                '+': 2,
                '-': 2,
                '*': 3,
                '//': 3,
                '/': 3,
                '^': 4,
                '%': 3,
                '(': 0,
                ')': 0
        }
    comparison_operations = set('<=>!')
    output = []
    stack = []
    list_of_elements = chek_minus(list_of_elements)
    index = 0
    while index < len(list_of_elements):
        element = list_of_elements[index]
        temp = str(element)
        temp = temp.replace('-', '', 1)
        if element is '(':
            stack.insert(0, element)
        elif temp.replace('.', '', 1).isdigit():
            output.append(element)
        elif not comparison_operations.isdisjoint(temp):
            '#if element is comparison'
            for operation in stack:
                output.append(operation)
            result = calculate(output)
            stack.clear()
            output.clear()
            output.append(result)
            new_list = list(list_of_elements[index+1:])
            notation2 = write_in_not(new_list)
            result2 = calculate(notation2)
            '#if we have more than one comparison'
            if result2 is True:
                index2 = 0
                temp = str(new_list[index2])
                while comparison_operations.isdisjoint(temp):
                    index2 += 1
                    temp = str(new_list[index2])
                index2 -= 1
                new_list = list(new_list[: index2 + 1])
                notation2 = write_in_not(new_list)
                result2 = calculate(notation2)
            elif result2 is False:
                output.clear()
                output.append(result2)
                return output
            output.append(result2)
            output.append(element)
            index = len(list_of_elements)
        elif element is ')'and len(stack) > 0:
            while stack[0] != '(':
                output.append(stack.pop(0))
            stack.pop(0)
        elif element in precedence.keys():
            if len(stack) > 0 and precedence[element] == precedence[stack[0]]\
                    and element != "^":
                output.append(stack.pop(0))
                stack.insert(0, element)
            elif len(stack) > 0 and precedence[element] < precedence[stack[0]]:
                while len(stack) > 0 and\
                        precedence[element] <= precedence[stack[0]]:
                    output.append(stack.pop(0))
                stack.insert(0, element)
            else:
                stack.insert(0, element)
        else:
            function = element
            brackets = 1
            temp = ""
            args = []
            index += 2
            while brackets != 0 and index < len(list_of_elements):
                element = list_of_elements[index]
                if element is ',' and brackets == 1:
                    args.append(testing(temp))
                    temp = ''
                elif element is ')' and brackets == 1:
                    args.append(testing(temp))
                    temp = ''
                    brackets -= 1
                elif element is ')' and brackets != 1:
                    temp += str(element)
                    brackets -= 1
                elif element is '(':
                    brackets += 1
                    temp += str(element)
                else:
                    temp += str(element)
                index += 1
            '#unpack all elements from list and '
            '#    transferring them to the  function'
            if function != "abs" and function != "round":
                function = getattr(math, function)
                try:
                    result = function(*args)
                except TypeError:
                    print("ERROR: invalid number or parameter types")
                    sys.exit(1)
            elif function == "abs":
                result = abs(*args)
            else:
                result = round(*args)
            output.append(result)
            '#because the current index points to the item'
            '#after the closing parenthesis'
            index -= 1
        index += 1
    for element in stack:
        output.append(element)
    return output


def tokenize(entered_string):
    """Breaks a string into elements
    """
    entered_string += " "
    '#some problems with index out of range without it'
    letters = set('qwertyuiopasdfghjklzxcvbnm')
    list_of_elements = []
    single_character_operations = set('+-*%^,')
    comparison_operations = set('<=>!')
    numbers = set('.0123456789')
    token = ''
    number_of_brackets = 0
    for element in entered_string:
        if element is '(':
            number_of_brackets += 1
        elif element is ')':
            number_of_brackets -= 1
    if number_of_brackets != 0:
        print("ERROR: the number of opening and closing brackets must match")
        sys.exit(1)
    index = 0
    while index < len(entered_string):
        element = entered_string[index]
        if element in single_character_operations:
            list_of_elements.append(element)
        elif element in comparison_operations:
            if entered_string[index + 1] not in comparison_operations:
                list_of_elements.append(element)
            else:
                token = element + entered_string[index + 1]
                list_of_elements.append(token)
                index += 1
                token = ''
        elif element in numbers:
            token += element
            while index+1 <= len(entered_string)-1 and \
                    entered_string[index+1] in numbers:
                token += entered_string[index+1]
                if index != len(entered_string)-1:
                    index += 1
                else:
                    break
            try:
                if '.' not in token:
                    list_of_elements.append(int(token))
                else:
                    list_of_elements.append(float(token))
                token = ''
            except ValueError:
                print("ERROR: incomprehensible variable")
                sys.exit(1)
        elif element in letters:
            token += element
            index += 1
            element = entered_string[index]
            while len(entered_string) > index + 1 and element in letters:
                token += element
                index += 1
                element = entered_string[index]
            index -= 1
            if token == 'log' and element in numbers:
                index += 1
                while len(entered_string) > index + 1 and element in numbers:
                    token += element
                    index += 1
                    element = entered_string[index]
                index -= 1
            if token != "log" and element is not '(':
                try:
                    math_constant = getattr(math, token)
                    list_of_elements.append(math_constant)
                    token = ''
                except AttributeError:
                    print("ERROR: unknown value " + token)
                    sys.exit(1)
            elif token == "abs" or token == "round":
                list_of_elements.append(token)
            else:
                try:
                    getattr(math, token)
                    list_of_elements.append(token)
                except AttributeError:
                    print("ERROR: unknown function " + token)
                    sys.exit(1)
            token = ''
        elif element == '/':
            if entered_string[index + 1] != '/':
                list_of_elements.append(element)
            else:
                list_of_elements.append('//')
                index += 1
        elif element in "()":
            list_of_elements.append(element)
        index += 1
    return list_of_elements


def get_function(str_function):
    """Accepts the symbolic expression of the operation
    and returns the operation itself
    """
    dictionary = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '%': lambda a, b: a % b,
        '/': lambda a, b: a / b,
        '//': lambda a, b: a // b,
        '^': lambda a, b: a ** b,
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '!=': lambda a, b: a != b,
        '==': lambda a, b: a == b,
        '<=': lambda a, b: a <= b,
        '>=': lambda a, b: a >= b
        }
    if str_function in dictionary.keys():
        return dictionary[str_function]
    else:
        try:
            return getattr(str_function, math)
        except AttributeError:
            print("ERROR: Please, check your expression")
            sys.exit(1)
        except TypeError:
            print("ERROR: Please, check your expression")
            sys.exit(1)


def calculate(notation):
    """Calculates elements written in the form
    of inverse Polish notation.
    """
    index = 2
    while len(notation) > 1:
        try:
            temp = str(notation[index])
        except IndexError:
            print("ERROR: not enough variables")
            sys.exit(1)
        temp = temp.replace('-', '', 1)
        result = 0
        if not temp.replace('.', '', 1).isdigit():
            func = notation.pop(index)
            function = get_function(func)
            try:
                a = notation.pop(index-2)
                b = notation.pop(index-2)
                result = function(a, b)
            except TypeError:
                print("ERROR: for selected elements operation " +
                      func + " doesn't work")
                sys.exit(1)
            notation.insert(index-2, result)
            index = 2
        else:
            index += 1
    try:
        result = notation.pop(0)
        temp = str(result).replace('-', '', 1).replace('.', '', 1)
        if not temp.isdigit or temp in '+-':
            print("ERROR: this is not an expression")
            sys.exit(1)
        return result
    except IndexError:
        print("ERROR: no expression")
        sys.exit(1)


def testing(entered_string):
    """A function that takes an expression as a string
    and returns a result. Not to be confused with main
    """
    list_of_elements = tokenize(entered_string)
    notation = write_in_not(list_of_elements)
    result = calculate(notation)
    return result


def main():
    """Parser get string expression, tokenize() breaks a string into elements,
    write_in_not writes() them in reverse Polish notation
    and calculate() calculates the result.
    """
    parser = argparse.ArgumentParser(
        description='Pure-python command-line calculator.')
    parser.add_argument('EXPRESSION', type=str,
                        help='expression string to evaluate')
    args = parser.parse_args()
    entered_string = args.EXPRESSION
    list_of_elements = tokenize(entered_string)
    notation = write_in_not(list_of_elements)
    result = calculate(notation)
    print(result)
    return result


if __name__ == '__main__':
    main()
