from .stack_manager import Stack
from .operator_manager import operator_dict, function_dict, unary_dict
from .split_operators import SplitOperators
from .converter import Converter


class Calculator:
    def __init__(self, expression_line):
        self.parser = SplitOperators(expression_line).split_operators()
        self.converted_list = Converter(self.parser).converter()
        self.current_result = ""
        self.operands = Stack()
        self.function = Stack()
        self.func_argument = False
        self.current_operator = ""

    def _calc_on_stack(self):
        operator_on_stack = self.function.take_from_stack()
        if operator_on_stack in function_dict.values():
            if self.func_argument:
                second_operand = self.operands.take_from_stack()
                first_operand = self.operands.take_from_stack()
                try:
                    self.current_result = operator_on_stack['operator'](first_operand, second_operand)
                    self.func_argument = False
                except TypeError as err:
                    raise SyntaxError(err)
            else:
                first_operand = self.operands.take_from_stack()
                self.current_result = operator_on_stack['operator'](first_operand)
        elif operator_on_stack in operator_dict.values() or operator_on_stack in unary_dict.values():
            if len(self.operands.stack) == 1:
                second_operand = self.operands.take_from_stack()
                first_operand = 0
            else:
                second_operand = self.operands.take_from_stack()
                first_operand = self.operands.take_from_stack()
            self.current_result = operator_on_stack['operator'](first_operand, second_operand)
        elif operator_on_stack == '(':
            return self.current_result
        self.operands.put_on_stack(self.current_result)
        if len(self.function.stack) and self.function.top() is not '(':
            if self.current_operator['priority'] >= self.function.top()['priority']:
                self.current_result = self._calc_on_stack()
        return self.current_result

    def calculate(self):
        for item in self.converted_list:
            if isinstance(item, float) or isinstance(item, int):
                self.operands.put_on_stack(item)
            elif item in operator_dict.values() \
                    or item in function_dict.values() \
                    or item in unary_dict.values():
                self.current_operator = item
                if self.function.is_empty():
                    self.function.put_on_stack(self.current_operator)
                else:
                    if self.function.top() is '(' \
                            or self.current_operator['priority'] < self.function.top()['priority'] \
                            or self.current_operator == operator_dict['^'] \
                            and self.function.top() == operator_dict['^']:
                        self.function.put_on_stack(self.current_operator)
                    else:
                        self._calc_on_stack()
                        self.function.put_on_stack(self.current_operator)
            elif item is '(':
                self.function.put_on_stack(item)
            elif item is ')' and self.function.top() == '(':
                self.function.take_from_stack()
            else:
                for i in range(len(self.function.stack)):
                    if item is ',' and self.function.top() is '(':
                        if self.func_argument:
                            raise SyntaxError('This function can have only two arguments')
                        self.func_argument = True
                        break
                    elif self.func_argument:
                        self._calc_on_stack()
                    if len(self.function.stack):
                        self._calc_on_stack()
                        if item is ')' and len(self.function.stack):
                            if self.function.top() is '(':
                                self.function.take_from_stack()
                                break
        if self.function.is_empty():
            self.current_result = self.operands.take_from_stack()
        elif len(self.function.stack) == 1:
            self._calc_on_stack()
        else:
            for i in range(len(self.function.stack)):
                self._calc_on_stack()
                if self.function.is_empty():
                    break
        return self.current_result
