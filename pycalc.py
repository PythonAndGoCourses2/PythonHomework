import math
import parser
#from sorter import shunting_yard


s = 'sin(-pi/(2+10-8^2))+log(1*-4+2^2+1,3^-2)'
print(parser.parse_input_expression(s))
