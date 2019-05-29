import math
import parser
from sorter import create_polish_notation
from calculation import calc

s = 'sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)'
print(s)
t = parser.parse_input_expression(s)
print(t)
f = create_polish_notation(t)
print(f)
print(calc(f))
