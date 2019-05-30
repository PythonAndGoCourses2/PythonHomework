import unittest
from PythonHomework.final_task.scr import find_open_and_close_brackets, define_func_attributes, define_funcs_in_expression


class TokenizeTest(unittest.TestCase):

    def test_tokenize(self):
        self.assertEqual(tokenize("(2+2)*sin(5)"), ['(', '2', '+', '2', ')', '*', 'sin', '(', '5', ')'])


class PreparedTokenizedExpessionTest(unittest.TestCase):
    def test_find_open_and_close_brackets(self):
        self.assertEqual(find_open_and_close_brackets(
            ['log', '(', '15', '+', '7', ',', 'sin', '(', '84', '+', '(', '8', '-', '2', ')', ')', ',', '78', ')']),
            {10: 14, 7: 15, 1: 18})

    def test_define_func_attributes(self):
        self.assertEqual(
            define_func_attributes(
                ['log', '(', 'sin', '(', '84', '+', '(', '8', '-', '2', ')', ')', ',', 'cos', '(', '3', ',', '4', ')',
                 ',', 'cos', '(', ')', ',', '23', ')']),
            ('log', 4))

    def test_define_funcs_in_expression(self):
        self.assertEqual(define_funcs_in_expression(['1', '+', '(', '2', '+', '3', '*', '2', ')', '*', '3']),
                         ['1', '+@2', '(', '2', '+@2', '3', '*', '2', ')', '*', '3'])
        self.assertEqual(define_funcs_in_expression(['log10', '(', '100', ')']), ['log10@1', '(', '100', ')'])
        self.assertEqual(define_funcs_in_expression(
            ['sin', '(', '2', '-', '1', ')', '+', 'cos', '(', '9', ')', '+', '2']),
            ['sin@1', '(', '2', '-@2', '1', ')', '+@2', 'cos@1', '(', '9', ')', '+@2', '2'])


class ReversePolishNotationTest(unittest.TestCase):

    def test_ispostfix_func(self):
        self.assertEqual(ispostfix_func('!'), True)
        self.assertEqual(ispostfix_func('/'), False)

    def test_isprefix_func(self):
        self.assertEqual(isprefix_func('cos'), True)
        self.assertEqual(isprefix_func('log10'), True)
        self.assertEqual(isprefix_func('lol'), False)

    def test_isconstant(self):
        self.assertTrue('pi')
        self.assertTrue('e')

    def test_isopenbracket(self):
        self.assertEqual(isopenbracket('('), True)
        self.assertEqual(isopenbracket(')'), False)
        self.assertEqual(isopenbracket('3'), False)
        self.assertEqual(isopenbracket('sin'), False)

    def test_isclosebracket(self):
        self.assertEqual(isclosebracket('('), False)
        self.assertEqual(isclosebracket(')'), True)
        self.assertEqual(isclosebracket('9'), False)
        self.assertEqual(isclosebracket('log'), False)

    def test_isbinary(self):
        self.assertEqual(isbinary('+'), True)
        self.assertEqual(isbinary('-'), True)
        self.assertEqual(isbinary('*'), True)
        self.assertEqual(isbinary('/'), True)
        self.assertEqual(isbinary('//'), True)
        self.assertEqual(isbinary('%'), True)
        self.assertEqual(isbinary('^'), True)
        self.assertEqual(isbinary('cos'), False)
        self.assertEqual(isbinary('!'), False)
        self.assertEqual(isbinary('10'), False)

    def test_priority(self):
        self.assertEqual(priority('^'), 100)
        self.assertEqual(priority('~'), 90)
        self.assertEqual(priority('*'), 80)
        self.assertEqual(priority('/'), 80)
        self.assertEqual(priority('%'), 80)
        self.assertEqual(priority('//'), 80)
        self.assertEqual(priority('+'), 70)
        self.assertEqual(priority('-'), 70)
        self.assertEqual(priority('>>'), 60)
        self.assertEqual(priority('<<'), 60)
        self.assertEqual(priority('&'), 50)
        self.assertEqual(priority('|'), 40)
        self.assertEqual(priority('<='), 30)
        self.assertEqual(priority('<'), 30)
        self.assertEqual(priority('>='), 30)
        self.assertEqual(priority('>'), 30)
        self.assertEqual(priority('<>'), 25)
        self.assertEqual(priority('=='), 25)
        self.assertEqual(priority('!='), 25)
        self.assertEqual(priority('='), 20)
        self.assertEqual(priority('%='), 20)
        self.assertEqual(priority('/='), 20)
        self.assertEqual(priority('-/='), 20)
        self.assertEqual(priority('+/='), 20)
        self.assertEqual(priority('*/='), 20)
        self.assertEqual(priority('^/='), 20)
        self.assertEqual(priority('**/='), 20)
        self.assertEqual(priority('is'), 15)
        self.assertEqual(priority('is not'), 15)
        self.assertEqual(priority('in'), 15)
        self.assertEqual(priority('not in'), 15)
        self.assertEqual(priority('not'), 10)
        self.assertEqual(priority('and'), 10)
        self.assertEqual(priority('('), 1)
        self.assertEqual(priority(')'), 1)

    def test_isleft_associative(self):
        self.assertEqual(isleft_associative('^'), False)
        self.assertEqual(isleft_associative('+'), True)
        self.assertEqual(isleft_associative('-'), True)
        self.assertEqual(isleft_associative('/'), True)
        self.assertEqual(isleft_associative('*'), True)

    def test_is_float(self):
        self.assertEqual(is_float('2.2'), True)
        self.assertEqual(is_float('2'), False)
        self.assertTrue(is_float('15.56'))
        self.assertFalse(is_float('98'))

    def test_convert_to_RPN(self):
        self.assertEqual(convert_to_RPN(['2', '+', '2.2']), ['2', '2.2', '+'])
        self.assertNotEqual(convert_to_RPN(['2', '+', '2.2']), ['2', '+', '2.2'])
        self.assertEqual(convert_to_RPN(['sin', '(', '3', '+', '6', ')']), ['3', '6', '+', 'sin'])
        self.assertEqual(convert_to_RPN(['5', '+', '3', ]), ['5', '3', '+'])
        self.assertEqual(convert_to_RPN(['3', '*', '1', '+', '(', '6', '-', '4', ')']),
                         ['3', '1', '*', '6', '4', '-', '+'])
        self.assertEqual(convert_to_RPN(['13', '+', '27', '-', '20', '*', '2', '+', '1']),
                                        ['13', '27', '+', '20', '2', '*', '-', '1', '+'])
        self.assertEqual(convert_to_RPN(['(', '1', '+', '2', ')', '*', '(', '3', '-', '4', ')']),
                         ['1', '2', '+', '3', '4', '-', '*'])


class EvaluateTest(unittest.TestCase):
    def test_is_operand(self):
        self.assertTrue(is_operand('1'))
        self.assertTrue(is_operand('568'))
        self.assertTrue(is_operand('2.34'))
        self.assertTrue(is_operand('92.9'))
        self.assertFalse(is_operand('cos'))
        self.assertFalse(is_operand('-'))
        self.assertFalse(is_operand('not'))

    def test_convert_to_proper_type(self):
        self.assertEqual(convert_to_proper_type('13'), 13)
        self.assertEqual(convert_to_proper_type('23.8'), 23.8)

    def test_calculate(self):
        self.assertEqual(calculate(['2', '4', '*']), 8)
        self.assertEqual(calculate(['5', '3', '+', ]), 8)
        self.assertEqual(calculate(['3', '6', '+', 'sin@1']), 0.4121184852417566)


if __name__ == '__main__':
    unittest.main()