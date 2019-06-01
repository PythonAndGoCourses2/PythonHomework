#!/usr/bin/env python3

"""
The module contains functions to solve mathematical expressions.
Use expression_parser.calculate(expression: str).
"""


import re
from collections import namedtuple
import operator


__C_REGEXP_BRACKETS = re.compile(r"[(]|[)]")
__C_REGEXP_BRACKET_UNARY_PLUSMINUS = re.compile(r"[*%^(,][+\-]|[/=!<>]+[+\-]")
__C_REGEXP_DOUBLED_PLUSMINUS = re.compile(r"[+\-]{2,}")
__C_REGEXP_OPERATOR_THEN_PLUSMINUS = re.compile(r"[*%^][+\-]|[/=!<>]{1,2}[+\-]")
__C_REGEXP_BEFORE_BRACKET = re.compile(r"[a-zA-Z]*[\d]*(?=[(])")
__C_REGEXP_AFTER_BRACKET = re.compile(r"(?<=[)])[a-zA-Z]*[\d]*")
__C_REGEXP_EXPONENTIATION = re.compile(r"[\^]")
__C_REGEXP_TOKENS = re.compile(r"[\-+][#]|[+\-*%^()]|[/=!<>]+|[a-zA-Z]+[\d]*|[\d]*[.][\d]+|[\d]+|[,]")


__operator_func_priority = namedtuple("Operator", ["function", "args", "priority"])
__OPERATORS = {
    "==": __operator_func_priority(operator.eq, 2, 0),
    "!=": __operator_func_priority(operator.ne, 2, 0),
    "<>": __operator_func_priority(operator.ne, 2, 0),

    "<=": __operator_func_priority(operator.le, 2, 0),
    "<": __operator_func_priority(operator.lt, 2, 0),
    ">": __operator_func_priority(operator.gt, 2, 0),
    ">=": __operator_func_priority(operator.ge, 2, 0),

    "+": __operator_func_priority(operator.add, 2, 1),
    "-": __operator_func_priority(operator.sub, 2, 1),

    "*": __operator_func_priority(operator.mul, 2, 2),
    "/": __operator_func_priority(operator.truediv, 2, 2),
    "//": __operator_func_priority(operator.floordiv, 2, 2),
    "%": __operator_func_priority(operator.mod, 2, 2),

    "+#": __operator_func_priority(operator.pos, 1, 3),
    "-#": __operator_func_priority(operator.neg, 1, 3),

    "^": __operator_func_priority(operator.pow, 2, 4)
}

math_funcs = {}
math_consts = {}  # these variables are changed by the external module (pycalc)


class ExpressionParserError(Exception):
    pass


def _are_brackets_balanced(expression: str):
    """
    Check whether brackets are balanced.
    Take:  expression: str.
    Return:  True, if brackets are balanced, else return False.
    Example:
        "1+1" -> True
        "(1+1)" -> True
        "(1+1))" -> False
        ")(1+1)(" -> False
    """
    if "(" not in expression and ")" not in expression:
        return True

    if expression.count("(") != expression.count(")"):
        return False

    first_bracket_match = __C_REGEXP_BRACKETS.match(expression)
    if first_bracket_match and first_bracket_match.group() == ")":
        return False

    last_bracket_match = __C_REGEXP_BRACKETS.match(expression[::-1])
    if last_bracket_match and last_bracket_match.group() == "(":
        return False

    return True


def _is_number(value: str):
    """
    Check if the value is a number (can be converting to a floating-point value).
    Take:  value: str
    Return True if the value is a number, else return False.
    """
    try:
        float(value)
    except ValueError:
        return False
    return True


def _are_operators_and_operands_correct(expression: str):
    """
    Checks expression for correctness of operators and operands:
        Checks for denied whitespaces: "1! =1", "1/ /1", "1+1 1+1".
        Checks for denied operator location: "1-//1", "1//*1".
        Checks for impossible/nonexistent operands: "pi1", "1pi"
    Take:  expression: str
    Return:  True, if all correct, else returns False.
    Example:
        "1*-1" -> True.
        "1*/1" -> False.
        "1* -1" -> True.
        "1/ /-1" -> False.
        "1 // -1" -> True.
        "1-//1" -> False.
        "1+.1 1-1" -> False.
        "1+.11-1" -> True.
        "1+pi" -> True.
        "pi+1" -> True.
        "1pi" -> False.
        "pi1" -> False.
        "log10(10) -> True.
    """
    operator_symbols = set(__OPERATORS.keys())
    operator_symbols.update("".join(__OPERATORS.keys()))
    operator_symbols_without_plusminus = operator_symbols.copy()
    operator_symbols_without_plusminus.difference_update({"+", "-"})

    math_attr_names = set(math_funcs.keys())
    math_attr_names.update(math_consts.keys())

    possible_tokens = operator_symbols.copy()
    possible_tokens.update(math_attr_names)
    possible_tokens.update({"(", ")", ","})

    last_token = ""
    tokens = __C_REGEXP_TOKENS.finditer(expression)

    for token in tokens:
        token = token.group()

        if token in operator_symbols_without_plusminus and last_token in operator_symbols:
            return False

        elif _is_number(token) or token in math_attr_names:
            if _is_number(last_token) or last_token in math_attr_names:
                return False

        elif not _is_number(token) and token not in possible_tokens:
            return False

        last_token = token

    return True


