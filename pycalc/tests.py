import unittest
import math
import operator

from pycalc import myresult


class MyTestsForCalc(unittest.TestCase):

    def test_not_my_1(self):
        self.assertEqual(myresult('-13'), -13, 'Fail')
        # self.assertEqual(myresult('6-(-13)'), 6-(-13))
        self.assertEqual(myresult('1---1'), 1---1)
        self.assertEqual(myresult('-+---+-1'), -+---+-1)
        self.assertEqual(myresult('1+2*2'), 1 + 2 * 2, 'Error')
        self.assertEqual(myresult('1+2*2'), 1+2*2, 'Error')
        self.assertEqual(myresult('1+(2+3*2)*3'), 1+(2+3*2)*3, 'Fail')
        self.assertEqual(myresult('10*(2+1)'), 10*(2+1), 'Fail')
        self.assertEqual(myresult('10**(2+1)'), 10**(2+1), 'Fail')
        self.assertEqual(myresult('100/3**2'), 100/3**2, 'Fail')
        # self.assertEqual(myresult('100/3%2**2'), operator.mod(100/3, 2**2), 'Fail')
        # self.assertEqual(myresult('log(e)'), math.log(math.e), 'Fail')
        self.assertEqual(myresult('sin(pi/2)'), math.sin(math.pi/2), 'Fail')
        self.assertEqual(myresult('100/4/3'), eval('100/4/3'), 'Fail')
        self.assertEqual(myresult('pi+e'), math.pi+math.e, 'Fail')
        self.assertEqual(myresult('log10(100)'), math.log10(100), 'Fail')
        self.assertEqual(myresult('sin(pi/2)*111*6'), math.sin(math.pi/2)*111*6, 'Fail')
        self.assertEqual(myresult('2*sin(pi/2)'), 2*math.sin(math.pi/2), 'Fail')
        # self.assertEqual(myresult('pow(2, 3)'),  math.pow(2, 3), 'Fail')
        # self.assertEqual(myresult('abs(-5)'),  5, 'Fail')
        self.assertEqual(myresult('round(123.4567890)'), round(123.4567890), 'Fail')
        self.assertEqual(myresult('102%12%7'), 6, 'Fail')
        self.assertEqual(myresult('100/4/3'),  100/4/3, 'Fail')
        self.assertEqual(myresult('2^3^4'),  (2**3)**4, 'Fail')
        self.assertEqual(myresult('1+2*3==1+2*3'), operator.eq(1+2*3, 1+2*3), 'Fail')
        self.assertEqual(myresult('e^5>=e^5+1'), operator.ge(math.e**5, math.e**5+1), 'Fail')
        # self.assertEqual(myresult('1+2*4/3+1!=1+2*4/3+2'), operator.ne(1+2*4/3+1, 1+2*4/3+2), 'Fail')
        self.assertEqual(myresult('(100)'), 100, 'Fail')
        self.assertEqual(myresult('666'), 666, 'Fail')
        self.assertEqual(myresult('-.1'), -0.1, 'Fail')
        self.assertEqual(myresult('1/3'), 1/3, 'Fail')
        self.assertEqual(myresult('1.0/3.0'), 1.0/3.0, 'Fail')
        self.assertEqual(myresult('.1 * 2.0^56.0'), .1 * 2.0**56.0, 'Fail')
        self.assertEqual(myresult('e^34'), math.e**34, 'Fail')
        self.assertEqual(myresult('(2.0^(pi/pi+e/e+2.0^0.0))'),  2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0), 'Fail')
        self.assertEqual(myresult('(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)'),
                         (2.0**(math.pi/math.pi+math.e/math.e+2.0**0.0))**(1.0/3.0), 'Fail')
        self.assertEqual(myresult('sin(pi/2^1) + log(1*4+2^2+1, 3^2)'),
                         math.sin(math.pi/2**1) + math.log(1*4+2**2+1, 3**2), 'Fail')
        # self.assertEqual(myresult('10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5'),
        # 10*math.e**0*math.log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5, 'Fail')
        self.assertEqual(myresult('2.0^(2.0^2.0*2.0^2.0)'),2.0**(2.0**2.0*2.0**2.0), 'Fail')
        # self.assertEqual(myresult('sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))',
        # math.sin(math.e**math.log(math.e**math.e**math.sin(23.0),45.0) + math.cos(3.0+math.log10(math.e**(-math.e)))),
        # 'Fail')


if __name__ == '__main__':
    unittest.main()
