"""
The exception class for function calling.
"""


class CallError(Exception):
    """
    Raise when a function call throw an exception.

    Wrap built-in exceptions like `ArithmeticError`,
    `OverflowError`, etc.
    """

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
