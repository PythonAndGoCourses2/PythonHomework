import re
import easyCalculation as calc
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




helper="""___o8o_____________________oo 
___8**o__________________o**88 
__$8*8888_____________88$8*_88 
__$8*888$888$$$$$$$$88888***$8 
__$8*8$$8888*******8$88***8$8 
__888$8****************888$8 
__*$8******************8888$8 
__$$********************8888$8_____oooooooo 
_8$8**8************8*****888$8___o$$$$$$8$$8888o 
_$$**8-8**********8-8*****88$8__$$88888********$$8 
_$$***$************$******88$8__$8888*********```$8 
_*$8****88***************88$$*__$888**********````$o 
__8$8**8$8**************88$8____$$8**********``````$8 
____8$88**********8**8888$8_____*$8**********``````$8 
______8$8$$$$$$$$$$$$$8*_________88*******8$$``8*88* 
______*$$**********$$$8ooo_______*$*******8$**8*_* 
_______8$**************$$$888___*$8******8$$* 
_______8$***8$8**88***$$$8$$$$$$$8*******8$* 
_______8$***$$8**$8*$$****$88$8$8*8**888888 
_____8$***$$$****8$$$******88*__*888888* 
______8888$$88888$$8888$$$88 
____________************* """

while True:
    try:
        a=input()
        if a!="--help":
            correctBrackets(a)
            a=expressionSearch(a)
        else: print (helper)

    except Exception as e:
        print("Error:  " + str(e))
    else: print(a)




