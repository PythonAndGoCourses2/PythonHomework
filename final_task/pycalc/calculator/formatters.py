"""
Provides functions for string formatting.
"""

from .messages import (
    ERROR_PLACE_INDICATOR,
    MODULES_IMPORT_ERROR,
)


def ctx_formatter(ctx):
    """
    Return a two-line string with a source in the first line
    and a sign in the second one which indicate
    a place where an error occured.
    """

    source = ctx.source
    pos = ctx.pos

    return '{}\n{}{}'.format(source, ' ' * (pos), ERROR_PLACE_INDICATOR)


def err_msg_with_ctx_formatter(msg, ctx):
    """Return an error message with context information."""

    ctx_msg = ctx_formatter(ctx)

    return f'{msg}\n{ctx_msg}'


def err_modules_import_formatter(modules_names):
    """Return an error message for module imports errors."""

    modules_names = ', '.join(modules_names)

    return f'{MODULES_IMPORT_ERROR} {modules_names}'
