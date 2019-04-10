import definitions

class EvaluateError(Exception):
    def __init__(self, eIdent, eArgCount, argCount):
        self.ident = eIdent
        self.eArgCount = eArgCount
        self.argCount = argCount

    def __str__(self):
        msg = 'too less arguments for ' + str(self.ident) + ' -- ' 
        msg += 'requires: ' + str(self.argCount) + ', provided: ' + str(self.eArgCount)
        return msg

class Evaluator(object):
    def _eval(self, iArgs):
        '''
        @iExpr -- list, describes function or operator (iExpr[0]) with its arguments (iExpr[>0])
        Return value: Identifier -- result of evaluating 
        '''
        op = iArgs[0]
        result = False
        if op in definitions._operators.keys():
            result = definitions._operators[op].alg(iArgs[1:])
            
        elif op in definitions._functions.keys():
            result = definitions._functions[op].alg(iArgs[1:])
            

        return result
    
    def evaluate(self, iExpr):
        '''
        @iExpr -- math string in RPN (list)
        This function computes @iExpr
        Return value: int or float or bool 
        '''
        

        stack = []
        for ident in iExpr:
            if (ident.type == 'num'):
                stack.append(ident)
            else: # operator or function 
                nArgs = 0
                if (ident.type == 'op'):
                    nArgs = definitions._operators[ident.val].argCount
                else:
                    nArgs = definitions._functions[ident.val].argCount
                args = []
                if (len(stack) < nArgs):
                    raise EvaluateError(ident.val, len(stack), nArgs)
                else:
                    for _ in range(nArgs):
                        args.append(stack.pop().val)
                args.append(ident.val)
                args.reverse() # we must reverse args to provide them in correct order
                stack.append(definitions.Identifier(type = 'num', val = self._eval(args)))
    
        if (len(stack) == 1):
            return stack.pop().val
