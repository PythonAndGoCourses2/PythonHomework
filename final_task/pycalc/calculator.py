from . import corrector
from . import converter
from . import evaluator


class Calculator(object):
    def __init__(self, **kwargs):

        self.corrector = corrector.Corrector()
        self.converter = converter.Converter()
        self.evaluator = evaluator.Evaluator()

    def calculate(self, iExpr):
        """function for final calculate"""
        correctedExpr = self.corrector.correct(iExpr)
        convertedExpr = self.converter.convert(correctedExpr)
        evaluatedExpr = self.evaluator.evaluate(convertedExpr)
        return evaluatedExpr
