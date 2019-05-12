import io
import unittest
from unittest.mock import patch
import pycalc


class TestCalcFunction(unittest.TestCase):
    def test_import_modules(self):
        pycalc.import_modules()
        self.assertFalse('path' in pycalc.LIBRARY)

        pycalc.import_modules('os')
        self.assertTrue('path' in pycalc.LIBRARY)

        pycalc.import_modules('sys', 'time')
        self.assertTrue('stdin' in pycalc.LIBRARY)
        self.assertTrue('clock' in pycalc.LIBRARY)

        with self.assertRaises(ModuleNotFoundError):
            pycalc.import_modules('bad_module')

    def test_exec_operation(self):
        a, b = '3', '7'

        with self.subTest("Arithmetic operations return currect sting value"):
            self.assertEqual(pycalc.exec_operation(a, b, pycalc.MULTIPLE), '+21.0')
            self.assertEqual(pycalc.exec_operation(b, a, pycalc.POWER), '+2187.0')
            self.assertEqual(pycalc.exec_operation(a, b, pycalc.TRUE_DIVISION), '+0.42857142857142855')
            self.assertEqual(pycalc.exec_operation(a, b, pycalc.FLOOR_DIVISION), '0.0')
            self.assertEqual(pycalc.exec_operation(a, b, pycalc.MODULE), '+3.0')
            self.assertEqual(pycalc.exec_operation(a, b, pycalc.PLUS), '+10.0')
            self.assertEqual(pycalc.exec_operation(a, b, pycalc.MINUS), '-4.0')

        with self.subTest("Comparison operations return currect sting value 1 (True) or 0 (False)"):
            self.assertEqual(float(pycalc.exec_operation(a, b, pycalc.LESS)), a < b)
            self.assertEqual(float(pycalc.exec_operation(a, b, pycalc.LESS_OR_EQUAL)), a <= b)
            self.assertEqual(float(pycalc.exec_operation(a, b, pycalc.EQUAL)), a == b)
            self.assertEqual(float(pycalc.exec_operation(a, b, pycalc.NOT_EQUAL)), a != b)
            self.assertEqual(float(pycalc.exec_operation(a, b, pycalc.GREAT_OR_EQUAL)), a >= b)
            self.assertEqual(float(pycalc.exec_operation(a, b, pycalc.GREAT)), a > b)

        with self.subTest("If don't have operation throw error"):
            self.assertRaises(ValueError, lambda: pycalc.exec_operation(a, b, '**'))
            self.assertRaises(ValueError, lambda: pycalc.exec_operation(a, b, '&&'))
            self.assertRaises(ValueError, lambda: pycalc.exec_operation(a, b, '||'))

    def test_replace_constant(self):
        with self.subTest("Replaces constant name to constant value"):
            self.assertEqual(pycalc.replace_constant('e'), '2.718281828459045')
            self.assertEqual(pycalc.replace_constant('e + e'), '2.718281828459045 + 2.718281828459045')

        with self.subTest("Does not touch function and digit"):
            self.assertEqual(pycalc.replace_constant('log()'), 'log()')
            self.assertEqual(pycalc.replace_constant('log(e)'), 'log(2.718281828459045)')
            self.assertEqual(pycalc.replace_constant('log(e) + e'), 'log(2.718281828459045) + 2.718281828459045')
            self.assertEqual(pycalc.replace_constant('2.161727821137838e+16'), '2.161727821137838e+16')
            self.assertEqual(pycalc.replace_constant('time(e) + e'), 'time(2.718281828459045) + 2.718281828459045')

    def test_replace_fanction(self):
        with self.subTest("Replaces function expression to function result"):
            self.assertEqual(pycalc.replace_fanction('log10(100)'), '2.0')
            self.assertEqual(pycalc.replace_fanction('log10(100) + log10(100)'), '2.0 + 2.0')
            self.assertEqual(pycalc.replace_fanction('log(100,10)'), '2.0')

        with self.subTest("Does not touch constants"):
            self.assertEqual(pycalc.replace_fanction('log10(100) + log(e)'), '2.0 + log(e)')
            self.assertEqual(pycalc.replace_fanction('log10(100) + e'), '2.0 + e')
            self.assertEqual(pycalc.replace_fanction('log10(e)'), 'log10(e)')
            self.assertEqual(pycalc.replace_fanction('log10(e) + 1'), 'log10(e) + 1')

        with self.subTest("Can receive seveeral arguments"):
            self.assertEqual(pycalc.replace_fanction('log(100,10)'), '2.0')
            self.assertEqual(pycalc.replace_fanction('hypot(-2,0)'), '2.0')
            self.assertEqual(pycalc.replace_fanction('hypot(-2,0) + log(100,10)'), '2.0 + 2.0')

    def test_replace_unary_operator(self):
        with self.subTest("Replaces sequence of unary operators"):
            self.assertEqual(pycalc.replace_unary_operator('+---+1'), '-1')
            self.assertEqual(pycalc.replace_unary_operator('+--+1'), '+1')
            self.assertEqual(pycalc.replace_unary_operator('-13'), '-13')
            self.assertEqual(pycalc.replace_unary_operator('-+---+-1'), '-1')

    def test_replace_bynary_operator(self):
        with self.subTest("Replaces sequence of bynary operators"):
            self.assertEqual(float(pycalc.replace_bynary_operator('1*2*3*4', pycalc.MULTIPLE)), eval('1*2*3*4'))
            self.assertEqual(float(pycalc.replace_bynary_operator('2^3^4', pycalc.POWER)), eval('2**3**4'))
            self.assertEqual(float(pycalc.replace_bynary_operator('1/2/3/4', pycalc.TRUE_DIVISION)), eval('1/2/3/4'))
            self.assertEqual(float(pycalc.replace_bynary_operator('1//2//3', pycalc.FLOOR_DIVISION)), eval('1//2//3'))
            self.assertEqual(float(pycalc.replace_bynary_operator('1%2%3%4', pycalc.MODULE)), eval('1%2%3%4'))
            self.assertEqual(float(pycalc.replace_bynary_operator('1+2+3+4', pycalc.PLUS)), eval('1+2+3+4'))
            self.assertEqual(float(pycalc.replace_bynary_operator('1-2-3-4', pycalc.MINUS)), eval('1-2-3-4'))
            self.assertEqual(float(pycalc.replace_bynary_operator('-1-2-3-4', pycalc.MINUS)), eval('-1-2-3-4'))

        with self.subTest("May receive several operators"):
            val = '1*2*3+1+2+3'
            self.assertEqual(float(pycalc.replace_bynary_operator(val, pycalc.MULTIPLE, pycalc.PLUS)), eval(val))
            val = '-1-2-3-4+1+2+3+4'
            self.assertEqual(float(pycalc.replace_bynary_operator(val, pycalc.MINUS, pycalc.PLUS)), eval(val))

    def test_replace_brackets(self):
        with self.subTest("Replaces inner brackets to result"):
            self.assertEqual(pycalc.replace_brackets('(1*2*3*4)'), '+24.0')
            self.assertEqual(pycalc.replace_brackets('1+(2+3*2)*3'), '1++8.0*3')
            self.assertEqual(pycalc.replace_brackets('10*(2+1)'), '10*+3.0')
            self.assertEqual(pycalc.replace_brackets('(100)'), '100')
            self.assertEqual(pycalc.replace_brackets('(((100)))'), '((100))')

        with self.subTest("Does not touch function brakets"):
            self.assertEqual(pycalc.replace_brackets('log(1*2*3*4)'), 'log(1*2*3*4)')
            self.assertEqual(pycalc.replace_brackets('log((5+95),10)'), 'log(+100.0,10)')

    def test_calc(self):
        pycalc.import_modules('math', 'time')

        with self.subTest("Calculates unary operations"):
            self.assertEqual(pycalc.calc('-13'), '-13')
            self.assertEqual(pycalc.calc('6-(-13)'), '+19.0')
            self.assertEqual(pycalc.calc('1---1'), '0.0')
            self.assertEqual(pycalc.calc('-+---+-1'), '-1')

        with self.subTest("Calculates priority operations"):
            self.assertEqual(pycalc.calc('1+2*2'), '+5.0')
            self.assertEqual(pycalc.calc('1+(2+3*2)*3'), '+25.0')
            self.assertEqual(pycalc.calc('10*(2+1)'), '+30.0')
            self.assertEqual(pycalc.calc('10^(2+1)'), '+1000.0')
            self.assertEqual(pycalc.calc('100/3^2'), '+11.11111111111111')
            self.assertEqual(pycalc.calc('100/3%2^2'), '+1.3333333333333357')

        with self.subTest("Calculates constants and functions"):
            self.assertEqual(pycalc.calc('pi+e'), '+5.859874482048838')
            self.assertEqual(pycalc.calc('log(e)'), '1.0')
            self.assertEqual(pycalc.calc('sin(pi/2)'), '1.0')
            self.assertEqual(pycalc.calc('log10(100)'), '2.0')
            self.assertEqual(pycalc.calc('sin(pi/2)*111*6'), '+666.0')
            self.assertEqual(pycalc.calc('2*sin(pi/2)'), '+2.0')

        with self.subTest("Calculates assotiacive operations"):
            self.assertEqual(pycalc.calc('102%12%7'), '+6.0')
            self.assertEqual(pycalc.calc('100/4/3'), '+8.333333333333334')
            self.assertIn(pycalc.calc('2^3^4'), ['2417851639229258349412352.0', '+2.4178516392292583e+24'])

        with self.subTest("Calculates comparation operations"):
            self.assertEqual(pycalc.calc('1+2*3==1+2*3'), '1')
            self.assertEqual(pycalc.calc('e^5>=e^5+1'), '0')
            self.assertEqual(pycalc.calc('1+2*4/3+1!=1+2*4/3+2'), '1')

        with self.subTest("Calculates common operations"):
            self.assertEqual(pycalc.calc('(100)'), '100')
            self.assertEqual(pycalc.calc('666'), '666')
            self.assertEqual(pycalc.calc('-.1'), '-.1')
            self.assertEqual(pycalc.calc('1/3'), '+0.3333333333333333')
            self.assertEqual(pycalc.calc('1.0/3.0'), '+0.3333333333333333')
            self.assertEqual(pycalc.calc('.1*2.0^56.0'), '+7205759403792794.0')
            self.assertEqual(pycalc.calc('e^34'), '+583461742527453.9')
            self.assertEqual(pycalc.calc('(2.0^(pi/pi+e/e+2.0^0.0))'), '+8.0')
            self.assertEqual(pycalc.calc('(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)'), '+2.0')
            self.assertEqual(pycalc.calc('sin(pi/2^1)+log(1*4+2^2+1,3^2)'), '+2.0')
            self.assertEqual(pycalc.calc('10*e^0*log10(.4-5/-0.1-10)--abs(-53/10)+-5'), '+16.36381365110605')
            self.assertEqual(pycalc.calc('2.0^(2.0^2.0*2.0^2.0)'), '+65536.0')
            self.assertEqual(pycalc.calc('sin(e^log(e^e^sin(23.0),45.0)+cos(3.0+log10(e^-e)))'), '0.76638122986603')

            val = ('sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))'
                   '+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)')
            self.assertEqual(pycalc.calc(val), '0.5361064001012783')

    def test_check_spaces(self):
        with self.subTest("Throws error if spaces is not correct"):
            self.assertRaises(ValueError, lambda: pycalc.check_spaces(''))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('------'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('-'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('+'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('1-'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('1 + 1 2 3 4 5 6 '))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('* *'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('/ /'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('/ *'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('+ *'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('1 2'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('= ='))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('! ='))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('<-+!'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('==7'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('1 + 2(3 * 4))'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('1 = = 2'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('1<>2'))
            self.assertRaises(ValueError, lambda: pycalc.check_spaces('1><2'))

        with self.subTest("removes spaces and returns new expretion"):
            self.assertEqual(pycalc.check_spaces('1   +   2'), '1+2')
            self.assertEqual(pycalc.check_spaces('1-2'), '1-2')
            self.assertEqual(pycalc.check_spaces('1 * - 2'), '1*-2')
            self.assertEqual(pycalc.check_spaces('1 == 2'), '1==2')
            self.assertEqual(pycalc.check_spaces('1 <= 2'), '1<=2')
            self.assertEqual(pycalc.check_spaces('1 - sin  (1,    2,  3) + - 2'), '1-sin(1,2,3)+-2')
            self.assertEqual(pycalc.check_spaces('sin(pi/2)'), 'sin(pi/2)')
            self.assertTrue(pycalc.check_spaces('sin(e^log(e^e^sin(23.0),45.0)+cos(3.0+log10(e^-e)))'))
            self.assertTrue(pycalc.check_spaces('time()-e-(1+1)/60+1-1*1//10000%1000^2==1==1<=3>=5<1>1'))

            val = ('sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))'
                   '+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)')
            self.assertTrue(pycalc.check_spaces(val))

    def test_check_brackets(self):
        with self.subTest("Throws error if brackets are not unpaired"):
            self.assertRaises(ValueError, lambda: pycalc.check_brackets('('))
            self.assertRaises(ValueError, lambda: pycalc.check_brackets(')'))
            self.assertRaises(ValueError, lambda: pycalc.check_brackets('())('))
            self.assertRaises(ValueError, lambda: pycalc.check_brackets('(()))'))
            self.assertRaises(ValueError, lambda: pycalc.check_brackets(')()('))

        with self.subTest("returns nothing if expretion is good"):
            self.assertIsNone(pycalc.check_brackets(''))
            self.assertIsNone(pycalc.check_brackets('()'))
            self.assertIsNone(pycalc.check_brackets('((()))()'))
            self.assertIsNone(pycalc.check_brackets('()()()()'))
            self.assertIsNone(pycalc.check_brackets('(()(()())())'))

    def test_check_constant(self):
        with self.subTest("Throws error if environment does not have constant"):
            self.assertRaises(ValueError, lambda: pycalc.check_constant('constant'))
            self.assertRaises(ValueError, lambda: pycalc.check_constant('constant + 5'))
            self.assertRaises(ValueError, lambda: pycalc.check_constant('sin(1) + constant + 7'))

        with self.subTest("Throws error if constant name starts with digit"):
            self.assertRaises(ValueError, lambda: pycalc.check_constant('10constant'))
            self.assertRaises(ValueError, lambda: pycalc.check_constant('10constant + 5'))
            self.assertRaises(ValueError, lambda: pycalc.check_constant('sin(1) + 10constant + 7'))

        with self.subTest("returns nothing if expretion is good"):
            pycalc.import_modules('math')

            self.assertIsNone(pycalc.check_constant(''))
            self.assertIsNone(pycalc.check_constant('e'))
            self.assertIsNone(pycalc.check_constant('sin(21)'))
            self.assertIsNone(pycalc.check_constant('sin(21) + e'))
            self.assertIsNone(pycalc.check_constant('2.4178516392292583e+24 + 5'))

    def test_check_function(self):
        with self.subTest("Throws error if environment does not have function"):
            self.assertRaises(ValueError, lambda: pycalc.check_function('multiply()'))
            self.assertRaises(ValueError, lambda: pycalc.check_function('multiply(5,7)'))
            self.assertRaises(ValueError, lambda: pycalc.check_function('multiply() + 7'))

        with self.subTest("Throws error if function name starts with digit"):
            self.assertRaises(ValueError, lambda: pycalc.check_function('10log()'))
            self.assertRaises(ValueError, lambda: pycalc.check_function('10log(1)'))
            self.assertRaises(ValueError, lambda: pycalc.check_function('10log(5,7)'))
            self.assertRaises(ValueError, lambda: pycalc.check_function('10log() + 7'))

        with self.subTest("returns nothing if expretion is good"):
            pycalc.import_modules('math')

            self.assertIsNone(pycalc.check_function(''))
            self.assertIsNone(pycalc.check_function('e'))
            self.assertIsNone(pycalc.check_function('sin(21)'))
            self.assertIsNone(pycalc.check_function('sin(21) + e'))
            self.assertIsNone(pycalc.check_function('2.4178516392292583e+24 + 5'))

    def test_check_expression(self):
        with self.subTest("calls methods check_spaces, check_brackets, check_constant, check_function"), \
             patch('pycalc.check_spaces', return_value='1') as check_spaces, \
             patch('pycalc.check_brackets') as check_brackets, \
             patch('pycalc.check_constant') as check_constant, \
             patch('pycalc.check_function') as check_function:

            pycalc.check_expression('1')

            self.assertTrue(check_spaces.called)
            self.assertTrue(check_brackets.called)
            self.assertTrue(check_constant.called)
            self.assertTrue(check_function.called)

        with self.subTest("returns expression without spaces"):
            self.assertEqual(pycalc.check_expression('1   +   2'), '1+2')
            self.assertEqual(pycalc.check_expression('1-2'), '1-2')
            self.assertEqual(pycalc.check_expression('1 * - 2'), '1*-2')
            self.assertEqual(pycalc.check_expression('1 - sin  (1,    2,  3) + - 2'), '1-sin(1,2,3)+-2')

    def test_parse_query(self):
        with self.subTest("return currect value"):
            import sys

            sys.argv = ['pycalc.py', 'time()/60', '-m', 'time', 'os', 'math']
            args = pycalc.parse_query()
            self.assertEqual(args.expr, 'time()/60')
            self.assertEqual(args.modules, ['time', 'os', 'math'])

    def test_print_answer(self):
        with self.subTest("print correct answer"), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            pycalc.HAS_COMPARE = False
            pycalc.print_answer('-1')
            self.assertEqual(mock_stdout.getvalue(), '-1\n')

            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            pycalc.print_answer('0')
            self.assertEqual(mock_stdout.getvalue(), '0\n')

            pycalc.HAS_COMPARE = True

            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            pycalc.print_answer('-1')
            self.assertEqual(mock_stdout.getvalue(), 'True\n')

            mock_stdout.truncate(0)
            mock_stdout.seek(0)
            pycalc.print_answer('0')
            self.assertEqual(mock_stdout.getvalue(), 'False\n')

    def test_main(self):
        with self.subTest("calls methods parse_query, import_modules, check_expression, calc, print_answer"), \
             patch('pycalc.parse_query') as parse_query, \
             patch('pycalc.import_modules') as import_modules, \
             patch('pycalc.check_expression') as check_expression, \
             patch('pycalc.calc', return_value='1') as calc, \
             patch('pycalc.print_answer') as print_answer:

            pycalc.main()

            self.assertTrue(parse_query.called)
            self.assertTrue(import_modules.called)
            self.assertTrue(calc.called)
            self.assertTrue(check_expression.called)
            self.assertTrue(print_answer.called)

        with self.subTest("catchs exception"), \
                patch('pycalc.parse_query') as parse_query, \
                patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            pycalc.main()
            self.assertTrue(mock_stdout.getvalue().startswith('ERROR: '))


if __name__ == '__main__':
    unittest.main()
