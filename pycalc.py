#%%
import argparse
from mymodule import first_foo, find_brackets, find_comparsion, calc, Compare

def byild_parser():
    parser=argparse.ArgumentParser(description='Pure-python command line calculator.')
    parser.add_argument('expression', help='expression string to evalute', type=str)
    args = parser.parse_args()
    return args
a = byild_parser().expression
try:
    a = first_foo(a)
    result1 = find_brackets(a)
    [compare,result2] = find_comparsion(result1)
    if len(compare) != 0:
        logic = True
        for idx, elem in enumerate(compare):
            try:
                logic *= Compare[elem](calc(result2[idx]),calc(result2[idx+1]))
            except KeyError:
                raise KeyError('comparsion error', elem)
        print(bool(logic))
    else:
        s = calc(result2[0])
        print(s)
except ZeroDivisionError:
    print('error: division by zero')
except TypeError as e:
    print('error:',str(e),sep=' ')
except KeyError as e:
    x,y = e.args
    print(x,y)
except ValueError as e:
        print('error: invalid syntax',str(e),sep=' ')
except IndexError:
    print('error: invalid syntax')
except OverflowError:
    print('error: overflow')






