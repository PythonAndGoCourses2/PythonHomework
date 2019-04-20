op1=''
op2=''




def prior(op1, op2):
    oper = ['^', '*', '/', '+', '-']    # 4
    operhi = ['^']                      # 3
    opermid = ['*', '/']                # 2
    operlow = ['+', '-']                # 1
    operlowest = ['(',')']              # 0

    priorset = [operlowest, operlow, opermid, operhi]
    print(priorset)

    for i, data in enumerate(priorset):
        print(op1, i,data,)
        if op1 in data:
            prior1 = i
        if op2 in data:
            prior2 = i


    print('PRIOR', prior1, prior2)
    return prior1 < prior2

#print(prior('+', '*'))



def func(oper,*args):
    print('reciv',oper,args)
    print

    return


s = [1,2,3,4,5]

func('sun',*s)


