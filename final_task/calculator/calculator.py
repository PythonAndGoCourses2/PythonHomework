from os import getcwd
import corrector
import parser
import converter
import evaluator


class Calculator(object):
    def __init__(self, **kwargs):

        self.corrector = corrector.Corrector()
        self.parser = parser.Parser()
        self.converter = converter.Converter()
        self.evaluator = evaluator.Evaluator()

    def calculate(self, iExpr):
        "function for final calculate"

        correctedExpr = self.corrector.correct(iExpr)

        parsedExpr = self.parser.parse(correctedExpr)
        
        convertedExpr = self.converter.convert(parsedExpr)
        
        evaluatedExpr = self.evaluator.evaluate(convertedExpr)

        return evaluatedExpr

#c = Calculator()
#s = "1-"
#print(c.calculate(s))
