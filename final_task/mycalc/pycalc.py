from mycalc import mymodule
from mycalc import equations


def main():
    a = mymodule.byild_parser().EXPRESSION
    init = mymodule.byild_parser().initroot
    try:
        if init:
            roots = equations.total_solve(a, init)
            print('roots of the equation: x_1 = {}'.format(roots[0]))
            for idx, elem in enumerate(roots[1:]):
                print('{:>25}{} = {}'.format('x_', idx+2, elem))
        else:
            total = mymodule.total_calculation(a)
            print(total)
    except ZeroDivisionError:
        print('ERROR: division by zero')
    except TypeError as e:
        print('ERROR:', str(e), sep=' ')
    except KeyError as e:
        x, y = e.args
        print(x, y)
    except ValueError as e:
        print('ERROR: invalid syntax', str(e), sep=' ')
    except IndexError:
        print('ERROR: invalid syntax')
    except OverflowError:
        print('ERROR: overflow')
