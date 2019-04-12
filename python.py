import re
import calc
import functions


def correctBrackets(expr):
    
    if re.search(r'[0-9]+',expr)==None:
        
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
        else: print("okey")
    return


def expressionSearch(expr):

    while True:

        func=re.search(r'[A-ZAa-z]+1?0?',expr)

        if func==None:
            return calc.calc(expr)
        
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

        if expr[afterExpr] != '(':
           
            raise Exception("the expression must be written in the following way 'function(expression)'")

        else: 

           
            a=findreplacement(func[0],expr[afterExpr+1:end])
            expr=expr[:k]+a+expr[end+1:]


def findreplacement(func,expr):


    if func in functions.d:
        
        expr= str(expressionSearch(expr))
        a=functions.d[func](float(expr))
        return str(a)
        
    else: 
    
        raise Exception("Indefined function")
    

try:
    a="log(12121223+22214211(123121+2444))"
    correctBrackets(a)
    a=expressionSearch(a)
    

except Exception as e:
   print("Error:  " + str(e))

print(a)


