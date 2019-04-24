#!/usr/bin/env python3


import argparse
import importlib.util
import sys
import re
from collections import namedtuple
import operator


class ArgParser:
    """
    The class contains method for args parsing.
    Use ArgParser.parse().
    """
    class __ArgumentParserError(argparse.ArgumentParser):
        """
        Overrides original exception-type to exception-type with human-readable error explanation.
        Write "ERROR: <message>" in stderr. Then return exit code 2.
        """
        def error(self, message):
            sys.stderr.write(f"ERROR: {message}\n")
            self.exit(2)

    @classmethod
    def parse(cls):
        """Parse args from CLI and return a tuple: (expression: str, (modules: str): tuple)."""
        parser = cls.__ArgumentParserError(prog="pycalc", description="Pure-python command-line calculator.",
                                           usage="pycalc [-h] EXPRESSION [-m MODULE [MODULE ...]]")

        if len(sys.argv) == 1:
            parser.print_usage()
            parser.exit()

        parser.add_argument(metavar="EXPRESSION",
                            type=str,
                            action="store",
                            dest="expression",
                            help="expression string to evaluate")

        parser.add_argument("-m", "--use-modules",
                            metavar="MODULE",
                            type=str,
                            action="store",
                            dest="arg_modules",
                            required=False,
                            default=[],
                            nargs="+",
                            help="additional modules to use")

        args = parser.parse_args()
        return args.expression, args.arg_modules


class ImportMathModules:
    """
    The class contains methods for importing args from the modules which received in the list.
    Use ImportMathModules.import_modules(list_of_modules_names: list).
    """
    class __ImportMathModulesError(ImportError):
        """
        Exception-type with human-readable error explanation.
        Write "ERROR: <message>" in stderr. Then return exit code 2.
        """
        def __init__(self, msg):
            sys.stderr.write(f"ERROR: {msg}\n")
            sys.exit(2)

    __importing_modules = ["math", ]
    __math_attrs = {"abs": abs,
                    "round": round}
    __math_funcs = dict()
    __math_consts = dict()

    @classmethod
    def __check_module(cls, module_name: str):
        """
        Check possibility of importing the module using its name.
        Take module_name as str like "math", "random", etc.
        Return a module_spec if possible else raise exception.
        """
        module_spec = importlib.util.find_spec(module_name)
        if module_spec is None:
            raise cls.__ImportMathModulesError(f"module '{module_name}' not found")
        else:
            return module_spec

    @classmethod
    def __import_module_from_spec(cls, module_spec):
        """
        Import the module from module_spec. Return a module as object.
        """
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    @classmethod
    def __parse_module(cls, module):
        """
        Parse received module for non-private attributes.
        Take: module as object.
        Return:  dict: {"name_of_func_or_const": func_or_const_as_an_object, ...}.
        """
        row_attrs_strings = dir(module)
        filt_attrs_strings = tuple(filter(lambda attr: not attr.startswith("_"), row_attrs_strings))
        filt_attrs_objects = (getattr(module, attr_str) for attr_str in filt_attrs_strings)
        attrs_dict = {attr_str: attr for attr_str, attr in zip(filt_attrs_strings, filt_attrs_objects)}
        return attrs_dict

    @classmethod
    def import_modules(cls, list_of_modules_names: list):
        """
        Import modules from list with module names.
        Take: list_of_modules_names: list  ( ["random", "cmath",...] )
        Return:  tuple: ({math_func_name: math_func_obj,...}, {math_const_name: math_const_obj,...}
        """
        cls.__importing_modules.extend(list_of_modules_names)

        for module in cls.__importing_modules:
            try:
                module_spec = cls.__check_module(module)
            except ImportError as err:
                sys.stderr.write(f"ERROR: {err}\n")
                sys.exit(2)

            module = cls.__import_module_from_spec(module_spec)
            module_attrs = cls.__parse_module(module)
            cls.__math_attrs.update(module_attrs)

            cls.__math_funcs = {name: obj for name, obj in cls.__math_attrs.items() if callable(obj)}
            cls.__math_consts = {name: obj for name, obj in cls.__math_attrs.items() if not callable(obj)}

        return cls.__math_funcs, cls.__math_consts


