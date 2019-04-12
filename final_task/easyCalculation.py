import re
import operators


def calculation(expr):    

    for i in operators.operators:   
        place=expr.rfind(i)
     

        while place!=-1:

            findBefore=re.search(r'(?:\d+(?:\.\d+)?|\.\d+)',expr[place::-1])
            findAfter=re.search(r'(?:\d+(?:\.\d+)?|\.\d+)',expr[place:])
           

            if findAfter==None or findAfter.start()!=1 or  findBefore==None or findBefore.start()!=1:
               raise Exception("the expression should be written in the following form 'number operator number'")
               
            rezult=str( operators.operators[i](float(findBefore[0][::-1]),float(findAfter[0])))
            begin=expr[:place-len(findBefore[0])]
            expr=begin+rezult+expr[findAfter.end()+place:]
            place=expr.rfind(i)
               
    
    if expr[-1]=="+" or expr[-1]=="-":
        raise Exception("'+' or '-'mustn' be the last even in brackets")
    
    all=list()
    while expr!="":
        find=re.search(r'(?:\d+(?:\.\d+)?|\.\d+)',expr)
        l=expr[:find.end()]
        if l.count("-")%2==1:
            all.append("-"+find[0])
        else: all.append(find[0])
        expr=expr[find.end():]

    sum =0
    for each in all:
        sum+=float(each)
    return sum

def calc(expr):
    expr.replace("//","&")
    while "(" in expr:
        
        end=expr.find(")")
        if end!=len(expr)-1 and expr[end+1] not in operators.operators:
            Exception("no operator after brackets")

        #проверка на множитель перед и после скобок
        begin=expr[:end].rfind("(")
        if begin!=0 and expr[begin-1] not in operators.operators and expr[begin-1]!='-' and expr[begin-1]!='+' :
            raise Exception("no operators before brackets")
        rezult=calculation(expr[begin+1:end])
       
        expr=expr[:begin]+str(rezult)+expr[end+1:]    
    else:
        rezult=calculation(expr)

        return rezult

