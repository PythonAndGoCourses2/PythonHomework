"""Module for custom exceptions"""


class GeneralError(Exception):
    def __init__(self):
        Exception.__init__(self)


class BracketsError(Exception):
    def __init__(self):
        Exception.__init__(self)


class UnknownFunctionError(Exception):
    def __init__(self, token):
        Exception.__init__(self)
        self.token = token


class InvalidStringError(Exception):
    def __init__(self):
        Exception.__init__(self)

