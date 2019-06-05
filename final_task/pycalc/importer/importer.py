"""
Functions for modules importing and module members collecting.
"""

from collections import OrderedDict
from importlib import import_module
from inspect import getmembers
from itertools import chain

from .errors import ModuleImportErrors


UNDERSCORE = '_'


def iter_uniq(iterables):
    """Returns a generator that iterates over unique elements of iterables."""

    return (key for key in OrderedDict.fromkeys(chain(*iterables)))


def import_modules(*iterables):
    """
    Return a list of imported modules.

    Raise an `ModuleImportErrors` exception if at least one of imports fails.
    """

    modules = []
    failed_imports = []

    for module_name in iter_uniq(iterables):

        try:
            module = import_module(module_name)
            modules.append(module)
        except ModuleNotFoundError:
            failed_imports.append(module_name)

    if failed_imports:
        raise ModuleImportErrors(failed_imports)

    return modules


def module_members_by_type(module, type_checker, skip_underscored=True):
    """
    Create a generator over tuples of names and
    members of a certain type in a module.
    """

    for name, member in getmembers(module, type_checker):
        if skip_underscored and name.startswith(UNDERSCORE):
            continue
        yield name, member


def collect_members_by_type(modules, type_checker, skip_underscored=True, predefined=None):
    """Collect members of modules by types into an dictionary."""

    accumulator = dict(predefined) if predefined else {}

    for module in modules:
        for name, member in module_members_by_type(module, type_checker, skip_underscored):
            accumulator[name] = member

    return accumulator
