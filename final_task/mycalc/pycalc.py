from mycalc import mymodule

def main():
    a = mymodule.byild_parser().expression
    try:
        a = mymodule.first_foo(a)
        result1 = mymodule.find_brackets(a)
        [compare, result2] = mymodule.find_comparsion(result1)
        if compare:
            logic = True
            for idx, elem in enumerate(compare):
                try:
                    logic *= mymodule.Compare[elem](mymodule.calc(result2[idx]), mymodule.calc(result2[idx+1]))
                except KeyError:
                    raise KeyError('ERROR: unknown compare operator', elem)
            print(bool(logic))
        else:
            s = mymodule.calc(result2[0])
            print(s)
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
