import math
from parser import get_token
from sorter import shunting_yard


s = '1---1'
f = get_token(s)
print(shunting_yard(f))

