"""
Collect maps of module member’s names
to module member’s objects of specified types.
"""

# TODO: handle exception when module importing fails


from functools import partial
from types import BuiltinFunctionType, FunctionType, LambdaType

from pycalc.importer import collect_members_by_type, import_modules


NUMERIC_TYPES = (int, float, complex)
FUNCTION_TYPES = (BuiltinFunctionType, FunctionType, LambdaType, partial)

DEFAULT_MODULE_NAMES = ('math',)
DEFAULT_FUNCTIONS = {'abs': abs, 'round': round}


def is_numeric(obj) -> bool:
    """Return `True` if a object is one of numeric types."""

    return isinstance(obj, (NUMERIC_TYPES))


def is_function(obj) -> bool:
    """Return `True` if a object is a function."""

    return isinstance(obj, (FUNCTION_TYPES))


def build_modules_registry(modules_names):
    """"""

    if not modules_names:
        modules_names = tuple()

    modules = import_modules(DEFAULT_MODULE_NAMES, modules_names)

    functions = collect_members_by_type(modules,
                                        is_function,
                                        predefined=DEFAULT_FUNCTIONS)

    constants = collect_members_by_type(modules,
                                        is_numeric)

    return {"functions": functions, 'constants': constants}
