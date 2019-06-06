import math
import operator
import sys

"""Module with calculator methods."""


def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True


def is_int(n):
    try:
        int(n)
    except ValueError:
        return False
    return True


def is_empty(n):
    return len(n) == 0


def peek(n):
    return n[len(n) - 1]


def check_brackets(expr):
    bracket_right = 0
    bracket_left = 0
    for i in expr:
        if i == '(':
            bracket_left += 1
        elif i == ')':
            bracket_right += 1
    if bracket_left != bracket_right:
        sys.exit('Error: brackets are not balanced')
    # elif (expr.find('(') > expr.find(')') or expr.rfind('(') < expr.rfind(')') and expr.find('(') != expr.rfind('(')):
    #     sys.exit('Error: brackets are not balanced')
    # if expr.find('()') == -1:
    #     sys.exit('Error: brackets are not balanced')

# not need
# def zero_minus(input_data):
#     result = []
#     value = 0
#     while value < len(input_data):
#         if input_data[0] == '-' or input_data[0] == '+':
#             result.append('0')
#             result.append(input_data[value])
#             del input_data[value]
#         else:
#             result.append(input_data[value])
#         value += 1
#     return result


def check_power(input_data):
    result = []
    value = 0
    while value < len(input_data):
        if input_data[value] == '*' and input_data[value + 1] == '*':
            result.append('^')
            del input_data[value + 1]
        else:
            result.append(input_data[value])
        value += 1
    return result


def check_minus_plus(input_data):
    result = []
    value = 0
    while value < len(input_data):
        if (input_data[value] == '-' and input_data[value + 1] == '+') or (input_data[value] == '+' and input_data[value + 1] == '-'):
            result.append('-')
            del input_data[value + 1]

        elif (input_data[value] == '-' and input_data[value + 1] == '-') or (
                input_data[value] == '+' and input_data[value + 1] == '+'):
            result.append('+')
            del input_data[value + 1]
        else:
            result.append(input_data[value])
        value += 1

    return result


def check(expr):
    check_brackets(expr)
    if not expr or expr == '()':
            sys.exit('Error: empty expression')


