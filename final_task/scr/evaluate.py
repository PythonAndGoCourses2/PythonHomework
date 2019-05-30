from PythonHomework.final_task import scr as st
from PythonHomework.final_task.scr import decode_func_attr_count, is_func_name_encoded
from PythonHomework.final_task.scr import is_float


def is_operand(token):
    if token.isdigit() or is_float(token):
        return True
    else:
        return False


def convert_to_proper_type(attr):
    if isinstance(attr, (int, float)):
        return attr
    elif is_float(attr):
        return float(attr)

    else:
        return int(attr)


def get_function_by_name(name):
    if name in st.math_functions_dict:
        return st.math_functions_dict[name]
    if name in st.ops_ex:
        return st.ops_ex[name]


def calculate(converted_expression):
    stack = []
    for token in converted_expression:
        attributes = []
        if is_operand(token):
            stack.append(token)
        else:
            if is_func_name_encoded(token):

                func_name, func_attr_count = decode_func_attr_count(token)
                while func_attr_count > 0:
                    if not stack:
                        raise Exception("missing argument")
                    attributes.insert(0, convert_to_proper_type(stack.pop()))
                    func_attr_count -= 1
                func = get_function_by_name(func_name)
                stack.append(func(*attributes))
            else:
                func_attr_count = st.ops[token][1]
                while func_attr_count > 0:
                    if not stack:
                        raise Exception("missing argument")
                    attributes.insert(0, convert_to_proper_type(stack.pop()))
                    func_attr_count -= 1
                stack.append(st.ops[token][0](*attributes))
    if len(stack) != 1:
        raise Exception("missing operator")
    return stack.pop()
