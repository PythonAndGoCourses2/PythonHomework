"""
The exception class for function calling.
"""


class CallError(Exception):
    """An exception for function calling."""

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
