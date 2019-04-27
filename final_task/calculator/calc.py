import math
from calculator.validation import check_exception


OPERATION_PRIORITIES = {
    '>': 0, '<': 0, '<=': 0, '==': 0, '!=': 0, '>=': 0,
    '+': 1, '-': 1,
    '*': 2, '/': 2, '%': 2, '//': 2,
    '^': 3,
    '(': 4, ')': 4}


CALCULATE = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '^': lambda x, y: x ** y,
        '//': lambda x, y: x // y,
        '%': lambda x, y: x % y,
        '<': lambda x, y: x < y,
        '>': lambda x, y: x > y,
        '!=': lambda x, y: x != y,
        '==': lambda x, y: x == y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y
    }


DICT_MATH = math.__dict__
DICT_MATH['round'] = round
DICT_MATH['abs'] = abs


def calculate_res_exception(res_expression):
    i = 1
    while i < len(res_expression):
        try:
            if res_expression[i] in OPERATION_PRIORITIES:
                res_expression[i-2] = CALCULATE[res_expression.pop(i)](res_expression[i - 2], res_expression.pop(i - 1))
                i = 1
            if len(res_expression) != 1 and type(res_expression[i]) is str and res_expression[i].isalnum():
                number = res_expression.pop(i-1)
                i -= 1
                args = res_expression[i-number:i]
                res_expression[i] = DICT_MATH[res_expression[i]](*args)
                del res_expression[i-number:i]
                i = 1
        except KeyError:
            return 'ERROR: unknown function'
        except ZeroDivisionError:
            return 'ERROR: division by zero'
        except ValueError:
            return 'ERROR: value'
        except TypeError:
            return 'ERROR: incorrect number of arguments'
        i += 1
    else:
        return res_expression[0]


def allocate_operations(expression, operations, res_expression, item, i):
    if item == '-' and (not i or (expression[i-1] in OPERATION_PRIORITIES and expression[i - 1] != ')')):
        res_expression.append(-1)
        operations.append('*')
    elif item == '+' and (not i or (expression[i - 1] in OPERATION_PRIORITIES and expression[i - 1] != ')')):
        return
    elif operations:
        if item == ')':
            unloading_operations(res_expression, operations, upload_bracket=True)
        else:
            if operations[-1].isalnum() or operations[-1] == '(':
                operations.append(item)
            elif OPERATION_PRIORITIES[item] > OPERATION_PRIORITIES[operations[-1]] or operations[-1] == '(':
                operations.append(item)
            elif item in OPERATION_PRIORITIES.keys() and OPERATION_PRIORITIES[item] == OPERATION_PRIORITIES[
                    operations[-1]] and OPERATION_PRIORITIES[item] == 3:
                operations.append(item)
            else:
                prior_operation = OPERATION_PRIORITIES[item]
                unloading_operations(res_expression, operations, prior_operation)
                operations.append(item)
    else:
        operations.append(item)


def allocate_numbers(expression, res_expression, i):
    if i > 0 and expression[i-1].isdigit() or expression[i-1] == '.':
        res_expression[-1] = res_expression[-1] + expression[i]
    else:
        res_expression.append(expression[i])
    if i == len(expression)-1 or not expression[i+1].isdigit() and expression[i+1] != '.':
        res_expression[-1] = float(res_expression[-1])


def unloading_operations(res_expression, operations, prior_operation=-1, upload_bracket=False):
    while operations and operations[-1] != '(' and not operations[-1].isalnum() \
            and OPERATION_PRIORITIES[operations[-1]] >= prior_operation:
        res_expression.append(operations.pop())
    else:
        if operations and upload_bracket:
            if operations[-1] == '(':
                operations.pop()
            elif operations[-1].isalnum():
                res_expression.append(operations.pop(-2))
                res_expression.append(operations.pop())


def search_func(operations):
    i = len(operations)-1
    while not operations[i].isalnum():
        i = i-1
    return i


def write_func(expression, i):
    func = ''
    while i < len(expression) and expression[i].isalnum():
        func += expression[i]
        i += 1
    return i, func


def translate_reverse_exception(expression):
    res_expression = []
    operations = []
    i = 0
    while i < len(expression):
        if expression[i].isdigit() or expression[i] == '.':
            allocate_numbers(expression, res_expression, i)
        elif expression[i] == ',':
            operations[search_func(operations)-1] += 1
            unloading_operations(res_expression, operations)
        elif i != len(expression)-1 and str(expression[i]) + str(expression[i+1]) in OPERATION_PRIORITIES:
            allocate_operations(expression, operations, res_expression, expression[i] + expression[i+1], i)
            i += 1
        elif expression[i] in OPERATION_PRIORITIES.keys():
            allocate_operations(expression, operations, res_expression, expression[i], i)
        elif expression[i].isalpha():
            i, func = write_func(expression, i)
            if i < len(expression) and expression[i] == '(':

                operations.append(1)
                operations.append(func)
            else:
                try:
                    res_expression.append(DICT_MATH[func])
                    i -= 1
                except KeyError:
                    return ['ERROR: unknown constant']
        else:
            return ['ERROR: unknown character']
        i += 1
    while operations:
        unloading_operations(res_expression, operations, upload_bracket=True)
    return res_expression


def main():
    if check_exception() is None:
        return
    else:
        expression = check_exception()
        res_expression = translate_reverse_exception(expression)
        result = calculate_res_exception(res_expression)
        if type(result) is not float and type(result) is not bool and type(result) is not int:
            print('ERROR: function')
        else:
            print(result)


if __name__ == '__main__':
    main()
