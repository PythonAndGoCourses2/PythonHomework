"""
"""

# TODO: handle exception when module importing fails

from collections import OrderedDict
from importlib import import_module
from inspect import getmembers
from itertools import chain

UNDERSCORE = '_'


def iter_uniq(iterables):
    """
    Returns a generator that iterates over unique elements of iterables.
    """

    return (key for key in OrderedDict.fromkeys(chain(*iterables)))


def import_modules(*iterables):
    """"""

    modules = []

    for module_name in iter_uniq(iterables):

        try:
            module = import_module(module_name)
            modules.append(module)
        except ModuleNotFoundError:
            raise ModuleNotFoundError

    return modules


def module_members_by_type(module, type_checker, skip_underscored=True):
    """"""

    for name, member in getmembers(module, type_checker):
        if skip_underscored and name.startswith(UNDERSCORE):
            continue
        yield name, member


def collect_members_by_type(modules, type_checker, skip_underscored=True, predefined=None):
    """"""

    accumulator = dict(predefined) if predefined else {}

    for module in modules:
        for name, member in module_members_by_type(module, type_checker, skip_underscored):
            accumulator[name] = member

    return accumulator
