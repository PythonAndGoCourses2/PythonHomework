""""""

from importlib import import_module
from inspect import getmembers

NUMERIC_TYPES = (int, float, complex)
UNDERSCORE = '_'

module_names = ['math']


def is_numeric(obj) -> bool:
    """Return `True` if a object is instance of numeric types"""

    return isinstance(obj, (NUMERIC_TYPES))


# def is_callable(obj) -> bool:
#     """Return `True` if a object is callable"""

#     return callable(obj)


def starts_with_underscore(string: str):
    """"""
    return string.startswith(UNDERSCORE)


def importing_module(name):
    """"""
    return import_module(name)


m = importing_module('math')


def get_module_members(module, predicat):
    """"""
    return [
        member[0] for member in getmembers(module, predicat)
        if not starts_with_underscore(member[0])
    ]

    # return members
    # members = getmembers(module, predicat)
# def get_members(module_name):


from pprint import pprint
pprint(get_module_members(m, is_numeric))
pprint(get_module_members(m, callable))
