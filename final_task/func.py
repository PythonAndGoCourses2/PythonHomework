import math
from math import *

funcdict = {'sin':sin, 'cos':cos, 'pow':pow}


def func(oper,*args):
	print(oper, args)
	print(oper, *args)
	print(funcdict[oper](*args) )
	return
	
#return funcdict['pow'](a)


func('pow',2,3)

func('sin',2)
