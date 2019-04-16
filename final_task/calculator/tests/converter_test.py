#!/usr/bin/python3

import unittest
import calculator.parser as parser
import calculator.converter as converter

class TestConverter(unittest.TestCase):
    def setUp(self):
        self.converter = converter.Converter()
        self.parser = parser.Parser()

    def testBasic(self):
        # 3 + 2 == 3 2 +
        iExpr = "3+2"
        parsedExpr = self.parser.parse(iExpr)
        convertedExpr = self.converter.convert(parsedExpr)

        self.assertEqual(len(convertedExpr), 3)

        self.assertEqual(convertedExpr[0].type, 'num')
        self.assertEqual(convertedExpr[0].val, 3)

        self.assertEqual(convertedExpr[1].type, 'num')
        self.assertEqual(convertedExpr[1].val, 2)

        self.assertEqual(convertedExpr[2].type, 'op')
        self.assertEqual(convertedExpr[2].val, '+')

    def testBrackets(self):
        # (3 + 2) * (3 - 2) == 3 2 + 3 2 - *
        iExpr = "(3+2)*(3-2)"
        parsedExpr = self.parser.parse(iExpr)
        convertedExpr = self.converter.convert(parsedExpr)

        self.assertEqual(len(convertedExpr), 7)

        self.assertEqual(convertedExpr[0].type, 'num')
        self.assertEqual(convertedExpr[0].val, 3)

        self.assertEqual(convertedExpr[1].type, 'num')
        self.assertEqual(convertedExpr[1].val, 2)

        self.assertEqual(convertedExpr[2].type, 'op')
        self.assertEqual(convertedExpr[2].val, '+')

        self.assertEqual(convertedExpr[3].type, 'num')
        self.assertEqual(convertedExpr[3].val, 3)

        self.assertEqual(convertedExpr[4].type, 'num')
        self.assertEqual(convertedExpr[4].val, 2)

        self.assertEqual(convertedExpr[5].type, 'op')
        self.assertEqual(convertedExpr[5].val, '-')

        self.assertEqual(convertedExpr[6].type, 'op')
        self.assertEqual(convertedExpr[6].val, '*')

    def testOperatorsPriority(self):
        # 3 + 2 * 4 == 3 2 4 * +
        iExpr = "3+2*4"
        parsedExpr = self.parser.parse(iExpr)
        convertedExpr = self.converter.convert(parsedExpr)

        self.assertEqual(len(convertedExpr), 5)

        self.assertEqual(convertedExpr[0].type, 'num')
        self.assertEqual(convertedExpr[0].val, 3)

        self.assertEqual(convertedExpr[1].type, 'num')
        self.assertEqual(convertedExpr[1].val, 2)

        self.assertEqual(convertedExpr[2].type, 'num')
        self.assertEqual(convertedExpr[2].val, 4)

        self.assertEqual(convertedExpr[3].type, 'op')
        self.assertEqual(convertedExpr[3].val, '*')

        self.assertEqual(convertedExpr[4].type, 'op')
        self.assertEqual(convertedExpr[4].val, '+')

    def testFunctions(self):
        # sin(2 + cos(5)) == 2 5 cos + sin
        iExpr = "sin(2+cos(5))"
        parsedExpr = self.parser.parse(iExpr)
        convertedExpr = self.converter.convert(parsedExpr)

        self.assertEqual(len(convertedExpr), 5)

        self.assertEqual(convertedExpr[0].type, 'num')
        self.assertEqual(convertedExpr[0].val, 2)

        self.assertEqual(convertedExpr[1].type, 'num')
        self.assertEqual(convertedExpr[1].val, 5)

        self.assertEqual(convertedExpr[2].type, 'func')
        self.assertEqual(convertedExpr[2].val, 'cos')

        self.assertEqual(convertedExpr[3].type, 'op')
        self.assertEqual(convertedExpr[3].val, '+')

        self.assertEqual(convertedExpr[4].type, 'func')
        self.assertEqual(convertedExpr[4].val, 'sin')

    def testConverterError(self):
        # mismatched parentheses
        iExpr = "(2*(1)"
        parsedExpr = self.parser.parse(iExpr)
        self.assertRaises(converter.ConvertError, self.converter.convert, parsedExpr)

        iExpr = "2*(1))"
        parsedExpr = self.parser.parse(iExpr)
        self.assertRaises(converter.ConvertError, self.converter.convert, parsedExpr)

if __name__ == '__main__':
    unittest.main()
