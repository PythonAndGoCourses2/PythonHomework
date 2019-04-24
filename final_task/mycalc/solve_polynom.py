import cmath


def get_canonical_polynom(list_number):
    if list_number:
        total_list = [elem / list_number[-1] for elem in list_number]
        return total_list
    else:
        return list_number


def solve_number(list_number):
    raise ValueError('the equation has no roots')


def solve_inf(list_number):
    raise ValueError('equation is trivial and the solution is any real number')


def solv_linear_equation(list_number):
    total = [-list_number[0] / list_number[1]]
    return total


def solv_quartic_equation(list_number):
    total = [0] * 2
    det = list_number[1] ** 2 - 4 * list_number[0]
    total[0] = (-list_number[1] + det ** 0.5) / 2
    total[1] = (-list_number[1] - det ** 0.5) / 2
    return total


def complex_power(number):
    total = [0] * 3
    phi_0 = cmath.phase(number)
    mod = abs(number) ** (1/3)
    total[0] = complex(number ** (1/3))
    phi_1 = (phi_0 + cmath.tau)/3
    phi_2 = (phi_0 + 2 * cmath.tau)/3
    total[1] = complex(mod * (cmath.cos(phi_1)), mod * cmath.sin(phi_1))
    total[2] = complex(mod * (cmath.cos(phi_2)), mod * cmath.sin(phi_2))
    return total


def get_canonical_cubic_form(list_number):
    total_list = [1] * 3
    total_list[1] = list_number[1] - (list_number[2] ** 2) / 3
    total_list[0] = (2 * list_number[2] ** 3 - 9 * list_number[2] * list_number[1] + 27 * list_number[0]) / 27
    return total_list


def solv_cubic_equation(list_number):
    lst = get_canonical_cubic_form(list_number)
    det = round((lst[1] / 3) ** 3 + (lst[0]/2) ** 2, 3)
    t = - lst[0] / 2 + det ** 0.5
    alpha = complex_power(t)
    beta = [-lst[1] / 3 / elem if elem != 0 else 0 for elem in alpha]
    total = [(alpha[idx] + beta[idx]) - list_number[2] / 3 for idx in range(3)]
    return total


def solv_four_degree(list_number):
    lst = list(list_number)
    edit_list = [1] * 4
    edit_list[0] = (-lst[3] ** 2) * lst[0] + 4 * lst[2] * lst[0] - lst[1] ** 2
    edit_list[1] = lst[3] * lst[1] - 4 * lst[0]
    edit_list[2] = -lst[2]
    root = solv_cubic_equation(edit_list)[0]
    q_list = [0] * 3
    q_list[0] = root ** 2 / 4 - lst[0]
    q_list[1] = lst[3] / 2 * root - lst[1]
    q_list[2] = lst[3] ** 2 / 4 - lst[2] + root
    t = q_list[2] ** 0.5
    q_list = get_canonical_polynom(q_list)
    q_root = solv_quartic_equation(q_list)[0]
    coeff_lst = [1] * 3
    coeff_lst[0] = root / 2 + t * q_root
    coeff_lst[1] = lst[3] / 2 - t
    total = solv_quartic_equation(coeff_lst)
    coeff_lst[0] = root / 2 - t * q_root
    coeff_lst[1] = lst[3] / 2 + t
    total = total + solv_quartic_equation(coeff_lst)
    return total
