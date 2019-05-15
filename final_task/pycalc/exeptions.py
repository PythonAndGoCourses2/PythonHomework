"""Module for custom exceptions"""


class PycalcException(Exception):
    pass


class GeneralError(PycalcException):
    pass


class BracketsError(PycalcException):
    pass


class UnknownFunctionError(PycalcException):
    def __init__(self, token):
        super().__init__()
        self.token = token


class InvalidStringError(PycalcException):
    pass
