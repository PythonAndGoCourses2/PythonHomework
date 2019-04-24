from mycalc import mymodule
from mycalc import solve_polynom


SOLVE_FUNCTION = {0: solve_polynom.solve_inf, 1: solve_polynom.solve_number,
                  2: solve_polynom.solv_linear_equation, 3: solve_polynom.solv_quartic_equation,
                  4: solve_polynom.solv_cubic_equation, 5: solve_polynom.solv_four_degree}


def coefficient_expression(list_expression):
    lst_coeff = list(map(lambda x: x.split('*x^'), list_expression))
    for elem in lst_coeff:
        if len(elem) == 1 and 'x' in elem[0]:
            elem[0] = elem[0].replace('*x', '')
            elem = elem.append(1)
    return lst_coeff


def add_null(lst_coeff):
    for elem in lst_coeff:
        if len(elem) == 1:
            elem = elem.append(0)
    return lst_coeff


def calc_list_coeff(list_expression):
    leng = max(list_expression, key=lambda i: i[1])[1] + 1
    list_coeff = ['0'] * leng
    for elem in list_expression:
        list_coeff[elem[1]] = list_coeff[elem[1]] + '+' + elem[0]
    total_list = list(map(mymodule.total_calculation, list_coeff))
    return total_list


def filter_coefficient(list_number):
    total = list(list_number[::-1])
    for elem in list_number[::-1]:
        if elem == 0:
            total.remove(0)
        else:
            break
    return total[::-1]


def get_canonical_polynom(list_number):
    if list_number:
        total_list = [elem / list_number[-1] for elem in list_number]
        return total_list
    else:
        return list_number


def cut_func(list_number):
    total = [0] * len(list_number)
    for idx, elem in enumerate(list_number):
        x = round(elem.real, 3)
        y = round(elem.imag, 3)
        if y == 0:
            total[idx] = x
        else:
            total[idx] = complex(x, y)
    return total


def get_coefficient(expression):
    list_expr = mymodule.plus_reject(expression)
    f = coefficient_expression(list_expr)
    f = add_null(f)
    for elem in f:
        elem[1] = int(elem[1])
    total_list = calc_list_coeff(f)
    return total_list


def total_solve_func(expression):
    expr = mymodule.first_function(expression)
    quantity = expr.count('=')
    if quantity == 0 or quantity > 1:
        raise ValueError('expression is not an equation')
    expr = mymodule.replace_many_plus_minus(mymodule.del_space(expr, '+-'))
    expr = mymodule.find_brackets(expr)
    expr = mymodule.del_space(expr, 'x')
    [left_expr, right_expr] = expr.split('=')
    if left_expr.strip() in '' or right_expr.strip() in '':
        raise ValueError('empty string between =')
    right_expr_list = [''] + mymodule.plus_reject(right_expr)
    left_expr = left_expr + '-'.join(right_expr_list)
    left_coeff = get_coefficient(left_expr)
    f = filter_coefficient(left_coeff)
    total = get_canonical_polynom(f)
    try:
        answer = cut_func(SOLVE_FUNCTION[len(total)](total))
    except KeyError:
        raise KeyError('Oh, I can not solve equations of degree', len(total)-1)
    return answer
