import unittest
from pycalc import pycalc


class TestStringMethods(unittest.TestCase):

    def test_brackets_count(self):
        self.assertEqual(pycalc.brackets_count('12+(100-10)'), '12+(100-10)')
        with self.assertRaises(pycalc.InternalError):
            pycalc.brackets_count('12+((100-10)')

    def test_transformathion_stack_expr(self):
        self.assertEqual(pycalc.transformathion_stack_expr('1+1'), ['1', '+', '1'])

    def test_replacement_signs(self):
        self.assertEqual(pycalc.replacement_signs('10--10'), '10+10')

    def test_replacement_cleaning(self):
        self.assertEqual(pycalc.replacement_cleaning('(2+2*2)', ['1', '+', '(', '2', '+', '2', '*', '2', ')',
                                                     '-', '3'], '6.0', [8], [2]), '1+6.0-3')

    def test_account(self):
        self.assertEqual(pycalc.account(['*'], ['5', '5']), '25.0')
        with self.assertRaises(pycalc.InternalError):
            pycalc.account(['/'], ['5', '0'])

    def test_calculate_expr(self):
        self.assertEqual(pycalc.calculate_expr(['1']), '1')
        self.assertEqual(pycalc.calculate_expr(['1', '+', '2']), '3.0')

    def test_pi_e(self):
        self.assertEqual(pycalc.pi_e(['pi', '+', 'pi']), ['3.141592653589793', '+', '3.141592653589793'])
        self.assertEqual(pycalc.pi_e(['pi']), ['3.141592653589793'])
        self.assertEqual(pycalc.pi_e(['e', '+', 'e']), ['2.718281828459045', '+', '2.718281828459045'])
        self.assertEqual(pycalc.pi_e(['e']), ['2.718281828459045'])

    def test_subfinder(self):
        self.assertEqual(pycalc.subfinder(['1', '+', 'log', '10', '(', '100', ')'], ['log', '10']),
                         ['1', '+', 'log10', '(', '100', ')'])
        self.assertEqual(pycalc.subfinder(['1', '+', 'log', '2', '(', '100', ')'], ['log', '2']),
                         ['1', '+', 'log2', '(', '100', ')'])
        self.assertEqual(pycalc.subfinder(['1', '+', 'log', '1', 'p', '(', '100', ')'], ['log', '1', 'p']),
                         ['1', '+', 'log1p', '(', '100', ')'])
        self.assertEqual(pycalc.subfinder(['1', '+', 'atan', '2', '(', '90', '3', ')'], ['atan', '2']),
                         ['1', '+', 'atan2', '(', '90', '3', ')'])

    def test_stack_math_with_number(self):
        self.assertEqual(pycalc.stack_math_with_number(['1', '+', 'log', '10', '(', '100', ')']),
                         ['1', '+', 'log10', '(', '100', ')'])
        self.assertEqual(pycalc.stack_math_with_number(['1', '+', 'log', '2', '(', '100', ')']),
                         ['1', '+', 'log2', '(', '100', ')'])
        self.assertEqual(pycalc.stack_math_with_number(['1', '+', 'atan', '2', '(', '90', '3', ')']),
                         ['1', '+', 'atan2', '(', '90', '3', ')'])

    def test_transformathion_stack(self):
        self.assertEqual(pycalc.transformathion_stack('1+1'), ['1', '+', '1'])
        self.assertEqual(pycalc.transformathion_stack('3-log(8)'), ['3', '-', 'log', '(', '8', ')'])
        self.assertEqual(pycalc.transformathion_stack('3-log10(100)'), ['3', '-', 'log10', '(', '100', ')'])
        self.assertEqual(pycalc.transformathion_stack('1'), ['1'])
        self.assertEqual(pycalc.transformathion_stack('-10+(-100-10)'), ['-10', '+', '(', '-100', '-', '10', ')'])

    def test_round_not_math(self):
        self.assertEqual(pycalc.round_not_math(['123.45456', ',', '2'], ['round', '(', '123.45456', ',', '2', ')'],
                                               [1], [5], ''), '123.45')
        self.assertEqual(pycalc.round_not_math(['123.456'], ['round', '(', '123.456', ')'],
                                               [1], [3], ''), '123')
        self.assertEqual(pycalc.round_not_math(['123.66', ',', '1'], ['round', '(', '123.66', ',', '1', ')'],
                                               [1], [5], ''), '123.7')

    def test_check_in_math(self):
        self.assertEqual(pycalc.check_in_math('log'), True)
        with self.assertRaises(pycalc.InternalError):
            pycalc.check_in_math('logf')

    def test_calculate_brack(self):
        self.assertEqual(pycalc.calculate_brack(['1', '+', '(', '10', '-', '4', ')']), ['1', '+', '6.0'])
        self.assertEqual(pycalc.calculate_brack(['1', '+', 'log2', '(', '8', ')']), ['1', '+', '3.0'])
        self.assertEqual(pycalc.calculate_brack(['1', '+', 'copysign', '(', '10', ',', '-', '2', ')']),
                                                ['1', '-', '10.0'])
        self.assertEqual(pycalc.calculate_brack(['1', '+', 'abs', '(', '-10', ')']), ['1', '+', '10'])
        self.assertEqual(pycalc.calculate_brack(['1', '+', 'round', '(', '10.34', ',', '1', ')']), ['1', '+', '10.3'])
        self.assertEqual(pycalc.calculate_brack(['1', '+', 'fsum', '(', '[', '1', ',', '2', ',', '3', ']', ')']),
                                                ['1', '+', '6.0'])
        with self.assertRaises(pycalc.InternalError):
            pycalc.calculate_brack(['1', '+', 'fsum', '(', '1', ',', '2', ',', '3', ']', ')'])

    def test_calculate(self):
        self.assertEqual(pycalc.calculate(['1', '-', '10']), '-9.0')

    def test_entry(self):
        self.assertEqual(pycalc.entry('10<11'), ([2], ['<']))
        self.assertEqual(pycalc.entry('10<=11'), ([2, 3], ['<=', '=']))

    def test_value(self):
        self.assertEqual(pycalc.value(([2], ['<']), '10<11'), ('10', '11'))
        self.assertEqual(pycalc.value(([2, 3], ['<=', '=']), '10<=11'), ('10', '11'))

    def test_comparasion(self):
        self.assertEqual(pycalc.comparasion(([2], ['<']), ('10', '11')), True)
        self.assertEqual(pycalc.comparasion(([2], ['>']), ('10', '11')), False)
        self.assertEqual(pycalc.comparasion(([2, 3], ['!=', '=']), ('10', '11')), True)
        self.assertEqual(pycalc.comparasion(([2, 3], ['==', '=']), ('10', '11')), False)

    def test_calculathion_on_functhions(self):
        self.assertEqual(pycalc.calculathion_on_functhions('12+(-10+12)'), '14.0')
        self.assertEqual(pycalc.calculathion_on_functhions('12+56'), '68.0')

    def test_calculathion_comparison_of_expression(self):
        self.assertEqual(pycalc.calculathion_comparison_of_expression('12+(-10+12)'), '14.0')
        self.assertEqual(pycalc.calculathion_comparison_of_expression('12+56'), '68.0')
        self.assertEqual(pycalc.calculathion_comparison_of_expression('12>10'), True)
        self.assertEqual(pycalc.calculathion_comparison_of_expression('12==12'), True)
        self.assertEqual(pycalc.calculathion_comparison_of_expression('12<10'), False)


if __name__ == '__main__':
    unittest.main()
