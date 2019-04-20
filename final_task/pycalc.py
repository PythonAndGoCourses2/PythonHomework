import math

operationPriorities = {
    '>': 0, '<': 0, '<=': 0, '==': 0, '!=': 0, '>=': 0,
    '+': 1, '-': 1,
    '*': 2, '/': 2, '%': 2, '//': 2,
    '^': 3,
    '(': 4, ')': 4}

func_math = math.__dict__
func_math['round'] = round
func_math['abs'] = abs


def translate_operations(operation, x, y):
    calculate = {
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
    return calculate[operation](x, y)


# если оператор сравнение то удалять -2 и сам знак а True помещать в список
def calculate_res_exception(res_expression):
    i = 1
    while i < len(res_expression):
        if res_expression[i] in operationPriorities:
            res_expression[i] = translate_operations(
                res_expression[i], res_expression[i-2], res_expression[i-1])
            del res_expression[i-1]
            del res_expression[i-2]
            i = 1
        if len(res_expression) != 1 and type(res_expression[i]) is str and res_expression[i].isalnum():
            number = res_expression[i-1]
            del res_expression[i-1]
            i -= 1
            args = res_expression[i-number:i]
            res_expression[i] = func_math[res_expression[i]](*args)
            del res_expression[i-number:i]
            i = 1
        i += 1
    else:
        return res_expression[0]


def read_math_func(expression, i):
    func = ''
    while expression[i] not in operationPriorities and i != -1:
        func += expression[i]
        i -= 1
    return func[::-1]


def allocate_operations(expression, operations, res_expression, item, i):
    if item == '-' and not i or (expression[i-1] in operationPriorities and expression[i-1] != ')'):
        res_expression.append(-1)
        operations.append('*')
    elif item == '(' and i and expression[i-1] not in operationPriorities:
        operations.append(1)
        operations.append(read_math_func(expression, i-1))
    elif operations:
        if item == ')':
            unloading_operations(res_expression, operations, upl_bracket=True)
        else:
            if operations[-1].isalnum() or operationPriorities[item] > operationPriorities[operations[-1]] or operations[-1] == '(':
                operations.append(item)
            else:
                prior_oper = operationPriorities[item]
                unloading_operations(res_expression, operations, prior_oper)
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


def unloading_operations(res_expression, operations, prior_oper=-1, upl_bracket=False):
    while operations and operations[-1] != '(' and not operations[-1].isalnum() and operationPriorities[operations[-1]] >= prior_oper:
        res_expression.append(operations[-1])
        del operations[-1]
    else:
        if operations and upl_bracket:
            if operations[-1] == '(':
                del operations[-1]
            elif operations[-1].isalnum():
                res_expression.append(operations[-2])
                res_expression.append(operations[-1])
                del operations[-1]
                del operations[-1]


beginningRepetitiveOperators = ('!', '=', '>', '<')

def increase_number_parameters(operations):  # переделать алгоритм
    i = len(operations)-1
    if operations[-1].isalnum():
        operations[i-1] += 1
    else:
        while not operations[i].isalnum() and i != -1:
            i = -1
        else:
            operations[i-2] += 1


def translate_reverse_exception(expression, operations, res_expression):
    for i, item in enumerate(expression):
        if item in operationPriorities.keys():
            allocate_operations(expression, operations, res_expression, item, i)
        elif item.isdigit() or item == '.':
            allocate_numbers(expression, res_expression, i)
        elif item == ',':
            increase_number_parameters(operations)
            unloading_operations(res_expression, operations)
        elif item == 'e':
            res_expression.append(func_math[item])
        elif i!=len(expression)-1:
            if str(item) + str(expression[i+1]) == 'pi':
                res_expression.append(func_math[item + expression[i+1]])
            else:
                if str(item) + str(expression[i+1]) in operationPriorities:
                    allocate_operations(expression, operations, res_expression, item + expression[i+1], i)
    unloading_operations(res_expression, operations)


def main():
    expression = 'round(-5.4)'
    operations = []
    res_expression = []
    translate_reverse_exception(expression, operations, res_expression)
    print(res_expression)
    result = calculate_res_exception(res_expression)
    print(result)

main()
