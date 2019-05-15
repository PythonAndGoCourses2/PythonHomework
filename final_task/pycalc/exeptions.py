"""Module for custom exceptions"""


class PycalcException(Exception):
    pass


class GeneralError(PycalcException):
    pass


class BracketsError(PycalcException):
    pass


class UnknownFunctionError(PycalcException):
    pass


class InvalidStringError(PycalcException):
    pass
