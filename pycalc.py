import math
import parser
from sorter import create_polish_notation
from calculation import calc

s = 'sin(pi/2)*111*6'
print(s)
t = parser.parse_input_expression(s)
print(t)
f = create_polish_notation(t)
print(f)
print(calc(f))