class ExpressionParser:
    """
    The class contains functionality to solve mathematical expressions.
    Use ExpressionParser.calculate(expression: str).
    """
    class __ExpressionParserError(Exception):
        """
        Make exception-type with human-readable error explanation.
        Write "ERROR: <message>" in stderr. Then return exit code 2.
        """
        def __init__(self, msg):
            sys.stderr.write(f"ERROR: {msg}\n")
            sys.exit(2)

    __C_REGEXP_BRACKET_UNARY_PLUSMINUS = re.compile(r"\([+\-]")
    __C_REGEXP_DOUBLED_PLUSMINUS = re.compile(r"[+\-]{2,}")
    __C_REGEXP_OPERATOR_THEN_PLUSMINUS = re.compile(r"[*%^][+\-]|[/=!<>]{1,2}[+\-]")
    __C_REGEXP_BEFORE_BRACKET = re.compile(r"[a-zA-Z]*[\d]*(?=[(])")
    __C_REGEXP_AFTER_BRACKET = re.compile(r"(?<=[)])[a-zA-Z]*[\d]*")
    __C_REGEXP_TOKENS = re.compile(r"[+\-*%^()]|[/=!<>]+|[a-zA-Z]+[\d]*|[\d]*[.][\d]+|[\d]+|[,]")

    math_funcs = {}
    math_consts = {}

    __operator_func_priority = namedtuple("Operator", ["function", "priority"])
    __OPERATORS = {
        "<>": __operator_func_priority(operator.eq, 0),
        "==": __operator_func_priority(operator.eq, 0),
        "!=": __operator_func_priority(operator.ne, 0),

        "<=": __operator_func_priority(operator.le, 1),
        "<": __operator_func_priority(operator.lt, 1),
        ">": __operator_func_priority(operator.gt, 1),
        ">=": __operator_func_priority(operator.ge, 1),

        "+": __operator_func_priority(operator.add, 1),
        "-": __operator_func_priority(operator.sub, 1),

        "*": __operator_func_priority(operator.mul, 2),
        "/": __operator_func_priority(operator.truediv, 2),
        "//": __operator_func_priority(operator.floordiv, 2),
        "%": __operator_func_priority(operator.mod, 2),

        "^": __operator_func_priority(operator.pow, 3)
    }

    @classmethod
    def __is_brackets_balanced(cls, expression: str):
        """
        Check whether brackets are balanced.
        Take:  expression: str.
        Return:  True, if brackets are balanced, else return False.
        """
        return expression.count("(") == expression.count(")")

    @classmethod
    def __is_not_denied_whitespaces_or_combined_operators(cls, expression: str):
        """
        Check expression for denied whitespaces or denied combined operators.
        Take:  expression: str.
        Return:  True, if there isn't denied whitespaces or denied combined operators, else return False.
        Example:
            "1*-1" -> True.
            "1*/1" -> False.
            "1* -1" -> True.
            "1/ /-1" -> False.
            "1 // -1" -> True.
            "1+.1 1-1" -> False.
            "1+.11-1" -> True.
        """
        last_token = ""
        tokens = cls.__C_REGEXP_TOKENS.finditer(expression)
        operator_symbols_without_plusminus = cls.__OPERATORS.keys()-{"-", "+"}

        for token in tokens:
            token = token.group()

            if token in operator_symbols_without_plusminus and last_token in cls.__OPERATORS:
                return False

            elif token in cls.math_consts or token in cls.math_funcs or cls.__is_number(token):
                if last_token in cls.math_consts or last_token in cls.math_funcs or cls.__is_number(last_token):
                    return False
            last_token = token

        return True

    @classmethod
    def __is_not_missed_operator_near_brackets(cls, expression: str):
        """
        Checks for missed operator before or after brackets.
        Take:  expression: str.
        Return:  True, if there is not a missed statement in the expression, else return True.
        Example:
            "1(1+1)" -> False.
            "1+(1+1)" -> True.
            "1+(1+1)func(...) -> False.
            "const(1+1) -> False.
            "1*(1+1)" -> True.
            "func(const)" -> True.
        """
        before_bracket_matches = cls.__C_REGEXP_BEFORE_BRACKET.findall(expression)
        for match in before_bracket_matches:
            if match and match not in cls.math_funcs:  # match may be '', but this is not a missed operator.
                return False

        after_bracket_matches = cls.__C_REGEXP_AFTER_BRACKET.findall(expression)
        for match in after_bracket_matches:
            if match:
                return False

        return True

    @classmethod
    def __remove_whitespaces(cls, expression: str):
        """
        Remove all whitespaces from string.
        Take:  expression: str.
        Return:  expression: str.
        """
        return ''.join(expression.split())

    @classmethod
    def __squash_doubled_plusminus(cls, expression: str):
        """
        Squashing combined add/sub operators.
        Take:  expression: str.
        Return:  expression: str.
        Example:
            "---+1" -> "-1".
            "--+1" -> "+1".
        """
        expression_chars = list(expression)
        doubled_plusminus_matches = cls.__C_REGEXP_DOUBLED_PLUSMINUS.finditer(expression)

        shift = 0
        for match in doubled_plusminus_matches:
            start_index, end_index = match.span()
            match_operators = match.group()
            output_operator = "-" if match_operators.count("-") % 2 else "+"
            expression_chars[start_index-shift:end_index-shift] = output_operator
            shift = end_index - start_index - 1

        return "".join(expression_chars)

    @classmethod
    def __bracket_unary_plusminus_wrapper(cls, expression: str):
        """
        Add brackets around value with unary plus/minus before.
        Take:  expression: str.
        Return:  expression: str.
        Example: "1^-1" -> "1^(-1)".
        """
        expression_chars = list(expression)
        shift = 0
        if expression[0] in "-+":
            expression_chars.insert(0, "(")
            expression_chars.append(")")
            shift += 2

        operator_then_plusminus_matches = cls.__C_REGEXP_OPERATOR_THEN_PLUSMINUS.finditer(expression)
        for match in operator_then_plusminus_matches:
            end_index = match.end()
            expression_chars.insert(end_index-1+shift, "(")
            shift += 1

            next_token = cls.__C_REGEXP_TOKENS.match(expression, end_index)
            if next_token.group() in cls.math_funcs:
                opened_brackets = 0
                following_tokens = cls.__C_REGEXP_TOKENS.finditer(expression, next_token.end())
                for following_token in following_tokens:
                    if following_token.group() == "(":
                        opened_brackets += 1
                    elif following_token.group() == ")":
                        opened_brackets -= 1
                    if not opened_brackets:
                        expression_chars.insert(following_token.end()+shift+1, ")")
                        break
            else:
                expression_chars.insert(next_token.end()+shift, ")")

        return "".join(expression_chars)

    @classmethod
    def __substitute_bracket_unary_plusminus(cls, expression: str):
        """
        Change unary plus/minus in brackets to binary plus/minus operation.
        Take:  expression: str.
        Return:  expression: str.
        Example: "sin(-3) -> "sin(0.0-3)".
        """
        expression_chars = list(expression)
        bracket_unary_plusminus_matches = cls.__C_REGEXP_BRACKET_UNARY_PLUSMINUS.finditer(expression)

        shift = 0
        for match in bracket_unary_plusminus_matches:
            end_index = match.end()
            expression_chars.insert((end_index-1)+shift, "0.0")
            shift += 1

        return "".join(expression_chars)

    @classmethod
    def __is_number(cls, value: str):
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

    @classmethod
    def __tokenizer(cls, expression: str):
        """
        Parse expression for tokens.
        Take:  expression: str.
        Return:  iterator with token values.
        """
        token_matches = cls.__C_REGEXP_TOKENS.finditer(expression)
        for token in token_matches:
            yield token.group()

    @classmethod
    def __token_handler(cls, parsed_expression: iter):
        """
        Handle tokens from tokenizer and return tokens using reverse polish notation.
        Can be used recursively with __function_handler-method.
        Take:  parsed_expression: iter  (from __tokenizer-method).
        Return:  iterator with token values in reverse polish notation.
        """
        stack = []
        func_stack = []
        func_brackets = 0

        for token in parsed_expression:
            if token in cls.math_funcs:
                func_brackets += 1
                func_stack.append(token)
            elif func_brackets:
                if token == "(" and func_stack[-1] not in cls.math_funcs:
                    func_brackets += 1
                elif token == ")":
                    func_brackets -= 1
                func_stack.append(token)

                if not func_brackets:
                    func_expression = "".join(func_stack)
                    func_stack.clear()
                    yield cls.__function_handler(func_expression)

            elif token in cls.__OPERATORS:
                while stack and stack[-1] != "(" and \
                        cls.__OPERATORS[token].priority <= cls.__OPERATORS[stack[-1]].priority:
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
            elif token in cls.math_consts:
                yield cls.math_consts[token]
            elif cls.__is_number(token):
                yield float(token)
            else:
                raise cls.__ExpressionParserError("invalid expression")
        while stack:
            yield stack.pop()

    @classmethod
    def __function_handler(cls, function_expression: str):
        """
        Handle function with attributes in string and call it.
        Can be used recursively with __token_handler-method.
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

        tokens = cls.__tokenizer(args)
        for token in tokens:
            if token in cls.math_funcs:
                func_brackets += 1
                buffer.append(token)
            elif token == "(" and buffer and buffer[-1] not in cls.math_funcs:
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
                raise cls.__ExpressionParserError("invalid expression")

        if buffer:
            args_list.append("".join(buffer))
            buffer.clear()

        args = [arg for arg in args_list if arg != ","]
        if not args:
            return cls.math_funcs[func]()
        else:
            calculated_func_args = []
            for arg in args:
                calculated_func_args.append(
                    cls.__polish_notation_calculate(
                        cls.__token_handler(
                            cls.__tokenizer(arg))))
            return cls.math_funcs[func](*calculated_func_args)

    @classmethod
    def __polish_notation_calculate(cls, polish_notation: iter):
        """
        Calculate reverse polish notation from __token_handler iterator.
        Take:  polish_notation: iter.
        Return:  value from calculated function.
        """
        stack = []
        for token in polish_notation:
            if token in cls.__OPERATORS:
                b, a = stack.pop(), stack.pop()
                stack.append(cls.__OPERATORS[token].function(a, b))
            else:
                stack.append(token)
        return stack[0]

    @classmethod
    def calculate(cls, expression: str):
        """
        Calculate input expression.
        Take:  expression: str.
        Return:  calculated value.
        """
        if not expression:
            raise cls.__ExpressionParserError("empty expression")
        if not cls.__is_brackets_balanced(expression):
            raise cls.__ExpressionParserError("brackets are not balanced")
        if not cls.__is_not_denied_whitespaces_or_combined_operators(expression):
            raise cls.__ExpressionParserError("expression includes denied whitespaces or invalid combined operators")
        expression = cls.__remove_whitespaces(expression)
        if not cls.__is_not_missed_operator_near_brackets(expression):
            raise cls.__ExpressionParserError("an operator near brackets is missed")
        expression = cls.__squash_doubled_plusminus(expression)
        expression = cls.__bracket_unary_plusminus_wrapper(expression)
        expression = cls.__substitute_bracket_unary_plusminus(expression)

        try:
            result = cls.__polish_notation_calculate(cls.__token_handler(cls.__tokenizer(expression)))
        except (IndexError, TypeError, ValueError):
            raise cls.__ExpressionParserError("invalid expression")
        except ZeroDivisionError:
            raise cls.__ExpressionParserError("division by zero")

        return result


def main():
    expression, modules = ArgParser.parse()
    math_funcs, math_consts = ImportMathModules.import_modules(modules)

    ExpressionParser.math_funcs.update(math_funcs)
    ExpressionParser.math_consts.update(math_consts)

    result = ExpressionParser.calculate(expression)

    print(result)


if __name__ == "__main__":
    main()
