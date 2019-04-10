import definitions

class ConvertError(Exception):
    def __str__(self):
        return 'cannot convert input expression to RPN due to mismatched parentheses'

class Converter(object):
    def __init__(self):
        pass

    def convert(self, iExpr):
        '''
        @iExpr -- parsed math string (list)
        This function converts @iExpr to list in RPN
        '''
        

        stack = []
        convertedExpr = []
        
        for ident in iExpr:
            if (ident.type == 'num'):
                convertedExpr.append(ident)
            elif (ident.type == 'func'):
                stack.append(ident)
            # elif (ident == ','):
            #     pass
            elif (ident.type == 'op'):
                while (len(stack) > 0):
                    stackIdent = stack[-1]
                    isStackIdentOp = stackIdent.val in definitions._operators.keys()
                    # complicated condition
                    if isStackIdentOp:
                        isIdentLeftAssoc = definitions._operators[ident.val].leftAssoc
                        IdentPriority = definitions._operators[ident.val].priority

                        stackIdentPriority = definitions._operators[stackIdent.val].priority
                        if ((isIdentLeftAssoc and IdentPriority <= stackIdentPriority) or
                        (not isIdentLeftAssoc and IdentPriority < stackIdentPriority)):
                            convertedExpr.append(stack.pop())
                        else:
                            break
                    else:
                        break
                stack.append(ident)
            elif (ident.type == 'lb'):
                stack.append(ident)
            elif (ident.type == 'rb'):
                while (len(stack) > 0):
                    if (stack[-1].type != 'lb'):
                        convertedExpr.append(stack.pop())
                    else:
                        break
                if (len(stack) == 0):
                    raise ConvertError()
                else:
                    stack.pop()
                if (len(stack) > 0):
                    if (stack[-1].type == 'func'):
                        convertedExpr.append(stack.pop())
        
        while (len(stack) > 0):
            if stack[-1].type in ('lb', 'rb'):
                raise ConvertError()
            convertedExpr.append(stack.pop())
        
        
        

        return convertedExpr
