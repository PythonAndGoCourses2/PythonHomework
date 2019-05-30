from . import settings as st
from .function_encoder import is_func_name_encoded, decode_func_attr_count


def ispostfix_func(token):
    if is_func_name_encoded(token):
        token, count = decode_func_attr_count(token)
    if token in st.postfix_func:
        return True
    return False


def isprefix_func(token):
    prefix_funcs = ['-@1', '+@1']
    if token in prefix_funcs:
        return True
    if is_func_name_encoded(token):
        token, count = decode_func_attr_count(token)
    if token in st.prefix_func:
        return True
    return False


def isconstant(token):
    if is_func_name_encoded(token):
        token, count = decode_func_attr_count(token)
    if token in st.constants:
        return True
    return False


def isopenbracket(token):
    if token == '(':
        return True
    return False


def isclosebracket(token):
    if token == ')':
        return True
    return False


def isbinary(token):
    if is_func_name_encoded(token):
        token, count = decode_func_attr_count(token)
        if count != 2:
            return False
    if token in st.binary_operators:
        return True
    return False


def priority(token):
    if is_func_name_encoded(token):
        token, count = decode_func_attr_count(token)
    return st.operators_priority[token]


def isleft_associative(token):
    if token == '^':
        return False
    return True


def is_float(token):
    flag = False
    try:
        if "." in token:
            val = float(token)
            flag = True
        else:
            val = int(token)
    except ValueError:
        pass
    return flag


def is_allowed(token):
    flag = False
    if is_func_name_encoded(token):
        token, count = decode_func_attr_count(token)
    if token.isdigit() or is_float(token):
        flag = True
    else:
        dataset = [st.math_functions_dict, st.prefix_func, st.ops, st.math_constants_dict, st.operators_priority]
        dataset.extend(st.data_set)
        for data in dataset:
            if token in data:
                flag = True
                break
    return flag


def is_ignored(token):
    if token in [',']:
        return True
    return False


def convert_to_RPN(listed_expression):
    stack = []
    output = []
    for token in listed_expression:
        if is_ignored(token):
            continue
        if not is_allowed(token):
            raise Exception("unknown token " + token)
        if token.isdigit() or ispostfix_func(token) or is_float(token):
            output.append(token)
        elif isconstant(token):
            output.append(str(st.math_constants_dict[token]))
        elif isprefix_func(token):
            stack.append(token)
        elif isopenbracket(token):
            stack.append(token)
        elif isclosebracket(token):
            temp_token = stack.pop()
            while not isopenbracket(temp_token):
                output.append(temp_token)
                temp_token = stack.pop()
        elif isbinary(token):
            if stack:
                temp_token = stack.pop()
                while isprefix_func(temp_token) or priority(temp_token) > priority(token) or \
                        isleft_associative(temp_token) and \
                        priority(temp_token) == priority(token):
                    output.append(temp_token)
                    temp_token = None
                    if stack:
                        temp_token = stack.pop()
                    else:
                        break
                if temp_token:
                    stack.append(temp_token)
            stack.append(token)
    if stack:
        while stack:
            temp_token = stack.pop()
            if isopenbracket(temp_token) or isclosebracket(temp_token):
                raise Exception("Parentheses mismatched")
                break
            else:
                output.append(temp_token)
    return output
