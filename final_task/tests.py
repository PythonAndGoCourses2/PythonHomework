import unittest
import pycalc
import math as m


class TestCalculator(unittest.TestCase):

        def test_input(self):
            self.assertEqual(pycalc.calculate('10+10'), 10 + 10)
            self.assertRaises(ValueError, pycalc.calculate, 'sin10')
            self.assertRaises(ValueError, pycalc.calculate, '')
            self.assertRaises(ValueError, pycalc.calculate, "12f")
            self.assertEqual(pycalc.calculate('2+2*3/5-6--12'), 2 + 2 * 3 / 5 - 6 - -12)
            self.assertRaises(ValueError, pycalc.calculate, 'abvfdbfvbndvsnf')

        def test_comfortable_input(self):
            self.assertEqual(pycalc.make_input_comfortable('10+10'), '10+10')
            self.assertEqual(pycalc.make_input_comfortable('2++3'), '2+3')
            self.assertRaises(ValueError, pycalc.make_input_comfortable, '2+()')
            self.assertRaises(ValueError, pycalc.make_input_comfortable, '(3+2)*3)')
            self.assertRaises(ValueError, pycalc.make_input_comfortable, '2*')
            self.assertEqual(pycalc.make_input_comfortable('log10(10)'), 'lg(10)')

        def test_split_brackets(self):
            self.assertEqual(pycalc.calculate('((2+3)*3)'), ((2 + 3) * 3))
            self.assertEqual(pycalc.calculate('cos(10)'), m.cos(10))
            self.assertEqual(pycalc.calculate('15'), 15)
            self.assertEqual(pycalc.calculate('2*cos(5)'), 2 * m.cos(5))
            self.assertEqual(pycalc.calculate('(2+3)'), (2 + 3))

        def test_tokinaze(self):
            self.assertEqual(pycalc.tokenize('sinf'), ['sinf'])
            self.assertEqual(pycalc.tokenize('cos(5)+5'), ['cos', '(', '5', ')', '+', '5'])
            self.assertEqual(pycalc.tokenize('2+++-3'), ['2', '+++-', '3'])
            self.assertEqual(pycalc.tokenize('sin(pi)'), ['sin', '(', 'pi', ')'])
            self.assertEqual(pycalc.tokenize('abs(-500)'), ['abs', '(', '-', '500', ')'])

        def test_negative_numbers(self):
            self.assertEqual(pycalc.calculate('-15'), -15)
            self.assertEqual(pycalc.calculate('2+(-3)'), 2 + (-3))
            self.assertEqual(pycalc.calculate('+-15//2'), +-15 // 2)
            self.assertEqual(pycalc.calculate('2+3'), 2 + 3)
            self.assertEqual(pycalc.calculate('2/3'), 2 / 3)


        def test_check_function_and_constants(self):
            self.assertRaises(ValueError, pycalc.calculate, 'abc')
            self.assertRaises(ValueError, pycalc.calculate, 'ln')
            self.assertRaises(ValueError, pycalc.calculate, 'piz')
            self.assertEqual(pycalc.calculate('pi*3'), m.pi * 3)
            self.assertEqual(pycalc.calculate('e*e'), m.e * m.e)

        def test_polish_notation(self):
            self.assertEqual(pycalc.calculate('7+3-2*4'), 7 + 3 - 2 * 4)
            self.assertEqual(pycalc.calculate('42+14//3'), 42 + 14 // 3)
            self.assertEqual(pycalc.calculate('1.7*4*0.8'), 1.7 * 4 * 0.8)
            self.assertEqual(pycalc.calculate('0.26*3.5/2'), 0.26 * 3.5 / 2)
            self.assertEqual(pycalc.calculate('53^e+16'), 53 ** m.e + 16)

        def test_arguments(self):
            self.assertEqual(pycalc.calculate('pow(2,3)') + 30, pow(2, 3) + 30)
            self.assertRaises(ValueError, pycalc.calculate, 'cos(5,3)')
            self.assertRaises(ValueError, pycalc.calculate, 'sin()')
            self.assertEqual(pycalc.calculate('log(2,3)'), m.log(2, 3))
            self.assertEqual(pycalc.calculate('pow(2,3)'), pow(2, 3))

        def test_calculate(self):
            self.assertEqual(pycalc.calculate('sin(180//2+30)'), m.sin(180 // 2 + 30))
            self.assertEqual(pycalc.calculate('42+14/3'), 42 + 14 / 3)
            self.assertEqual(pycalc.calculate('1.7*4*0.8^50'), 1.7 * 4 * 0.8 ** 50)
            self.assertRaises(Exception, pycalc.calculate, '0.26*3.5/0')
            self.assertRaises(Exception, pycalc.calculate, '53^e+16+0/0')

        def test_common(self):
            self.assertEqual(pycalc.calculate('90*3/20+---5'), 90 * 3 / 20 + ---5)
            self.assertRaises(Exception, pycalc.calculate, '10^10^10^10^10')
            self.assertEqual(pycalc.calculate('90*3/20+---5*sin(10//5)-e'), 90 * 3 / 20 + ---5 * m.sin(10 // 5) - m.e)
            self.assertEqual(pycalc.calculate('+-+-++1'), +-+-++1)
            self.assertRaises(Exception, pycalc.calculate, 'The end.')

        if __name__ == '__main__':
            unittest.main()
