import math
import parser
from sorter import create_polish_notation
from calculation import calc

s = 'sin(1/(5-sin(cos(3*(7-atan2(4)-8))/9)))'
print(s)
t = parser.parse_input_expression(s)
print(t)
f = create_polish_notation(t)
print(f)
print(calc(f))
