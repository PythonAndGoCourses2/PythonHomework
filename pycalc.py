import math
from parser import get_token
from sorter import shunting_yard


s = 'sin(pi/2)+(5+5)^2-8'
f = get_token(s)
print(shunting_yard(f))

