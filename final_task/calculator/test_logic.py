import calculator.logic as c
import unittest
import math as m


class TestFunctions(unittest.TestCase):

    def test_error(self):
        self.assertRaisesRegex(Exception, "ERROR: no func with that name", c.add_math_objects, "12%5 * arcsin(1)", 0)
        self.assertRaises(ValueError, c.add_math_objects, "(((6)", 0)
        self.assertRaises(Exception, c.add_math_objects, "I would enjoy working on something great", 0)
        self.assertRaises(ValueError, c.add_math_objects, "1 2 3 < = 4 f,2", 0)

    def test_solve_equality(self):
        self.assertEqual(c.solve_equality("3 >    2>=2", 0), (True, 8))
        self.assertEqual(c.solve_equality(" cos(sin(1+2*3))==cos(sin(1+2*3)) ", 0), (True, 34))
        self.assertEqual(c.solve_equality("    pi/pi+e/e+2.0^2.0  <=   pi/pi+e/e+2.0^(1/e)   ", 0), (False, 50))
        self.assertEqual(c.solve_equality("5*abs(-2)/round(5.3)!=2.2^3", 0), (True, 27))
        self.assertEqual(c.solve_equality("2^abs(++--+-+6) < abs(--+-6)", 0), (False, 28))

    def test_add_math_objects(self):
        self.assertAlmostEqual(c.add_math_objects("2 * asin(sqrt(1 - 0.5 * 0.5)) + abs(asin(0.5))", 0)[0], 2.617993877)
        self.assertEqual(c.add_math_objects("2*3+(((4+5)*2.5)+4)*5", 0), (138.5, 21))
        self.assertEqual(c.add_math_objects("pow(6, 2) + 2*6*3 + pow(3, 2)", 0), (m.pow(9, 2), 29))
        self.assertAlmostEqual(c.add_math_objects("cos(pi/4)^2 + sin(pi/4)^2", 0)[0], 1)

    def test_multiply(self):
        self.assertEqual(c.multiply("1/2 * 3/4", 0), (0.375, 9))
        self.assertEqual(c.multiply("1/2 * 3/4", 0), (0.375, 9))
        self.assertAlmostEqual(c.multiply("5*abs(-2)/fsum(frexp(atan(5.3)))", 0)[0], 5.9096251221)
        self.assertAlmostEqual(c.multiply("12%5 * asin(1)^1", 0)[0], m.pi)

    def test_get_degree(self):
        self.assertEqual(c.get_degree("2^2^3", 0), (256, 5))

    def test_number_sign(self):
        self.assertEqual(c.number_sign("----++--+---++-+-+----+++++-cos(pi)", 0), (-1, 35))

