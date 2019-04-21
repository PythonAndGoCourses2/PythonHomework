import unittest
from mycalc import mymodule
import math


class Testmyfunction(unittest.TestCase):

    def test_del_space(self):
        self.assertEqual(mymodule.del_space(' + 1'), '+1')
        self.assertEqual(mymodule.del_space('1 + + -1 +'), '1++-1+')

    def test_replace_many_plus_minus(self):
        self.assertEqual(mymodule.replace_many_plus_minus('+-1*3+++2'), '-1*3+2')

    def test_plus_reject(self):
        self.assertEqual(mymodule.plus_reject('3'), ['3'])
        self.assertEqual(mymodule.plus_reject('3+2'), ['3', '2'])
        self.assertEqual(mymodule.plus_reject('3-1'), ['3', '-1'])
        self.assertEqual(mymodule.plus_reject('3+'), ['3', ''])

    def test_calculation(self):
        self.assertAlmostEqual(mymodule.calculation('1*3'), 3.0)
        self.assertAlmostEqual(mymodule.calculation('1*3/3'), 1.0)
        self.assertAlmostEqual(mymodule.calculation('1*3^2*2'), 18.0)
        self.assertAlmostEqual(mymodule.calculation('1*-3'), -3.0)
        self.assertAlmostEqual(mymodule.calculation(' 1 *-3'), -3.0)
        self.assertAlmostEqual(mymodule.calculation('3%3'), 0)
        self.assertAlmostEqual(mymodule.calculation('-1^3^2'), -1.0)
        self.assertAlmostEqual(mymodule.calculation('e*-3'), -3.0*math.e)
        self.assertAlmostEqual(mymodule.calculation('pi*e*-tau'), -math.pi*math.e*math.tau)
        with self.assertRaises(ValueError):
            mymodule.calculation('1*')
            mymodule.calculation('1-')
            mymodule.calculation('p*2')
            mymodule.calculation('2**2')
            mymodule.calculation('/2')
            mymodule.calculation('')

    def test_calculation_without_brackets(self):
        self.assertAlmostEqual(mymodule.calculation_without_brackets('- - 1* 3'), 3.0)
        self.assertAlmostEqual(mymodule.calculation_without_brackets('  2 - -1^ - 3'), 3)
        self.assertAlmostEqual(mymodule.calculation_without_brackets('1-5 / 5* 3'), -2.0)
        self.assertAlmostEqual(mymodule.calculation_without_brackets('1* 3^2/ - 1'), -9.0)
        with self.assertRaises(ValueError):
            mymodule.calculation_without_brackets('1 *')
            mymodule.calculation_without_brackets('p * 2')
            mymodule.calculation_without_brackets(' * -e')
            mymodule.calculation_without_brackets('1-')

    def test_find_brakets(self):
        self.assertAlmostEqual(mymodule.find_brackets('(- - 1* 3  )'), '3.0')
        with self.assertRaises(ValueError):
            mymodule.find_brackets('1+2)')
            mymodule.find_brackets('( 1+2')
            mymodule.find_brackets('( (')

    def test_find_func(self):
        self.assertAlmostEqual(mymodule.find_func('sin3', 3, [3]), str(math.sin(3)))
        self.assertAlmostEqual(mymodule.find_func('  sin  3', 7, [3]), str(math.sin(3)))
        with self.assertRaises(KeyError):
            mymodule.find_func('si(3)', 2, [3])
    
    def test_calc_logical(self):
        self.assertEqual(mymodule.calc_logical([['>'], ['3', '1']]), True)
        with self.assertRaises(KeyError):
            mymodule.calc_logical([['<>'], ['2', '2']])

    def test_find_comparsion(self):
        self.assertEqual(mymodule.find_comparsion('3>1'), [['>'], ['3', '1']])
        self.assertEqual(mymodule.find_comparsion('3 >= 1'), [['>='], ['3 ', ' 1']])
        with self.assertRaises(ValueError):
            mymodule.find_comparsion('> 1')
            mymodule.find_comparsion('1 >=')
            


if __name__ == '__main__':
    unittest.main()
