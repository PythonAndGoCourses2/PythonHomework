"""
    Test module for check the functionality of supporting of functions
    and constants with  '-m' or '--use-modules' command-line option
"""


def sin():
    """function to check that function from user have higher priority
    than functions from math module"""
    return 42


def user_function():
    """function to check that user function can be added to all functions"""
    return 24


# to check that constant can be added to all functions
CONSTANT = 42
pi = 3.14
