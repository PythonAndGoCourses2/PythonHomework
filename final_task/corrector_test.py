#!/usr/sbin/python3

import unittest
import calculator.corrector as corrector

class TestCorrector(unittest.TestCase):
    def setUp(self):
        self.corrector = corrector.Corrector()

    def testFindFunc(self):
        self.corrector._expr = "sin(cos(3.123+2*e)-log10(pi))"
        self.corrector._findFunc()

        self.assertEqual(len(self.corrector._funcPos), 11)
        self.assertEqual(self.corrector._funcPos[0], 0)
        self.assertEqual(self.corrector._funcPos[1], 1)
        self.assertEqual(self.corrector._funcPos[2], 2)
        self.assertEqual(self.corrector._funcPos[3], 4)
        self.assertEqual(self.corrector._funcPos[4], 5)
        self.assertEqual(self.corrector._funcPos[5], 6)
        self.assertEqual(self.corrector._funcPos[6], 19)
        self.assertEqual(self.corrector._funcPos[7], 20)
        self.assertEqual(self.corrector._funcPos[8], 21)
        self.assertEqual(self.corrector._funcPos[9], 22)
        self.assertEqual(self.corrector._funcPos[10], 23)
        
    def testShortMultiplication(self):
        self.corrector._expr = "3(3+2)(2+3)2e(3+2)(3log10(ee))pi3"
        self.corrector._shortMultiplication()
        self.assertEqual(self.corrector._expr, "3*(3+2)*(2+3)*2*e*(3+2)*(3*log10(e*e))*pi*3")
        
        self.corrector._expr = ".123(3.123+.321)(2.321+.123)2.321e(.123+2.321)(.123log10(ee))pi.321"
        self.corrector._shortMultiplication()
        self.assertEqual(self.corrector._expr, \
                         ".123*(3.123+.321)*(2.321+.123)*2.321*e*(.123+2.321)*(.123*log10(e*e))*pi*.321")

        self.corrector._expr = "eee"
        self.corrector._shortMultiplication()
        self.assertEqual(self.corrector._expr, "e*e*e")


    def testConstInterpolation(self):
        self.corrector._expr = "e*e*e*pi*expi()*pi"
        self.corrector._constInterpolation()
        self.assertEqual(self.corrector._expr, \
                         "2.71828182846*2.71828182846*2.71828182846*3.14159265359*expi()*3.14159265359")

    def testPlusMinusReduce(self):
        self.corrector._expr = "--1+-2+3+--4++5*--6++--+-7-8--(--9)"
        self.corrector._plusMinusReduce()
        self.assertEqual(self.corrector._expr, \
                         "+1-2+3+4+5*+6-7-8+(+9)")

    def testUnaryPlusReduce(self):
        self.corrector._expr = "+1*+2+(+exp())"
        self.corrector._unaryPlusReduce()
        self.assertEqual(self.corrector._expr, \
                         "1*2+(exp())")

    def testUnaryMinusReduce(self):
        self.corrector._expr = "-1*-2-(-3)+3^-2+1"
        self.corrector._unaryMinusReduce()
        self.assertEqual(self.corrector._expr, \
                         "(0-1)*(0-2)-((0-3))+3^(0-2)+1")

        self.corrector._expr = "-sin(-(1*-(2*3))-(-3))+3^(-2+1)"
        self.corrector._unaryMinusReduce()
        self.assertEqual(self.corrector._expr, \
                         "(0-sin((0-(1*(0-(2*3))))-((0-3))))+3^((0-2)+1)")

    def testCorrect(self):
        iExpr = "1*4+3.3/(3+.3)*3(sqrt(4))/(sin(0)+1)"
        oExpr = self.corrector.correct(iExpr)
        self.assertEqual(oExpr, "1*4+3.3/(3+.3)*3*(sqrt(4))/(sin(0)+1)")

        iExpr = "10*e^0*log10(.4*-5/-0.1-10)--abs(-53//10)+-5"
        oExpr = self.corrector.correct(iExpr)
        self.assertEqual(oExpr, \
                         "10*2.71828182846^0*log10(.4*(0-5)/(0-0.1)-10)+abs((0-53)//10)-5")

if __name__ == '__main__':
    unittest.main()
