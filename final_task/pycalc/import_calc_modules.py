#!/usr/bin/env python3

"""
The module contains functions for importing args from the modules which received in the list.
Use import_calc_modules.import_modules(list_of_modules_names: list).
"""


import importlib.util


BUILTIN_CALC_MODULES = ("math", )
BUILTIN_CALC_ATTRS = (
    ("abs", abs),
    ("round", round),
)


class ImportCalculatorModulesError(ImportError):
    pass


def _check_module(module_name: str):
    """
    Check possibility of importing the module using its name.
    Take module_name as str like "math", "random", etc.
    Return a module_spec if possible else raise exception.
    """
    module_spec = importlib.util.find_spec(module_name)
    if module_spec is None:
        raise ImportCalculatorModulesError(f"module \"{module_name}\" not found")
    else:
        return module_spec


def _import_module_from_spec(module_spec):
    """
    Import the module from module_spec. Return a module as object.
    """
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def _parse_module(module):
    """
    Parse received module for non-private attributes.
    Take: module as object.
    Return:  dict: {"name_of_func_or_const": func_or_const_as_an_object, ...}.
    """
    row_attrs_strings = dir(module)
    filt_attrs_strings = tuple(filter(lambda attr: not attr.startswith("_"), row_attrs_strings))
    filt_attrs_objects = (getattr(module, attr_str) for attr_str in filt_attrs_strings)
    attrs_dict = {attr_str: attr for attr_str, attr in zip(filt_attrs_strings, filt_attrs_objects)}
    return attrs_dict


def import_modules(list_of_modules_names: list):
    """
    Import modules from list with module names.
    Take: list_of_modules_names: list  ( ["random", "cmath",...] )
    Return:  tuple: ({math_func_name: math_func_obj,...}, {math_const_name: math_const_obj,...}
    """
    importing_modules = list(BUILTIN_CALC_MODULES)
    importing_modules.extend(list_of_modules_names)

    math_attrs = dict(BUILTIN_CALC_ATTRS)

    for module in importing_modules:
        module_spec = _check_module(module)
        module = _import_module_from_spec(module_spec)
        module_attrs = _parse_module(module)
        math_attrs.update(module_attrs)

    math_funcs = {name: obj for name, obj in math_attrs.items() if callable(obj)}
    math_consts = {name: obj for name, obj in math_attrs.items() if not callable(obj)}

    return math_funcs, math_consts


if __name__ == "__main__":
    print(__doc__)