def _are_no_missing_operators_next_to_brackets(expression: str):
    """
    Checks for missing operators next to brackets.
    Take:  expression: str.
    Return:  True, if there are no missing operators in the expression, else returns False.
    Example:
        "1(1+1)" -> False.
        "1+(1+1)" -> True.
        "(1+1)sin(1) -> False.
        "pi(1+1) -> False.
        "sin(pi)" -> True.
    """
    before_bracket_matches = __C_REGEXP_BEFORE_BRACKET.findall(expression)
    for match in before_bracket_matches:
        if match and match not in math_funcs:  # match may be '', but this is not a missed operator.
            return False

    after_bracket_matches = __C_REGEXP_AFTER_BRACKET.findall(expression)
    for match in after_bracket_matches:
        if match:
            return False

    return True


def _remove_whitespaces(expression: str):
    """
    Remove all whitespaces from string.
    Take:  expression: str.
    Return:  expression: str.
    """
    return ''.join(expression.split())


def _squash_doubled_plusminus(expression: str):
    """
    Squashing combined add/sub operators.
    Take:  expression: str.
    Return:  expression: str.
    Example:
        "---+1" -> "-1".
        "--+1" -> "+1".
    """
    expression_chars = list(expression)
    doubled_plusminus_matches = __C_REGEXP_DOUBLED_PLUSMINUS.finditer(expression)

    shift = 0
    for match in doubled_plusminus_matches:
        start_index, end_index = match.span()
        match_operators = match.group()
        output_operator = "-" if match_operators.count("-") % 2 else "+"
        expression_chars[start_index-shift:end_index-shift] = output_operator
        shift = end_index - start_index - 1

    return "".join(expression_chars)


def _differentiate_unary_plusminus(expression: str):
    """
    Find unary plus/minus operators and differentiate them from binary plus/minus operators.
    Take:  expression: str.
    Return:  expression: str.
    Example: "-3*-pow(1+1,-2-1)" -> -#3-#pow(1+1,-#2-1).
    """
    expression_chars = list(expression)
    bracket_unary_plusminus_matches = __C_REGEXP_BRACKET_UNARY_PLUSMINUS.finditer(expression)

    shift = 0

    if expression_chars[0] in {"+", "-"}:
        expression_chars.insert(1, "#")
        shift += 1

    for match in bracket_unary_plusminus_matches:
        end_index = match.end()
        expression_chars.insert(end_index+shift, "#")
        shift += 1
    return "".join(expression_chars)


def _bracket_exponentiation_wrapper(expression: str):
    """
    Add extra brackets for correct calculation of expression with exponentiation operator.
    (Exponentiation operator is the only right-to-left associativity operator).
    Take:  expression: str.
    Return:  expression: str.
    Example:
        "2^2^2^2^2" -> "2^(2^(2^(2^(2))))".
        "2^-#2^-#2" -> "2^(-#2^(-#2))".
    """
    expression_chars = list(expression)

    breaking_tokens = set(__OPERATORS.keys())
    breaking_tokens.add(",")
    breaking_tokens.difference_update({"^", "-#", "+#"})
    unary_tokens = {"^+#", "^-#"}

    shift = 0
    delayed_shift_indexes = list()
    delayed_shift_indexes_to_remove = list()

    exponentiation_matches = __C_REGEXP_EXPONENTIATION.finditer(expression)
    for exponentiation_match in exponentiation_matches:
        opened_brackets = 0
        exponentiation_end_index = exponentiation_match.end()
        exponentiation_string = exponentiation_match.group()

        for delayed_shift_index in delayed_shift_indexes:
            if exponentiation_end_index >= delayed_shift_index:
                shift += 1
                delayed_shift_indexes_to_remove.append(delayed_shift_index)
        for delayed_shift_index_to_remove in delayed_shift_indexes_to_remove:
            delayed_shift_indexes.remove(delayed_shift_index_to_remove)
        delayed_shift_indexes_to_remove.clear()

        if exponentiation_string in unary_tokens:
            expression_chars.insert(exponentiation_end_index+shift-2, "(")
            shift += 1
        expression_chars.insert(exponentiation_end_index+shift, "(")
        shift += 1

        token_matches = __C_REGEXP_TOKENS.finditer(expression, exponentiation_end_index)
        for token_match in token_matches:
            token_index = token_match.start()
            token_string = token_match.group()

            if token_string == "(":
                opened_brackets += 1
            elif token_string == ")":
                opened_brackets -= 1

            if opened_brackets < 0 or (not opened_brackets and token_string in breaking_tokens):
                break
        else:
            token_index = token_match.end()

        expression_chars.insert(token_index+shift, ")")
        delayed_shift_indexes.append(token_index)

        if exponentiation_string in unary_tokens:
            expression_chars.insert(token_index+shift+1, ")")
            delayed_shift_indexes.append(token_index+1)

    return "".join(expression_chars)


