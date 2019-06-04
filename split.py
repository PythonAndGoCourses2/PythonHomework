import re
from operators import *


def is_num(char):
    try:
        float(char)
        return True
    except ValueError:
        return False

'''def is_num(char):
    return char.isdigit() or try: float(char) return True excep'''

def split_string(inp, prefixes=list_of_op):
    """Разбиение строки по операторам и операндам с помощью регулярных выражений"""

    str_list = re.findall('[a-zA-Z\d]+|\W+', inp)
    new_str = []
    for item in str_list:
        if is_num(item) or item in list_of_op:
            new_str.append(item)
        else:
            new_str.extend(split_by_prefix(item, prefixes))
    return new_str


def split_by_prefix(string, prefixes):
    regex = re.compile('|'.join(map(re.escape, prefixes)))
    while True:
        match = regex.match(string)
        if not match:
            break
        end = match.end()
        yield string[:end]
        string = string[end:]
    if string:
        yield string

