import math
from calculator.validation import check_exception
import operator

OPERATION_PRIORITIES = {
    '>': 0, '<': 0, '<=': 0, '==': 0, '!=': 0, '>=': 0,
    '+': 1, '-': 1,
    '*': 2, '/': 2, '%': 2, '//': 2,
    '^': 3,
    '(': 4, ')': 4}


CALCULATE = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '%': operator.mod,
    '^': operator.pow,
    '=': operator.eq,
    '==': operator.eq,
    '<': operator.lt,
    '<=': operator.le,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt,
}


DICT_MATH = math.__dict__
DICT_MATH['round'] = round
DICT_MATH['abs'] = abs


class CALCULATOR:
    error = None
    res_expression = []
    operations = []

    def __init__(self, expression, dicts_modules=None):
        self.expression = expression
        self.translate_reverse_exception(dicts_modules)
        if self.error is None:
            self.result = self.calculate_res_exception(dicts_modules)

    def get_result(self):
        if self.error is None:
            return self.result
        else:
            return self.error

    def calculate_function(self, dicts_modules, i):
        number = self.res_expression.pop(i - 1)
        i -= 1
        args = self.res_expression[i - number:i]
        is_in_dicts_modules = False
        if dicts_modules is not None:
            for item in dicts_modules:
                if self.res_expression[i] in item:
                    self.res_expression[i] = item[self.res_expression[i]](*args)
                    is_in_dicts_modules = True
                    break
        if not is_in_dicts_modules:
            self.res_expression[i] = DICT_MATH[self.res_expression[i]](*args)
        del self.res_expression[i - number:i]

    def calculate_res_exception(self, dicts_modules):
        i = 1
        while i < len(self.res_expression):
            try:
                if self.res_expression[i] in OPERATION_PRIORITIES:
                    self.res_expression[i - 2] = CALCULATE[self.res_expression.pop(i)](self.res_expression[i - 2],
                                                                                       self.res_expression.pop(i - 1))
                    i = 1
                elif type(self.res_expression[i]) is str and self.res_expression[i].isalnum():
                    self.calculate_function(dicts_modules, i)
                    i = 1
            except KeyError:
                self.error = 'ERROR: unknown function'
                break
            except ZeroDivisionError:
                self.error = 'ERROR: division by zero'
                break
            except ValueError:
                self.error = 'ERROR: value'
                break
            except TypeError:
                self.error = 'ERROR: incorrect number of arguments'
                break
            i += 1
        else:
            if not isinstance(self.res_expression[0], (float, bool, int)):
                self.error = 'ERROR: incomplete expression'
            else:
                return self.res_expression.pop()

    def allocate_operations(self, item, i):
        if item == '-' and (not i or (self.expression[i - 1] in OPERATION_PRIORITIES and
                                      self.expression[i - 1] != ')')):
            self.res_expression.append(-1)
            self.operations.append('*')
        elif item == '+' and (not i or (self.expression[i - 1] in OPERATION_PRIORITIES and
                                        self.expression[i - 1] != ')')):
            return
        elif self.operations:
            if item == ')':
                self.unloading_operations(upload_bracket=True)
            else:
                if self.operations[-1].isalnum() or self.operations[-1] == '(':
                    self.operations.append(item)
                elif OPERATION_PRIORITIES[item] > OPERATION_PRIORITIES[self.operations[-1]] or\
                        self.operations[-1] == '(':
                    self.operations.append(item)
                elif item in OPERATION_PRIORITIES.keys() and item == self.operations[-1] == '^':
                    self.operations.append(item)
                else:
                    self.unloading_operations(OPERATION_PRIORITIES[item])
                    self.operations.append(item)
        else:
            self.operations.append(item)

    def allocate_numbers(self, i):
        number = ''
        while i < len(self.expression) and (self.expression[i].isdigit() or self.expression[i] == '.'):
            number += self.expression[i]
            i += 1
        self.res_expression.append(float(number))
        return i

    def unloading_operations(self, prior_operation=-1, upload_bracket=False):
        while self.operations and self.operations[-1] != '(' and not self.operations[-1].isalnum() \
                and OPERATION_PRIORITIES[self.operations[-1]] >= prior_operation:
            self.res_expression.append(self.operations.pop())
        else:
            if self.operations and upload_bracket:
                if self.operations[-1] == '(':
                    self.operations.pop()
                elif self.operations[-1].isalnum():
                    self.res_expression.append(self.operations.pop(-2))
                    self.res_expression.append(self.operations.pop())

    def search_func(self):
        """Looking for function to increase the argument counter
        """
        i = len(self.operations) - 1
        while not self.operations[i].isalnum():
            i = i - 1
        return i

    def write_func(self, i):
        func = ''
        while i < len(self.expression) and self.expression[i].isalnum():
            func += self.expression[i]
            i += 1
        return i, func

    def add_constant_to_res_expression(self, func, dicts_modules):
        """The function searches for a constant in the modules added via -m,
        then in the math module, if it does not find it, it gives an error
        """

        try:
            is_in_dicts_modules = False
            if dicts_modules is not None:
                for item in dicts_modules:
                    if func in item:
                        self.res_expression.append(item[func])
                        is_in_dicts_modules = True
                        break
            if not is_in_dicts_modules:
                self.res_expression.append(DICT_MATH[func])
        except KeyError:
            self.error = 'ERROR: unknown constant'

    def allocate_function(self, i, dicts_modules):
        i, func = self.write_func(i)
        if i < len(self.expression) and self.expression[i] == '(':
            self.operations.append(1)
            self.operations.append(func)
        else:
            self.add_constant_to_res_expression(func, dicts_modules)
            i -= 1
        return i

    def translate_reverse_exception(self, dicts_modules):
        i = 0
        while i < len(self.expression):
            if self.expression[i].isdigit() or self.expression[i] == '.':
                i = self.allocate_numbers(i) - 1
            elif self.expression[i] == ',':
                self.operations[self.search_func() - 1] += 1
                self.unloading_operations()
            elif i != len(self.expression) - 1 and str(self.expression[i]) + str(self.expression[i + 1])\
                    in OPERATION_PRIORITIES:
                self.allocate_operations(self.expression[i] + self.expression[i + 1], i)
                i += 1
            elif self.expression[i] in OPERATION_PRIORITIES.keys():
                self.allocate_operations(self.expression[i], i)
            elif self.expression[i].isalpha():
                i = self.allocate_function(i, dicts_modules)
                if self.error is not None:
                    return
            else:
                self.error = 'ERROR: unknown character'
                return
            i += 1
        while self.operations:
            self.unloading_operations(upload_bracket=True)


def main():
    try:
        expression, dicts_modules = check_exception()
    except Exception as error:
        print(error)
    else:
        print(CALCULATOR(expression, dicts_modules).get_result())


if __name__ == '__main__':
    main()
