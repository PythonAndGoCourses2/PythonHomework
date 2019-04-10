#!/usr/bin/python3

import unittest
import calculator.parser as parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = parser.Parser()

    def testInt(self):
        iExpr = "3//2"
        oExpr = self.parser.parse(iExpr)

        self.assertEqual(len(oExpr), 3)

        self.assertEqual(oExpr[0].type, 'num')
        self.assertEqual(oExpr[0].val, 3)

        self.assertEqual(oExpr[1].type, 'op') 
        self.assertEqual(oExpr[1].val, '//')

        self.assertEqual(oExpr[2].type, 'num') 
        self.assertEqual(oExpr[2].val, 2)

    def testFloat(self):
        iExpr = "1.23*.123"
        oExpr = self.parser.parse(iExpr)

        self.assertEqual(len(oExpr), 3)

        self.assertEqual(oExpr[0].type, 'num')
        self.assertEqual(oExpr[0].val, 1.23)

        self.assertEqual(oExpr[1].type, 'op') 
        self.assertEqual(oExpr[1].val, '*')

        self.assertEqual(oExpr[2].type, 'num') 
        self.assertEqual(oExpr[2].val, 0.123)

    def testFunc(self):
        iExpr = "1.23*sin(.123)"
        oExpr = self.parser.parse(iExpr)

        self.assertEqual(len(oExpr), 6)

        self.assertEqual(oExpr[0].type, 'num')
        self.assertEqual(oExpr[0].val, 1.23)

        self.assertEqual(oExpr[1].type, 'op') 
        self.assertEqual(oExpr[1].val, '*')

        self.assertEqual(oExpr[2].type, 'func') 
        self.assertEqual(oExpr[2].val, 'sin')

        self.assertEqual(oExpr[3].type, 'lb') 
        self.assertEqual(oExpr[3].val, '(')

        self.assertEqual(oExpr[4].type, 'num') 
        self.assertEqual(oExpr[4].val, 0.123)

        self.assertEqual(oExpr[5].type, 'rb') 
        self.assertEqual(oExpr[5].val, ')')

    def testParseError(self):
        iExpr = "2e3"
        self.assertRaises(parser.ParseError, self.parser.parse, iExpr)

if __name__ == '__main__':
    unittest.main()
