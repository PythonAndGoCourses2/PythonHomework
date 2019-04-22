
import pycalc.difcalc as difcalc
import pycalc.CheckAndChange as CheckAndChange
import argparse


calculator = difcalc.ComplexCalc()
cheker = CheckAndChange. CheckAndChange()

parser = argparse.ArgumentParser(description='Calculation')
parser.add_argument('a', type=str, help='input your expression')
args = parser.parse_args()


def start():
    try:

        if args.a != "--help":
            a = cheker.do_all_changes(args.a)
            a = calculator.calculate(args.a)

        else:
            print("help yourself")

    except Exception as e:
        print("ERROR:  " + str(e))
    else:
        print(a)


"""

while True:
        a=input()
        try:
                if a!="--help":
                        a=cheker.do_all_changes(a)
                        a=calculator.calculate(a)
        
                else: print ("your problem")

        except Exception as e:
                print("Error:  " + str(e))
        else: print(a)

    
    
"""
