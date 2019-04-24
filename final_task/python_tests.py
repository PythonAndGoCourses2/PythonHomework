import unittest
from mycalc import mymodule
from mycalc import solve_polynom
from mycalc import equations
import math


class Testmyfunction(unittest.TestCase):

    def test_del_space(self):
        self.assertEqual(mymodule.del_space(' + 1', '+-'), '+1')
        self.assertEqual(mymodule.del_space('1 + + -1 +', '+-'), '1++-1+')

    def test_replace_many_plus_minus(self):
        self.assertEqual(mymodule.replace_many_plus_minus('+-1*3+++2'), '-1*3+2')

    def test_plus_reject(self):
        self.assertEqual(mymodule.plus_reject('3'), ['3'])
        self.assertEqual(mymodule.plus_reject('3+2'), ['3', '2'])
        self.assertEqual(mymodule.plus_reject('3-1'), ['3', '-1'])
        self.assertEqual(mymodule.plus_reject('3+'), ['3', ''])

    def test_calculation_without_quotient(self):
        self.assertAlmostEqual(mymodule.calculation_without_quotient('1*3'), 3.0)
        self.assertAlmostEqual(mymodule.calculation_without_quotient('1*3/3'), 1.0)
        self.assertAlmostEqual(mymodule.calculation_without_quotient('1*3^2*2'), 18.0)
        self.assertAlmostEqual(mymodule.calculation_without_quotient('1*-3'), -3.0)
        self.assertAlmostEqual(mymodule.calculation_without_quotient(' 1 *-3'), -3.0)
        self.assertAlmostEqual(mymodule.calculation_without_quotient('3%3'), 0)
        self.assertAlmostEqual(mymodule.calculation_without_quotient('-1^3^2'), -1.0)
        self.assertAlmostEqual(mymodule.calculation_without_quotient('e*-3'), -3.0*math.e)
        self.assertAlmostEqual(mymodule.calculation_without_quotient('pi*e*-tau'), -math.pi*math.e*math.tau)
        with self.assertRaises(ValueError):
            mymodule.calculation_without_quotient('1*')
            mymodule.calculation_without_quotient('1-')
            mymodule.calculation_without_quotient('p*2')
            mymodule.calculation_without_quotient('2**2')
            mymodule.calculation_without_quotient('/2')
            mymodule.calculation_without_quotient('')

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

    def test_calculation(self):
        self.assertAlmostEqual(mymodule.calculation('7 * 1 //2'), 3.0)
        self.assertAlmostEqual(mymodule.calculation('4*3^2/-1'), eval('4*3**2/-1'))
        with self.assertRaises(ValueError):
            mymodule.calculation('//1')
            mymodule.calculation('1/ /2')

    def test_solv_linear_equation(self):
        self.assertEqual(solve_polynom.solv_linear_equation([6, 3]), [-2.0])

    def test_solv_quartic_equation(self):
        self.assertEqual(solve_polynom.solv_quartic_equation([-6, 5, 1]), [1.0, -6.0])

    def test_total_solve_func(self):
        self.assertAlmostEqual(equations.total_solve_func('1*x^2+5*x-6=0'), [1.0, -6.0])
        self.assertAlmostEqual(equations.total_solve_func('2*x + -6 = 4'), [5.0])
        self.assertAlmostEqual(equations.total_solve_func('2*x^3-11*x^2+12*x+9=0'), [3.0, -0.5, 3.0])
        with self.assertRaises(KeyError):
            equations.total_solve_func('1*x^5 -1 = 0')

    def test_filter_coefficient(self):
        self.assertAlmostEqual(equations.filter_coefficient([1, 1, 0, 0, 0]), [1, 1])
        self.assertAlmostEqual(equations.filter_coefficient([0, 0, 0, 0, 0]), [])

    def test_get_canonical_polynom(self):
        self.assertAlmostEqual(equations.get_canonical_polynom([2, 4, 6, 8, 2]), [1, 2, 3, 4, 1])
        self.assertAlmostEqual(equations.filter_coefficient([]), [])

    def test_get_coefficient(self):
        self.assertAlmostEqual(equations.get_coefficient('2*x^3-11*x^2+12*x+9-0'), [9.0, 12.0, -11.0, 2.0])


if __name__ == '__main__':
    unittest.main()