class Calculator:
    """Calculator class."""

    first_priority_operators = {
        '+': (3, operator.add),
        '-': (3, operator.sub),
        '*': (4, operator.mul),
        '/': (4, operator.truediv),
        '//': (4, operator.floordiv),
        '%': (4, operator.mod),
        '^': (5, operator.pow),
        '-u': (5, operator.neg),
        '+u': (5, operator.pos),
        '(': (1,),
        ')': (1,),
        ',': (1,)
    }
    second_priority_operators = {
        '<': (2, operator.lt),
        '>': (2, operator.gt),
        '>=': (2, operator.ge),
        '<=': (2, operator.le),
        '==': (2, operator.eq),
        '!=': (2, operator.ne)
    }
    operators = {}
    all_op_and_func = {}
    operators.update(second_priority_operators)
    operators.update(first_priority_operators)
    math_functions = {attr: (10, getattr(math, attr))
                      for attr in dir(math)
                      if callable(getattr(math, attr))}
    math_functions.update({
        'abs': (10, operator.abs),
        'round': (10, (lambda x: round(x)))
    })
    all_op_and_func.update(math_functions)
    all_op_and_func.update(operators)

    constants = {'pi': math.pi, 'e': math.e, 'tau': math.tau}

    def __init__(self):
        pass

    def expr_parts(self, input_data):
        """Функция разбивает начальную строку на список чисел, операций и функций; возвращает его"""  # TODO: translate

        all_operators = list(self.all_op_and_func.keys())
        for i in range(len(self.all_op_and_func)):
            if input_data.find(all_operators[i]) == -1:
                continue
            input_data = input_data.replace(all_operators[i],
                                            ' ' + all_operators[i] + ' ')

        input_data = list(filter(None, input_data.split(' ')))
        result = []

        curr_pos = 0
        while curr_pos < len(input_data):
            if input_data[curr_pos] == 'log' and input_data[curr_pos + 1] == '10':
                result.append(input_data[curr_pos] + input_data[curr_pos + 1])
                del input_data[curr_pos + 1]
            else:
                result.append(input_data[curr_pos])
            curr_pos += 1

        for i in range(len(result)):
            if result[i] == '<' or result[i] == '>' or result[i] == '/':
                if result[i + 1][0] == '=':
                    result[i] = result[i] + result[i + 1][0]
                    result[i + 1] = result[i + 1][1:]
                elif result[i + 1][0] == '/':
                    result[i] = result[i] + result[i + 1][0]
                    result[i + 1] = ''

        for i in result:
            result = check_minus_plus(result)


        # result = list(filter(None, result))
        # value = 0
        # while value < len(result):
        #     if not result[value] in self.all_op_and_func.keys() and not is_number(result[value]):
        #         sys.exit('Error: unknown operation, check expression')
        #     value += 1

        return result

    def polish_notation(self, input_data):
        """add docstring"""
        op_stack = []
        polish_list = []

        for part_exp in input_data:
            if part_exp in self.constants:
                polish_list.append(str(self.constants[part_exp]))
            elif is_number(part_exp):
                polish_list.append(part_exp)
            elif part_exp == ',':
                if not is_empty(op_stack) and self.all_op_and_func[peek(op_stack)] >= self.all_op_and_func[part_exp]:
                    polish_list.append(op_stack.pop())
            elif part_exp == '(':
                op_stack.append(part_exp)
            elif part_exp == ')':
                top_token = op_stack.pop()
                while top_token != '(':
                    polish_list.append(top_token)
                    top_token = op_stack.pop()
            else:
                while not is_empty(op_stack) and self.all_op_and_func[peek(op_stack)] >= self.all_op_and_func[part_exp]:
                    polish_list.append(op_stack.pop())
                op_stack.append(part_exp)

        while not is_empty(op_stack):
            polish_list.append(op_stack.pop())
        return polish_list

    def calc(self, polish):
        """Calculate expression by polish notation."""
        stack = []
        for item in polish:
            if item == 'log':
                x, y = stack.pop(), stack.pop()
                stack.append(math.log(y, x))
            elif item in self.math_functions and not (item in self.constants):
                x = stack.pop()
                to_app = self.math_functions[item][1](x)
                stack.append(to_app)
            elif item in self.operators:
                x, y = stack.pop(), stack.pop()
                stack.append(self.operators[item][1](y, x))
            else:
                if is_int(item):
                    stack.append(int(item))
                else:
                    stack.append(float(item))
        s = 0
        if len(stack) > 1:
            for i in range(len(stack)):
                s += stack[i]
                i += 1
        else:
            return stack.pop()
        return s == len(stack)

        # print(calc(['1', '4', '>', '5', '!=', '2', '<']))
        # print(expr_parts('2>=3>5'))
        # print(polish_notation(expr_parts('1>2!=1')))
        # print(eval('2>=3'))
        # print(calc(polish_notation(expr_parts('sin(pi/2)'))))
        # d = "1+2+5+0.8*5+(4*3*(5+1))"
        # а = "1+2+5+.8*5+(4*3*(5+1))+0"
        # c = "1+2+5+.8*5+(4*3*(5+1))+0"
        # print(calc(polish_notation(expr_parts("(100)"))))
        # print(calc(polish_notation(expr_parts("666"))))
        # print(polish_notation(expr_parts("-.1")))
        # print(calc(polish_notation(expr_parts("1/3"))))
        # print(calc(polish_notation(expr_parts("1.0/3.0"))))
        # print(calc(polish_notation(expr_parts(".1 * 2.0^56.0"))))
        # print(calc(polish_notation(expr_parts("e^34"))))
        # print(calc(polish_notation(expr_parts("2.0^(pi/pi+e/e+2.0^0.0)"))))
        # print(calc(polish_notation(expr_parts("(2.0^(pi/pi+e/e+2.0^0.0))"))))
        # print(calc(polish_notation(expr_parts("(2.0^(pi/pi+e/e+2.0^0.0))^(1.0/3.0)"))))
        # print(calc(polish_notation(expr_parts("2 + log(3+1, 4)"))))
        # print(calc(polish_notation(expr_parts("sin(pi/2^1) + log(1*4+2^2+1, 3^2)"))))
        # print(polish_notation(expr_parts("10*e^0*log10(.4 -5/ -0.1-10) - -abs(-53/10) + -5")))
        # print(polish_notation(expr_parts("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)")))
        # print(calc(polish_notation(expr_parts("2.0^(2.0^2.0*2.0^2.0)"))))
        # print(polish_notation(expr_parts("sin(e^log(e^e^sin(23.0),45.0) + cos(3.0+log10(e^-e)))")))


def myresult(input_data):
    check(input_data)
    g = check_power(ca.expr_parts(input_data))
    if len(g) == 2:
        if g[0] == '-':
            exp_len_2 = g[0] + g[1]
            if is_int(g[1]):
                return int(exp_len_2)
            else:
                return float(exp_len_2)

    return ca.calc(ca.polish_notation(g))


ca = Calculator()

