import re
import pycalc.easyCalculation as easyCalculation 
import math

class ComplexCalc():
   
    calc=easyCalculation.Calculator()

    math_functions = {**{attr:getattr(math, attr) for attr in dir(math) if callable(getattr(math, attr))},
    **{"abs":lambda a:abs(a),
        "round":lambda a:round(a),
        "pow":lambda a,b:pow(a,b)}}


    const={
    "pi":math.pi,
    "e":math.e
    }


    def expression_search(self,expr):

        while True:

            func=re.search(r'[A-ZAa-z]+1?0?',expr)

            if func==None:
                return self.calc.calculate(expr)
        
            afterExpr=func.end()
            k=func.start()
            if func[0] in ComplexCalc.const:

                s=ComplexCalc.const[func[0]]
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
           
                a=self.__find_replacement(func[0],expr[afterExpr+1:end])
                expr=expr[:k]+a+expr[end+1:]


    def __find_replacement(self,func,expr):

        if  func in ComplexCalc.math_functions:
            l=expr.split(",")
            
            k=[]
            for each in l:               
                k.append(float(self.expression_search(each)))

            a='{:.10f}'.format(ComplexCalc.math_functions[func](*k))      

        else: 
    
            raise Exception("Indefined function")
        return str(a)

 
    compare={

    ">":lambda a, b: a>b,
    ">=":lambda a, b:a>=b,
    "<=":lambda a, b:a<=b,
    "=": lambda a, b: a==b,
    "<":lambda a,b: a<b,
    "!=":lambda a,b:a!=b


    }
    def calculate(self,expr):

         place=re.search(r'(>=)|(>)|(<=)|(<)|(!=)|=',expr)
         if place:
             a=self.expression_search(expr[:place.start()])
             b=self.expression_search(expr[place.end():])
             return ComplexCalc.compare[place[0]](a,b)
         else:
             return self.expression_search(expr)