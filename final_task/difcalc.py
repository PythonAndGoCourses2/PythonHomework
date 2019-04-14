import re
import easyCalculation as calc
import functions

#вынести обработку и изменение строки для подсчета в отдельный файл, вроде что-то из помеченного тоже можно там сделать
def correctBrackets(expr):
   #пробелы 

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
        #выкинуть если конец строки
        if expr[afterExpr] != '(':
           
            raise Exception("the expression must be written in the following way 'function(expression)'")

        else: 

           
            a=findreplacement(func[0],expr[afterExpr+1:end])
            expr=expr[:k]+a+expr[end+1:]


def findreplacement(func,expr):

#сделать общий алгоритм для всех вариантов
    if func in functions.d:
        
        expr= str(expressionSearch(expr))
        a=functions.d[func](float(expr))
        
    elif  func in functions.twoarg:
        l=expr.split(",")
        if(len(2)!=2):
            raise Exception("проверьте аргументы функции ")
        l1=float(expressionSearch(l[0]))
        l2=float(expressionSearch(l[1]))
        a=functions.twoarg[func](l1,l2)
       

    else: 
    
        raise Exception("Indefined function")
    return str(a)

