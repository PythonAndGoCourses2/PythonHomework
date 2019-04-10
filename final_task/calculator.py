from os import getcwd
#from singleton import singleton
import corrector
import parser
import converter
import evaluator

#@singleton
class Calculator(object):
    def __init__(self, **kwargs):
        
        
        self.corrector = corrector.Corrector()
        self.parser = parser.Parser()
        self.converter = converter.Converter()
        self.evaluator = evaluator.Evaluator()


    def calculate(self, iExpr):
        
        correctedExpr = self.corrector.correct(iExpr)
       
        parsedExpr = self.parser.parse(correctedExpr)
        
        convertedExpr = self.converter.convert(parsedExpr)
        
        evaluatedExpr = self.evaluator.evaluate(convertedExpr)
        

        return evaluatedExpr


#c = Calculator()
#s = "2^3^2"
#print(c.calculate(s))

