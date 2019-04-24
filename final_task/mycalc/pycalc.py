from mycalc import mymodule
from mycalc import equations


def main():
    a = mymodule.byild_parser().EXPRESSION
    try:
        if mymodule.byild_parser().use_module:
            total = equations.total_solve_func(a)
            print('polynomial roots:')
            for idx, elem in enumerate(total):
                print('x_' + str(idx + 1) + ' =', elem)
        else:
            total = mymodule.total_calculation(a)
            print('Answer is:', total)
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
