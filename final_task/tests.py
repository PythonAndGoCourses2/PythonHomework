import unittest
import pycalc
import math as m


class TestCalculator(unittest.TestCase):

    def test_input(self):
        self.assertEqual(pycalc.pycalc('10+10'), 10 + 10)
        self.assertRaises(ValueError, pycalc.pycalc, 'sin10')
        self.assertRaises(ValueError, pycalc.pycalc, '')
        self.assertRaises(ValueError, pycalc.pycalc, "12f")
        self.assertEqual(pycalc.pycalc('2+2*3/5-6--12'), 2 + 2 * 3 / 5 - 6 - -12)
        self.assertRaises(ValueError, pycalc.pycalc, 'abvfdbfvbndvsnf')

    def test_split_brackets(self):
        self.assertEqual(pycalc.pycalc('((2+3)*3)'), ((2 + 3) * 3))
        self.assertEqual(pycalc.pycalc('cos(10)'), m.cos(10))
        self.assertEqual(pycalc.pycalc('15'), 15)
        self.assertEqual(pycalc.pycalc('2*cos(5)'), 2 * m.cos(5))
        self.assertEqual(pycalc.pycalc('(2+3)'), (2 + 3))

    def test_comfortable_input(self):
        self.assertEqual(pycalc.pycalc('10+10'), 10 + 10)
        self.assertEqual(pycalc.pycalc('2++3'), 2 + 3)
        self.assertRaises(ValueError, pycalc.pycalc, '2+()')
        self.assertRaises(ValueError, pycalc.pycalc, '(3+2)*3)')
        self.assertRaises(ValueError, pycalc.pycalc, '2**3')
        self.assertEqual(pycalc.pycalc('log10(10)'), m.log10(10))

    def test_tokinazer(self):
        self.assertRaises(ValueError, pycalc.pycalc, 'sinf')
        self.assertEqual(pycalc.pycalc('cos(5)+5'), m.cos(5) + 5)
        self.assertEqual(pycalc.pycalc('2+++-3'), 2 + ++-3)
        self.assertEqual(pycalc.pycalc('sin(pi)'), m.sin(m.pi))
        self.assertEqual(pycalc.pycalc('abs(-500)'), abs(-500))

    def test_negative_numbers(self):
        self.assertEqual(pycalc.pycalc('-15'), -15)
        self.assertEqual(pycalc.pycalc('2+(-3)'), 2 + (-3))
        self.assertEqual(pycalc.pycalc('+-15//2'), +-15 // 2)
        self.assertEqual(pycalc.pycalc('2+3'), 2 + 3)
        self.assertEqual(pycalc.pycalc('2/3'), 2 / 3)

    def test_check_function_and_constants(self):
        self.assertRaises(ValueError, pycalc.pycalc, 'abc')
        self.assertRaises(ValueError, pycalc.pycalc, 'ln')
        self.assertRaises(ValueError, pycalc.pycalc, 'piz')
        self.assertEqual(pycalc.pycalc('pi*3'), m.pi * 3)
        self.assertEqual(pycalc.pycalc('e*e'), m.e * m.e)

    def test_polish_notation(self):
        self.assertEqual(pycalc.pycalc('7+3-2*4'), 7 + 3 - 2 * 4)
        self.assertEqual(pycalc.pycalc('42+14//3'), 42 + 14 // 3)
        self.assertEqual(pycalc.pycalc('1.7*4*0.8'), 1.7 * 4 * 0.8)
        self.assertEqual(pycalc.pycalc('0.26*3.5/2'), 0.26 * 3.5 / 2)
        self.assertEqual(pycalc.pycalc('53^e+16'), 53 ** m.e + 16)

    def test_arguments(self):
        self.assertEqual(pycalc.pycalc('pow(2,3)') + 30, pow(2, 3) + 30)
        self.assertRaises(ValueError, pycalc.pycalc, 'cos(5,3)')
        self.assertRaises(ValueError, pycalc.pycalc, 'sin()')
        self.assertEqual(pycalc.pycalc('log(2,3)'), m.log(2, 3))
        self.assertEqual(pycalc.pycalc('pow(2,3)'), pow(2, 3))

    def test_calculate(self):
        self.assertEqual(pycalc.pycalc('sin(180//2+30)'), m.sin(180 // 2 + 30))
        self.assertEqual(pycalc.pycalc('42+14/3'), 42 + 14 / 3)
        self.assertEqual(pycalc.pycalc('1.7*4*0.8^50'), 1.7 * 4 * 0.8 ** 50)
        self.assertRaises(Exception, pycalc.pycalc, '0.26*3.5/0')
        self.assertRaises(Exception, pycalc.pycalc, '53^e+16+0/0')

    def test_common(self):
        self.assertEqual(pycalc.pycalc('90*3/20+---5'), 90 * 3 / 20 + ---5)
        self.assertRaises(Exception, pycalc.pycalc, '10^10^10^10^10')
        self.assertEqual(pycalc.pycalc('90*3/20+---5*sin(10//5)-e'), 90 * 3 / 20 + ---5 * m.sin(10 // 5) - m.e)
        self.assertEqual(pycalc.pycalc('+-+-++1'), +-+-++1)
        self.assertRaises(Exception, pycalc.pycalc, 'The end.')


if __name__ == '__main__':
    unittest.main()
