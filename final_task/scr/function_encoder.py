def encode_func_attr_count(func_name, att_number):
    return func_name + '@' + str(att_number)


def decode_func_attr_count(encoded_func_name):
    delimeter_idx = encoded_func_name.index('@')
    return encoded_func_name[:delimeter_idx], int(encoded_func_name[delimeter_idx+1:])


def is_func_name_encoded(func):
    return '@' in func
