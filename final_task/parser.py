from collections import defaultdict
import re
import definitions

class ParseError(Exception):
    def __init__(self, eExpr, ePos):
        self.expr = eExpr
        self.pos = ePos
    def __str__(self):
        msg = 'unknown token at ' + str(self.pos) + ': \n'
        msg += self.expr + '\n'
        msg += ''.join([' ' for i in range(self.pos - 1)]) + '---'
        return msg

class Parser(object):
    def __init__(self):
        self.numberM = definitions.Identifier(
            type = 'num', val = re.compile(definitions._number.regex))
        
        self.functionM = definitions.Identifier(type = 'func', val = re.compile( r'|'.join( 
            [re.escape(func) for func in sorted(definitions._functions, key=lambda func: len(func), reverse=True) ] )))

        self.operatorM = definitions.Identifier(type = 'op', val = re.compile( r'|'.join( 
            [re.escape(op) for op in sorted(definitions._operators, key=lambda func: len(func), reverse=True)] )))
        
        self.lBracketM = definitions.Identifier(type = 'lb', val = re.compile(r'\('))
        self.rBracketM = definitions.Identifier(type = 'rb', val = re.compile(r'\)'))
        self.comma = definitions.Identifier(type = 'comma', val = re.compile(r'\,'))

        self.matchers = (self.numberM, self.functionM, self.operatorM, self.lBracketM, self.rBracketM, self.comma)


    def parse(self, iExpr):
        '''
        @iExpr -- string to parse
        @parsedExpr -- output parsed expression
        '''

        

        parsedExpr = []
        curPos = 0

        while curPos < len(iExpr):
            for matcher in self.matchers:
                result = matcher.val.match(iExpr, curPos)
                if result:
                    if result.re == self.numberM.val:
                        parsedExpr.append( \
                            definitions.Identifier(type = matcher.type, val = float(result.group(0))))
                    else:
                        parsedExpr.append( \
                            definitions.Identifier(type = matcher.type, val = result.group(0)))
                    curPos = result.end()
                    break
                elif matcher == self.matchers[-1]:
                    # can't find suitable matcher
                    raise ParseError(iExpr, curPos)
                    


        
        
        
        
        return parsedExpr
