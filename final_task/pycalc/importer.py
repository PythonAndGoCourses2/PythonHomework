""""""
# TODO: exception when import fails

from collections import OrderedDict
from functools import partial
from importlib import import_module
from inspect import getmembers
from types import BuiltinFunctionType, FunctionType, LambdaType


NUMERIC_TYPES = (int, float, complex)
FUNCTION_TYPES = (BuiltinFunctionType, FunctionType, LambdaType, partial)
UNDERSCORE = '_'

DEFAULT_MODULE_NAMES = ('math',)


def dedupe_to_list(iterable) -> list:
    """"""

    return list(OrderedDict.fromkeys(iterable))


def is_numeric(obj) -> bool:
    """Return `True` if a object is one of numeric types."""

    return isinstance(obj, (NUMERIC_TYPES))


def is_function(obj) -> bool:
    """Return `True` if a object is a function."""

    return isinstance(obj, (FUNCTION_TYPES))


def merge_module_names(module_names: tuple) -> list:
    """"""

    m_names = list(DEFAULT_MODULE_NAMES)
    if module_names:
        m_names.extend(module_names)

    return m_names


def get_module_members_names_by_type(module, type_checker) -> list:
    """"""

    return [
        member[0] for member in getmembers(module, type_checker)
        if not member[0].startswith(UNDERSCORE)
    ]


MEMBER_TYPES = {
    'functions': is_function,
    'constants': is_numeric
}


def get_module_members_names(module):
    """"""

    return {type_: get_module_members_names_by_type(module, type_checker)
            for type_, type_checker in MEMBER_TYPES.items()}


def get(module_names: tuple = None) -> dict:
    """"""

    if not module_names:
        module_names = tuple()

    m_names = merge_module_names(module_names)
    m_names = dedupe_to_list(m_names)

    result = {}

    for module_name in m_names:
        try:
            module = import_module(module_name)
        except ModuleNotFoundError:
            raise ModuleNotFoundError

        members = get_module_members_names(module)
        result[module_name] = {}
        result[module_name]['module'] = module
        result[module_name]['members'] = members

    return result


if __name__ == '__main__':
    MODULE_NAMES = ('calendar', 'pprint')
    from pprint import pprint
    for key, value in get(MODULE_NAMES).items():
        print(key)
        pprint(value)
