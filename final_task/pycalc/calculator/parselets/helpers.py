"""
Provides helper functions.
"""

from .errors import CallError


def call(ctx, func, args):
    """Call a function with given arguments."""

    try:
        result = func(*args)
    except Exception as exc:
        raise CallError(ctx) from exc

    return result
