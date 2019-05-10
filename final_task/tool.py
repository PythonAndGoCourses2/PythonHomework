import config
import sys


def arithmetic(a, b, token):
    """Simple calculation."""
    return config.characters[token](a, b)


def functions(token, *args):
    """Calculation math and trigonometry functions."""
    try:
        return config.all_functions[token](*args)
    except KeyError:
        print('ERROR: this function is not supported.!')
        sys.exit(1)
    except TypeError:
        print('ERROR: invalid number of arguments!')
        sys.exit(1)
    except ValueError:
        print('ERROR: incorrect value!')
        sys.exit(1)
    except OverflowError:
        print('ERROR: results that overflow!')
        sys.exit(1)


def constants_calculation(token):
    """Return the value of a constant."""
    return config.constants[token]


def comparison_calculation(a, b, token):
    """Calculation simple logic expression."""
    return config.comparison[token](a, b)


def object_type(obj):
    """Sets various objects to data types for calculations."""
    try:
        if type(obj) == str:
            if obj[0] == '[':
                array = []
                for token in obj:
                    if token.isdigit():
                        array.append(object_type(token))
                return array
            elif obj == 'True' or obj == 'False':
                return bool(obj)
            elif '.' in obj:
                return float(obj)
            return int(obj)
        return obj
    except ValueError:
        print('ERROR: unknown object - ' + obj)
        sys.exit(1)


def pop_calculated_items(array, first_index, second_index, length):
    """
    Pulls out items to replace them with calculated ones.

    Description: Due to the complexity of the operation of cyclical pulling elements by indexes(O(n)).
    Implemented an automatic change of the following array elements to the offset delta.
    """
    index = first_index
    for token in array[second_index:]:
        array[index] = token
        index += 1
    for i in range(length):
        array.pop()
    return array


def replace_minus_and_negative_numbers(array):
    """
    Technical function. Replaces all the disadvantages in a simple expression by a plus,
    and the value makes it negative. In order to equate the priority of minus and plus.

    Example: 2-1+3 = -2 -->  2+(-1)+3 = 4
    """
    for idx, token in enumerate(array):
        if token == '-' and array[idx+1][-1].isdigit():
            array[idx] = '+'
            array[idx+1] = str(-object_type(array[idx+1]))
    return array
