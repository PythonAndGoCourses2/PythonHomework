import re

class CandC():
        
    def doAllCh(self,expr):
        expr=expr.replace("//","&")
        self.correctBrackets(expr)
        return expr


    def correctBrackets(self,expr):
     
        if re.search(r'[0-9]+',expr)==None and re.search(r'[A-ZAa-z]+',expr)==None:
        
            raise Exception("Numbers???")
        
        i=0
  
        for one in expr:

       
            if one=="(":
                i+=1
            elif one==")":
                i-=1
            if i<0 :
                raise Exception("check brackets! ")
        else:
            if i!=0 :
                raise Exception("check brackets! ")  

#доделать всякие исключения, есть ли исключение на пустые скобки?
