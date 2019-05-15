import math as m
"""
   This calculator is written using the recursive descent method.
   Frequently encountered variables:
   eval_string - a string that contains a mathematical expression needed to calculate
   index - the number of the character in eval_string on which function finished working
"""

# Dictionary that contains functions' name as a key and math library functions plus abs and round as a value
func_dictionary = dict([(attr, getattr(m, attr)) for attr in dir(m) if callable(getattr(m, attr))])
func_dictionary['abs'] = abs
func_dictionary['round'] = round


def skip_space(eval_string, index):
    """
        Returns the position of first met non-space symbol
    """
    while index < len(eval_string) and eval_string[index] == ' ':
        index += 1
    if index > len(eval_string):
        raise ValueError("ERROR: invalid argument")
    return index


def call_func_with_args(Func, Args):
    """
        Calls function with arguments
        Func - function to be called
        Args - list of function arguments
    """
    return Func(*Args)


def get_func_arguments(eval_string, index):
    """
        Reads function arguments from a string
        Called only if function is found
        Returns a tuple that contains a list of function arguments and a position where function finished working
    """
    arguments = []
    while index < len(eval_string) and eval_string[index] != ')':
        temp = solve_equality(eval_string, index)
        index = temp[1]
        index = skip_space(eval_string, index)
        if index < len(eval_string) and eval_string[index] not in (',', ')'):
            raise ValueError("ERROR: no commma")
        elif index < len(eval_string) and eval_string[index] == ',':
            index += 1
        arguments.append(temp[0])
    if index < len(eval_string) and eval_string[index] == ')':
        return arguments, index
    else:
        raise ValueError('ERROR: no closing bracket')


def error(args):
    """
       Used only once in line 171 when a function is searched by its name in the function dictionary.
       If function with specified name is not found, this function will be called.
    """
    raise Exception("ERROR: no func with that name")


def search_float(eval_string, index):
    """
       Reads number from a string
       Returns a turple that contains integer or float number and a position where function finished working
    """
    num = ""
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == '-':
        num = '-'
        index += 1
    index = skip_space(eval_string, index)
    while index < len(eval_string):
        if eval_string[index].isdigit():
            num += eval_string[index]
            index += 1
        elif (eval_string[index].isalpha()):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        else:
            break
    if (index < len(eval_string) and eval_string[index] == '.'):
        num += eval_string[index]
        index += 1
        while index < len(eval_string):
            if eval_string[index].isdigit():
                num += eval_string[index]
                index += 1
            else:
                break
        return (float(num), index)
    else:
        return (int(num), index)


def get_bracket(eval_string, index):
    """
       Calculates mathematical expression in brackets
       Called only if brackets are found
       Returns a turple that contains expression result and a position where function finished working
    """
    result, num1 = 0, 0
    index += 1
    result, index = solve_equality(eval_string, index)
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == ')':
        index += 1
        return result, index
    else:
        raise ValueError("ERROR: invalid argument on position {}".format(index))


def number_sign(eval_string, index):
    """
       Reads the number sign (+ and -) from the string
       It's purpose is to calculate expressions of the form +-+---+mathematical_expression
       Returns a turple that contains expression result and a position where function finished working
    """
    if eval_string[index] == '+':
        index += 1
        if index >= len(eval_string):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        result, index = get_variable(eval_string, index)
    elif eval_string[index] == '-':
        index += 1
        if index >= len(eval_string):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        result, index = get_variable(eval_string, index)
        result *= -1
    return result, index


def get_variable(eval_string, index):
    """
       Reads a mathematical object from a string
       And depending on its type, it transfers control to another function
       And takes the result of the work of that function
       Returns a turple that contains expression result and a position where function finished working
    """
    index = skip_space(eval_string, index)
    variable = ""
    if index < len(eval_string) and (eval_string[index].isdigit() or eval_string[index] == '.'):
        variable, index = search_float(eval_string, index)
        index = skip_space(eval_string, index)
        if index < len(eval_string) and eval_string[index] not in (
                                           '+', '-', '*', '/', '%', '^',
                                           '>', '<', '=', ')', '!', ','
                                           ):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
    elif index < len(eval_string) and eval_string[index] in ('-', '+'):
        variable, index = number_sign(eval_string, index)
    elif index < len(eval_string) and eval_string[index] == '(':
        variable, index = get_bracket(eval_string, index)
    elif index < len(eval_string) and eval_string[index].isalpha():
        math_object = ""
        while index < len(eval_string) and (eval_string[index].isalpha() or eval_string[index].isdigit()):
            math_object += eval_string[index]
            index += 1
        if (math_object == 'pi'):
            variable = m.pi
        elif (math_object == 'e'):
            variable = m.e
        elif (math_object == 'tau'):
            variable = m.tau
        else:
            if index < len(eval_string) and eval_string[index] == '(':
                index += 1
                tmp = get_func_arguments(eval_string, index)
                variable = call_func_with_args(func_dictionary.get(math_object.lower(), error), tmp[0])
                index = tmp[1]
                if index < len(eval_string) and eval_string[index] == ')':
                    index += 1
                    index = skip_space(eval_string, index)
            else:
                raise ValueError("ERROR: Invalid argument (index {})".format(index))
    elif index < len(eval_string) and eval_string[index] == ',':
        return variable, index
    else:
        raise ValueError("ERROR: invalid argument on position {}".format(index))
    return (variable, index)


