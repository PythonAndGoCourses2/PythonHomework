"""
Provides functions for string formatting.
"""

from .messages import ERROR_MSG_PREFIX


ERROR_PLACE_INDICATOR = '^'


def err_msg_formatter(msg):
    """Return an error message with error prefix."""

    return f'{ERROR_MSG_PREFIX}{msg}'


def err_ctx_formatter(ctx):
    """
    Return a two-line string with a source in the first string
    and a sign in the second one wich indicate
    a place where an error occured.
    """

    source = ctx.source
    pos = ctx.pos

    return '{}\n{}{}'.format(source, ' ' * (pos), ERROR_PLACE_INDICATOR)
