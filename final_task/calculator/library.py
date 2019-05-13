# -*- coding: utf-8 -*-
"""
The module is designed for dynamic creation of module libraries.

Example:
        lib = Library('math', 'os')
        lib.update('time', 'os')

        lib['e']
        >>> 2.718281828459045

        lib['sum'](5, 10)
        >>> 15
"""


class Library(dict):
    """
    Class is designed to work with modules.
    It is a dictionary of functions and constants.
    """
    def __init__(self, *modules: list):
        super().__init__()

        self['abs'] = abs
        self['round'] = round

        self.update(*modules)

    def update(self, *modules: list):
        """Adds functions and veriables from got module names to dictionary."""
        for module in modules:
            super().update(__import__(module).__dict__)
