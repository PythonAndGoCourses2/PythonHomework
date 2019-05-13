import unittest
from ..library import Library
from .checker import (
    check_brackets,
    check_constant,
    check_expression,
    check_function,
    check_spaces,
)


class TestCheckFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = Library('math')

    def test_check_spaces(self):
        with self.subTest("Throws error if spaces is not correct"):
            self.assertRaises(ValueError, lambda: check_spaces(''))
            self.assertRaises(ValueError, lambda: check_spaces('------'))
            self.assertRaises(ValueError, lambda: check_spaces('-'))
            self.assertRaises(ValueError, lambda: check_spaces('+'))
            self.assertRaises(ValueError, lambda: check_spaces('1-'))
            self.assertRaises(ValueError, lambda: check_spaces('1 + 1 2 3 4 5 6 '))
            self.assertRaises(ValueError, lambda: check_spaces('* *'))
            self.assertRaises(ValueError, lambda: check_spaces('/ /'))
            self.assertRaises(ValueError, lambda: check_spaces('/ *'))
            self.assertRaises(ValueError, lambda: check_spaces('+ *'))
            self.assertRaises(ValueError, lambda: check_spaces('1 2'))
            self.assertRaises(ValueError, lambda: check_spaces('= ='))
            self.assertRaises(ValueError, lambda: check_spaces('! ='))
            self.assertRaises(ValueError, lambda: check_spaces('<-+!'))
            self.assertRaises(ValueError, lambda: check_spaces('==7'))
            self.assertRaises(ValueError, lambda: check_spaces('1 + 2(3 * 4))'))
            self.assertRaises(ValueError, lambda: check_spaces('1 = = 2'))
            self.assertRaises(ValueError, lambda: check_spaces('1<>2'))
            self.assertRaises(ValueError, lambda: check_spaces('1><2'))

        with self.subTest("removes spaces and returns new expretion"):
            self.assertEqual(check_spaces('1   +   2'), '1+2')
            self.assertEqual(check_spaces('1-2'), '1-2')
            self.assertEqual(check_spaces('1 * - 2'), '1*-2')
            self.assertEqual(check_spaces('1 == 2'), '1==2')
            self.assertEqual(check_spaces('1 <= 2'), '1<=2')
            self.assertEqual(check_spaces('1 - sin  (1,    2,  3) + - 2'), '1-sin(1,2,3)+-2')
            self.assertEqual(check_spaces('sin(pi/2)'), 'sin(pi/2)')
            self.assertTrue(check_spaces('sin(e^log(e^e^sin(23.0),45.0)+cos(3.0+log10(e^-e)))'))
            self.assertTrue(check_spaces('time()-e-(1+1)/60+1-1*1//10000%1000^2==1==1<=3>=5<1>1'))

            val = ('sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))'
                   '+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)')
            self.assertTrue(check_spaces(val))

    def test_check_brackets(self):
        with self.subTest("Throws error if brackets are not unpaired"):
            self.assertRaises(ValueError, lambda: check_brackets('('))
            self.assertRaises(ValueError, lambda: check_brackets(')'))
            self.assertRaises(ValueError, lambda: check_brackets('())('))
            self.assertRaises(ValueError, lambda: check_brackets('(()))'))
            self.assertRaises(ValueError, lambda: check_brackets(')()('))

        with self.subTest("returns nothing if expretion is good"):
            self.assertIsNone(check_brackets(''))
            self.assertIsNone(check_brackets('()'))
            self.assertIsNone(check_brackets('((()))()'))
            self.assertIsNone(check_brackets('()()()()'))
            self.assertIsNone(check_brackets('(()(()())())'))

    def test_check_constant(self):
        with self.subTest("Throws error if environment does not have constant"):
            self.assertRaises(ValueError, lambda: check_constant('constant', self.lib))
            self.assertRaises(ValueError, lambda: check_constant('constant + 5', self.lib))
            self.assertRaises(ValueError, lambda: check_constant('sin(1) + constant + 7', self.lib))

        with self.subTest("Throws error if constant name starts with digit"):
            self.assertRaises(ValueError, lambda: check_constant('10constant', self.lib))
            self.assertRaises(ValueError, lambda: check_constant('10constant + 5', self.lib))
            self.assertRaises(ValueError, lambda: check_constant('sin(1) + 10constant + 7', self.lib))

        with self.subTest("returns nothing if expretion is good"):
            self.assertIsNone(check_constant('', self.lib))
            self.assertIsNone(check_constant('e', self.lib))
            self.assertIsNone(check_constant('sin(21)', self.lib))
            self.assertIsNone(check_constant('sin(21) + e', self.lib))
            self.assertIsNone(check_constant('2.4178516392292583e+24 + 5', self.lib))

    def test_check_function(self):
        with self.subTest("Throws error if environment does not have function"):
            self.assertRaises(ValueError, lambda: check_function('multiply()', self.lib))
            self.assertRaises(ValueError, lambda: check_function('multiply(5,7)', self.lib))
            self.assertRaises(ValueError, lambda: check_function('multiply() + 7', self.lib))

        with self.subTest("Throws error if function name starts with digit"):
            self.assertRaises(ValueError, lambda: check_function('10log()', self.lib))
            self.assertRaises(ValueError, lambda: check_function('10log(1)', self.lib))
            self.assertRaises(ValueError, lambda: check_function('10log(5,7)', self.lib))
            self.assertRaises(ValueError, lambda: check_function('10log() + 7', self.lib))

        with self.subTest("returns nothing if expretion is good"):
            self.assertIsNone(check_function('', self.lib))
            self.assertIsNone(check_function('e', self.lib))
            self.assertIsNone(check_function('sin(21)', self.lib))
            self.assertIsNone(check_function('sin(21) + e', self.lib))
            self.assertIsNone(check_function('2.4178516392292583e+24 + 5', self.lib))

    def test_check_expression(self):
        with self.subTest("returns expression without spaces"):
            self.assertEqual(check_expression('1   +   2', self.lib), '1+2')
            self.assertEqual(check_expression('1-2', self.lib), '1-2')
            self.assertEqual(check_expression('1 * - 2', self.lib), '1*-2')
            self.assertEqual(check_expression('1 - sin  (1,    2,  3) + - 2', self.lib), '1-sin(1,2,3)+-2')


if __name__ == '__main__':
    unittest.main()
