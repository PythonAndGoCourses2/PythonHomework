import re
import easyCalculation 
import functions
class ComplexCalc():
   
    calc=easyCalculation.Calculator()


    def expressionSearch(self,expr):

        while True:

            func=re.search(r'[A-ZAa-z]+1?0?',expr)

            if func==None:
                return self.calc.calculate(expr)
        
            afterExpr=func.end()
            k=func.start()
            if func[0] in functions.const:

                s=functions.const[func[0]]
                expr=expr[:k]+str(s)+expr[afterExpr:]
                continue
            
            searcher=0
            count=1
            for one in expr[afterExpr+1:]:

                searcher+=1
                if one ==")":
                    count-=1
                if one=="(":
                    count+=1
                if count==0:
                    break
            end=searcher+afterExpr
        #выкинуть если конец строки
            if expr[afterExpr] != '(':
           
                raise Exception("the expression must be written in the following way 'function(expression)'")

            else: 
           
                a=self.__findreplacement(func[0],expr[afterExpr+1:end])
                expr=expr[:k]+a+expr[end+1:]


    def __findreplacement(self,func,expr):

#сделать общий алгоритм для всех вариантов
        if func in functions.d:
        
            expr= str(self.expressionSearch(expr))
            a=functions.d[func](float(expr))
        
        elif  func in functions.twoarg:
            l=expr.split(",")
            if(len(2)!=2):
                raise Exception("проверьте аргументы функции ")
            l1=float(self.expressionSearch(l[0]))
            l2=float(self.expressionSearch(l[1]))
            a=functions.twoarg[func](l1,l2)
       

        else: 
    
            raise Exception("Indefined function")
        return str(a)