def get_degree(eval_string, index):
    """
       Performs an exponentiation.
       Each expression is treated as "expression1 mathematical_operator expression2"
       It calculates expression1 and if mathematical_operator is ^ it calculates expression2
       And performs expression1 ^ expression2, or returns result of expression1 if operator is not ^
    """
    result, num1, index = 0, 0, skip_space(eval_string, index)
    result, index = get_variable(eval_string, index)
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] == '^':
        index += 1
        num1, index = get_degree(eval_string, index)
        if (result == 0 and num1 == 0):
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        result **= num1
        index = skip_space(eval_string, index)
    return result, index


def multiply(eval_string, index):
    """
       Performs ("*", "/", "%", "//") operations
       Each expression is treated as "expression1 mathematical_operator expression2"
       It calculates expression1 and if mathematical_operator is in ("*", "/", "%", "//") it calculates expression2
       And performs "expression1 ("*", "/", "%", "//") expression2", or returns result of expression1
    """
    mult, num1, index = 1, 0, skip_space(eval_string, index)
    mult, index = get_degree(eval_string, index)
    index = skip_space(eval_string, index)
    while index < len(eval_string) and eval_string[index] in ("*", "/", "%"):
        number_sign = ""
        while eval_string[index] in ("*", "/", "%"):
            number_sign += eval_string[index]
            index += 1
        num1, index = get_degree(eval_string, index)
        if (number_sign == '*'):
            mult *= num1
        elif (number_sign == '/'):
            mult /= num1
        elif (number_sign == "//"):
            mult //= num1
        elif (number_sign == '%'):
            mult %= num1
        else:
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        index = skip_space(eval_string, index)
    return mult, index


def add_math_objects(eval_string, index):
    """
       Performs ("+", "-") operations
       Each expression is treated as "expression1 mathematical_operator expression2"
       It calculates expression1 and if mathematical_operator is in ("+", "-") it calculates expression2
       And performs "expression1 ("+", "-") expression2", or returns result of expression1
    """
    total, num1 = 0, 0
    total, index = multiply(eval_string, index)
    index = skip_space(eval_string, index)
    while index < len(eval_string) and eval_string[index] in ("+", "-"):
        number_sign = eval_string[index]
        index += 1
        num1, index = multiply(eval_string, index)
        if(number_sign == '+'):
            total += num1
        elif(number_sign == '-'):
            total -= num1
        index = skip_space(eval_string, index)
    return total, index


def solve_equality(eval_string, index):
    """
       Performs (">", "==", "<", "!=", ">=", "<=") operations
       Each expression is treated as "expression1 mathematical_operator expression2"
       It calculates expression1 and if mathematical_operator is in (">", "==", "<", "!=", ">=", "<=")
       It calculates expression2 and performs "expression1 ">", "==", "<", "!=", ">=", "<=") expression2"
       Or returns result of expression1
    """
    num1, num2, number_sign = 0, 0, ""
    num1, index = add_math_objects(eval_string, index)
    index = skip_space(eval_string, index)
    if index < len(eval_string) and eval_string[index] not in (">", "=", "<", "!", ")", ","):
        raise ValueError("ERROR: invalid argument on position {}".format(index))
    while index < len(eval_string) and eval_string[index] in (">", "=", "<", "!"):
        while index < len(eval_string) and eval_string[index] in ('>', '=', '<', '!'):
            number_sign += eval_string[index]
            index += 1
        num2, index = add_math_objects(eval_string, index)
        if (number_sign == '>='):
            result = (num1 >= num2)
        elif (number_sign == '>'):
            result = (num1 > num2)
        elif (number_sign == '=='):
            result = (num1 == num2)
        elif (number_sign == '<'):
            result = (num1 < num2)
        elif (number_sign == '<='):
            result = (num1 <= num2)
        elif (number_sign == '!='):
            result = (num1 != num2)
        else:
            raise ValueError("ERROR: invalid argument on position {}".format(index))
        return result, index
    return num1, index


def solve(eval_string, index=0):
    """
        Calculates a mathematical expression.
        Called once at the very beginning of program
    """
    index = skip_space(eval_string, index)
    if index >= len(eval_string):
        raise ValueError("ERROR: invalid argument on position {}".format(index))
    result, index = solve_equality(eval_string, index)
    return result
