import re

class CheckAndChange():
        
    def do_all_changes(self,expr):
        expr=expr.replace("//","&")
        self.correct_brackets(expr)
        expr=expr.replace(" ","")
        return expr


    def correct_brackets(self,expr):
     
        if re.search(r'[0-9]+',expr)==None and re.search(r'[A-ZAa-z]+',expr)==None:        
            raise Exception("No Numbers in expression")
        
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

#доделать всякие исключения, есть ли исключение на пустые скобки