def _tokenizer(expression: str):
    """
    Parse expression for tokens.
    Take:  expression: str.
    Return:  iterator with token values.
    """
    token_matches = __C_REGEXP_TOKENS.finditer(expression)
    for token in token_matches:
        yield token.group()


def _token_handler(parsed_expression: iter):
    """
    Handle tokens from tokenizer and return tokens using reverse polish notation.
    Can be used recursively with _function_handler-method.
    Take:  parsed_expression: iter  (from _tokenizer-method).
    Return:  iterator with token values in reverse polish notation.
    """
    stack = []
    func_stack = []
    func_brackets = 0

    for token in parsed_expression:
        if token in math_funcs:
            func_brackets += 1
            func_stack.append(token)
        elif func_brackets:
            if token == "(" and func_stack[-1] not in math_funcs:
                func_brackets += 1
            elif token == ")":
                func_brackets -= 1
            func_stack.append(token)

            if not func_brackets:
                func_expression = "".join(func_stack)
                func_stack.clear()
                yield _function_handler(func_expression)

        elif token in __OPERATORS:
            while stack and stack[-1] != "(" and \
                    __OPERATORS[token].priority <= __OPERATORS[stack[-1]].priority:
                yield stack.pop()
            stack.append(token)
        elif token == ")":
            while stack:
                x = stack.pop()
                if x == "(":
                    break
                yield x
        elif token == "(":
            stack.append(token)
        elif token in math_consts:
            yield math_consts[token]
        elif _is_number(token):
            yield float(token)
        else:
            raise ExpressionParserError("invalid expression")
    while stack:
        yield stack.pop()


def _function_handler(function_expression: str):
    """
    Handle function with attributes in string and call it.
    Can be used recursively with _token_handler-method.
    Take:  function_expression.
    Return:  value from called function.
    Example:
        "sin(pi/2)" -> 1.0.
        "pow(2,8)"-> 256.0.
    """
    func, args = function_expression.split("(", 1)
    args = args[:-1]

    buffer = []
    args_list = []
    func_brackets = 0

    tokens = _tokenizer(args)
    for token in tokens:
        if token in math_funcs:
            func_brackets += 1
            buffer.append(token)
        elif token == "(" and buffer and buffer[-1] not in math_funcs:
            func_brackets += 1
            buffer.append(token)
        elif token == ")":
            func_brackets -= 1
            buffer.append(token)
        elif func_brackets:
            buffer.append(token)
        elif not func_brackets:
            if token != ",":
                buffer.append(token)
            else:
                args_list.append("".join(buffer))
                buffer.clear()
        else:
            raise ExpressionParserError("invalid expression")

    if buffer:
        args_list.append("".join(buffer))
        buffer.clear()

    args = [arg for arg in args_list if arg != ","]
    if not args:
        return math_funcs[func]()
    else:
        calculated_func_args = []
        for arg in args:
            calculated_func_args.append(
                _polish_notation_calculate(
                    _token_handler(
                        _tokenizer(arg))))
        return math_funcs[func](*calculated_func_args)


def _polish_notation_calculate(polish_notation: iter):
    """
    Calculate reverse polish notation from _token_handler iterator.
    Take:  polish_notation: iter.
    Return:  value from calculated function.
    """
    stack = []
    for token in polish_notation:
        if token in __OPERATORS:
            if __OPERATORS[token].args == 1:
                a = stack.pop()
                stack.append(__OPERATORS[token].function(a))
            elif __OPERATORS[token].args == 2:
                b, a = stack.pop(), stack.pop()
                stack.append(__OPERATORS[token].function(a, b))
        else:
            stack.append(token)
    return stack[0]


def calculate(expression: str):
    """
    Calculate input expression.
    Take:  expression: str.
    Return:  calculated value.
    """
    if not expression:
        raise ExpressionParserError("empty expression")
    if not _are_brackets_balanced(expression):
        raise ExpressionParserError("brackets are not balanced")
    if not _are_operators_and_operands_correct(expression):
        raise ExpressionParserError(
            "expression includes denied whitespaces or invalid combined operators or invalid operands")
    expression = _remove_whitespaces(expression)
    if not _are_no_missing_operators_next_to_brackets(expression):
        raise ExpressionParserError(
            "an operator near brackets is missed or expression contains unknown function")
    expression = _squash_doubled_plusminus(expression)
    expression = _differentiate_unary_plusminus(expression)
    expression = _bracket_exponentiation_wrapper(expression)

    try:
        result = _polish_notation_calculate(_token_handler(_tokenizer(expression)))
    except (IndexError, TypeError, ValueError):
        raise ExpressionParserError("invalid expression")
    except ZeroDivisionError:
        raise ExpressionParserError("division by zero")
    except OverflowError:
        raise ExpressionParserError("numerical result out of range (float value overflow)")
    else:
        return result


if __name__ == "__main__":
    print(__doc__)
