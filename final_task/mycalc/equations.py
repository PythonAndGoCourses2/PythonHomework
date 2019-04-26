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


def verifi_expression(expression):
    expr = mymodule.first_function(expression)
    lst = expr.strip().split('=')
    if len(lst) != 2 or '' in lst:
        raise ValueError('expression is not an equation')
    return expr


def total_solve_poly(expression):
    expr = verifi_expression(expression)
    expr = mymodule.find_brackets(expr)
    expr = mymodule.del_space(expr, 'x')
    [left_expr, right_expr] = expr.split('=')
    right_expr_list = [''] + mymodule.plus_reject(right_expr)
    left_expr = left_expr + '-'.join(right_expr_list)
    left_coeff = get_coefficient(left_expr)
    f = filter_coefficient(left_coeff)
    total = get_canonical_polynom(f)
    try:
        answer = cut_func(SOLVE_FUNCTION[len(total)](total))
    except KeyError:
        raise KeyError("Oh, I can't solve equations of degree {}".format(len(total)-1),
                       'but you can specify the initial approximation of the root - INITROOT.')
    return answer


def get_func_value(expression, val):
    expr = expression.replace('x', str(val))
    total = mymodule.total_calculation(expr)
    return total


def find_approximate_root(expression, val):
    expr = verifi_expression(expression)
    lst = expr.split('=')
    x, x_prev, i = val, val + 0.1, 0
    while abs(x - x_prev) >= 1e-7 and i < 1000:
        f_0 = get_func_value(lst[0], x_prev) - get_func_value(lst[1], x_prev)
        f_1 = get_func_value(lst[0], x) - get_func_value(lst[1], x)
        x, x_prev = x - f_1 / (f_1 - f_0) * (x - x_prev), x
        i += 1
    if abs(f_0 - f_1) > 1e-1:
        raise ValueError('Incorrectly chosen initial approximation or equation has no real roots.')
    return [round(x, 10)]


def total_solve(equation, num):
    if type(num) == float:
        root = find_approximate_root(equation, num)
    else:
        root = total_solve_poly(equation)
    return root
