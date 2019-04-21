from mycalc import mymodule


def main():
    a = mymodule.byild_parser().expression
    try:
        a = mymodule.first_function(a)
        result1 = mymodule.find_brackets(a)
        compare = mymodule.find_comparsion(result1)
        total = mymodule.calc_logical(compare)
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
