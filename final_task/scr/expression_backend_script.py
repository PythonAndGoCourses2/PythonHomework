from .reverse_polish_notation import isopenbracket, isclosebracket
from .function_encoder import encode_func_attr_count
from . import settings as st


def find_open_and_close_brackets(expression):
    stack = []
    # check_ind_dict is a dictionary where key is index of open bracket and value is index of corresponding close bracket.
    check_ind_dict = {}
    open_bracket_indexes = []
    for token_ind in range(len(expression)):
        if isopenbracket(expression[token_ind]):
            stack.append(expression[token_ind])
            open_bracket_indexes.append(token_ind)
        elif isclosebracket(expression[token_ind]):
            if not stack:
                raise Exception("Brackets are not balanced. Open bracket missed.")
            stack.pop()
            open_bracket_ind = open_bracket_indexes.pop()
            check_ind_dict[open_bracket_ind] = token_ind
    return check_ind_dict


def define_func_attributes(func):
    attributes_number = 0
    func_name = func[0]
    func = func[2:-1]
    # Count amount of attributes
    opn_bracket = '('
    while opn_bracket in func:
        brackets_dict = find_open_and_close_brackets(func)
        opn_bracket_idx = func.index(opn_bracket)
        cls_bracket_idx = brackets_dict[opn_bracket_idx]
        func_begin = func[:opn_bracket_idx]
        func_end = func[cls_bracket_idx + 1:]
        func = func_begin
        func.extend(func_end)

    if func:
        attributes_number = func.count(st.sep) + 1
    return func_name, attributes_number


def is_token_basic_operator(token):
    exceptions = [')']
    if token in exceptions:
        return False
    return token in st.operators_priority


# Left-associative function
def define_funcs_in_expression(tokenized_expression):
    brackets_in_tokenized_expression = find_open_and_close_brackets(tokenized_expression)
    processed_tokenized_expression = []
    for idx, token in enumerate(tokenized_expression):
        if token in st.prefix_func:
            # Find index of open bracket of build-in function. For example index of '(' in ['sin','(','5',')'].
            open_bracket_of_func = idx + 1
            close_bracket_of_func = brackets_in_tokenized_expression[open_bracket_of_func]
            func = tokenized_expression[idx:close_bracket_of_func + 1]
            func_name, att_number = define_func_attributes(func)
            token = encode_func_attr_count(func_name, att_number)
        if token in ['-', '+']:
            if idx == 0 or is_token_basic_operator(tokenized_expression[idx-1]):
                token = encode_func_attr_count(token, 1)
            else:
                token = encode_func_attr_count(token, 2)
        processed_tokenized_expression.append(token)
    return processed_tokenized_expression


