#!/usr/bin/python3

import unittest
import calculator.parser as parser
import calculator.converter as converter
import calculator.evaluator as evaluator


class TestEvaluate(unittest.TestCase):
    def setUp(self):
        self.parser = parser.Parser()
        self.converter = converter.Converter()
        self.evaluator = evaluator.Evaluator()

    def evaluate(self, iExpr):
        parsedExpr = self.parser.parse(iExpr)
        convertedExpr = self.converter.convert(parsedExpr)
        evaluatedExpr = self.evaluator.evaluate(convertedExpr)
        return evaluatedExpr

    def testArithmetical(self):
        self.assertEqual(self.evaluate("3+2"), 5)
        self.assertEqual(self.evaluate("3-2"), 1)
        self.assertEqual(self.evaluate("3*2"), 6)
        self.assertEqual(self.evaluate("3/2"), 1.5)
        self.assertEqual(self.evaluate("3//2"), 1)
        self.assertEqual(self.evaluate("3%2"), 1)
        self.assertEqual(self.evaluate("3^2"), 9)

    def testLogical(self):                              	
        self.assertEqual(self.evaluate("!3"), False)
        self.assertEqual(self.evaluate("!0"), True)                             	
        self.assertEqual(self.evaluate("3=2"), False)
        self.assertEqual(self.evaluate("3=3"), True)
                              	
    def testFunctional(self):                              	
        self.assertEqual(self.evaluate("sin(0)"), 0)
        self.assertEqual(self.evaluate("cos(0)"), 1)        
        self.assertEqual(self.evaluate("tan(0)"), 0)
        self.assertEqual(self.evaluate("sqrt(9)"), 3)
        self.assertEqual("%.4f" % self.evaluate("log(2.71828182846)"), '1.0000')
        self.assertEqual(self.evaluate("log10(10)"), 1) 

    def testEvaluatorError(self):
        # arguments count error
        self.assertRaises(evaluator.EvaluateError, self.evaluate, "sqrt()" )
        self.assertRaises(evaluator.EvaluateError, self.evaluate, "3+" )

if __name__ == '__main__':
    unittest.main()
