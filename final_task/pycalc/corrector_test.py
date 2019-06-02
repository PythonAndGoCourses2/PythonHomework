import unittest
import corrector

class TestCorrector(unittest.TestCase):
    corrector = corrector.Corrector()

    
    def testPlusMinusReduce(self):
        self.corrector._expr = "---5+---2+++8+--4++5*--6+-+-+15-23--(--5)"
        self.corrector._plusMinusReduce()
        self.assertEqual(self.corrector._expr, \
                         "-5-2+8+4+5*+6+15-23+(+5)")

    def testUnaryPlusReduce(self):
        self.corrector._expr = "+8*+3+(+sin())"
        self.corrector._unaryPlusReduce()
        self.assertEqual(self.corrector._expr, \
                         "8*3+(sin())")

    def testUnaryMinusReduce(self):
        self.corrector._expr = "-1*-2-(-3)+3^-2+1"
        self.corrector._unaryMinusReduce()
        self.assertEqual(self.corrector._expr, \
                         "(0-1)*(0-2)-((0-3))+3^(0-2)+1")

        self.corrector._expr = "-sin(-(1*-(2*3))-(-3))+3^(-2+1)"
        self.corrector._unaryMinusReduce()
        self.assertEqual(self.corrector._expr, \
                         "(0-sin((0-(1*(0-(2*3))))-((0-3))))+3^((0-2)+1)")

    

if __name__ == '__main__':
    unittest.main()
