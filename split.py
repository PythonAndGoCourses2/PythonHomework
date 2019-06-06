import re
import operators
from operators import *


def is_num(char):
    try:
        float(char)
        return True
    except ValueError:
        return False


def split_string(inp, prefixes=list_of_op):
    """Разбиение строки по операторам и операндам с помощью регулярных выражений"""
    """String splitting by operators and operands using regular expressions"""
    str_list = re.findall('(?:\d*\.\d+)|(?:\d+\.?)|[a-zA-Z\d]+|\W+', inp)
    new_str = []
    for item in str_list:
        if is_num(item) or item in list_of_op:
            new_str.append(item)
        else:
            new_str.extend(split_by_prefix(item, prefixes))
    return [i.strip(' ') for i in new_str]


def split_by_prefix(string, prefixes):
    """Разбиение строки по префиксам."""
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
