import unittest
from pycalc import testing
import math
import sys


class TestUnaryOperators(unittest.TestCase):

    def test_minus(self):
        self.assertEqual(testing("-33"), -33)

    def test_minus_with_brackets(self):
        self.assertEqual(testing("6-((-13))"), 19)

    def test_four_minus(self):
        self.assertEqual(testing("-1---1"), -2)
    
    def test_plus_minus(self):
        self.assertEqual(testing("-+--1"), -1)

            
class TestOperationPriority(unittest.TestCase):

    def test_plus_multiply(self):
        self.assertEqual(testing("2*3-4/5"), 2*3-4/5)

    def test_brackets_plus_multiply(self):
        self.assertEqual(testing("1+(2+3*2)*3"), 25)
        self.assertEqual(testing("10*(2+1)"), 30)
    def test_power(self): 
        self.assertEqual(testing("10^(2+1)"), 1000)
      
    def test_division(self):
        self.assertEqual(testing("100/3^2"), 100/3**2)
 
 
class TestFunctionsConstants(unittest.TestCase):

    def test_constants(self):
        self.assertEqual(testing("pi+e"), math.pi + math.e)

    def test_log(self):
        self.assertEqual(testing("log(e)"), math.log(math.e))
    
    def test_sin(self):
        self.assertEqual(testing("sin(pi/2)"), math.sin(math.pi/2))
        
    def test_common(self):
        self.assertEqual(testing("sin(pi/2)*111*6"), math.sin( math.pi/2)*111*6)
    
    def test_abs(self):
        self.assertEqual(testing("abs(-5)"), abs(-5))
        
    def test_round(self):
        self.assertEqual(testing("round(123.456789)"), round(123.456789))

            
class TestAssociative(unittest.TestCase):

    def test_modulo(self):
        self.assertEqual(testing("102%12%7"), 102%12%7)

    def test_division(self):
        self.assertEqual(testing("100/4/3"), 100/4/3)

    def test_power(self):
        self.assertEqual(testing("2^3^4"), 2**3**4)
            
class TestComparisonOperators(unittest.TestCase):



    def test_equally(self):
        self.assertEqual(testing("1+2*3==1+2*3"), 1+2*3==1+2*3)

    def test_more_or_equal(self):
        self.assertEqual(testing("e^5>=e^5+1"), pow(math.e, 5)>= pow(math.e, 5)+1)

    def test_not_equal(self):
        self.assertEqual(testing("1+2*4/3+1!=1+2*4/3+2"), 1+2*4/3+1!=1+2*4/3+2)

class TestCommon(unittest.TestCase):

    def test_number_with_brackets(self):
        self.assertEqual(testing("(100)"), 100)

    def test_number(self):
        self.assertEqual(testing("666"), 666)

    def test_number_with_floating_point(self):
        self.assertEqual(testing("-.1"), -0.1)

    def test_division(self):
        self.assertEqual(testing("1.0/3.0"), 1.0/3.0)
        self.assertEqual(testing("1/3"), 1/3)
        
    def test_power_and_multiply(self):
        self.assertEqual(testing(".1 * 2.0^56.0"), 0.1*pow(2.0, 56.0))
        
    def test_power_exp(self):
        self.assertEqual(testing("e^34"), pow(math.e, 34))

    def test_expressions(self):
        self.assertEqual(testing("(2.0^(pi/pi+e/e+2.0^0.0))"),
          pow(2, 3))
        self.assertEqual(testing("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"), 2.0)
        self.assertEqual(testing("sin(pi/2^1) + log(1*4+2^2+1, 3^2)") , math.sin(math.pi/2**1) + math.log(1*4+2**2+1, 3**2))
        self.assertEqual(testing("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5")
        , 10*pow(math.e, 0)*math.log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5)
    def test_function_in_function(self):
        self.assertEqual(testing("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)"),
         math.sin(- math.cos(- math.sin(3.0)- math.cos(- math.sin(-3.0*5.0)- math.sin( math.cos( math.log10(43.0))))+ math.cos( math.sin( math.sin(34.0-2.0**2.0))))-- math.cos(1.0)-- math.cos(0.0)**3.0))
    def test_power(self):
        self.assertEqual(testing("2.0^(2.0^2.0*2.0^2.0)"), pow(2, 16))


            
class TestErrorCases(unittest.TestCase):
    def test_ee(self):
        with self.assertRaises(SystemExit):
            testing("abcd")
    def test_multiply(self):
        with self.assertRaises(SystemExit):
            testing("6 * * 6")
    def test_comparisaon(self):
        with self.assertRaises(SystemExit):
            testing("6 < = 6")
    def test_division(self):
        with self.assertRaises(SystemExit):
            testing("5 / / 6")
        
    def test_only_plus(self):
        with self.assertRaises(SystemExit):
            testing("+")
        
    def test_not_enough_operands(self):
        with self.assertRaises(SystemExit):
            testing("1-")
    
    def test_no_operations(self):
        with self.assertRaises(SystemExit):
            testing("1 2")
     
    def test_comparison_error(self):
        with self.assertRaises(SystemExit):
            testing("==7")
    
    def test_missed_brackets(self):
        with self.assertRaises(SystemExit):
            testing("1 + 2(3*4))")
        with self.assertRaises(SystemExit):
            testing("((1+2)")
        with self.assertRaises(SystemExit):
            testing("))))")
        with self.assertRaises(SystemExit):
            testing(")1+1(")    
        
    def test_not_enough_operations(self):
        with self.assertRaises(SystemExit):
            testing("1 + 1 2 3 4 5 6 ")
    
    def test_missed_operands(self):
        with self.assertRaises(SystemExit):
            testing("------")
    
    def test_too_many_arguments(self):
        with self.assertRaises(SystemExit):
            testing("pow(2, 3, 4)")
        
if __name__ == '__main__':
    unittest.main()