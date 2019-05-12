import io
import unittest
from unittest.mock import patch
from pycalc import main


class TestPycalcFunction(unittest.TestCase):
    def test_main(self):
        with self.subTest("calls methods parse_query, update, check_expression, replace_all_mathes, convert_answer"), \
             patch('pycalc.parse_query') as parse_query, \
             patch('pycalc.Library.update') as import_modules, \
             patch('pycalc.check_expression') as check_expression, \
             patch('pycalc.has_comparator') as has_comparator, \
             patch('pycalc.replace_all_mathes') as replace_all_mathes, \
             patch('pycalc.convert_answer', return_value='1') as convert_answer, \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            main()
            self.assertEqual(mock_stdout.getvalue(), '1\n')

            self.assertTrue(parse_query.called)
            self.assertTrue(import_modules.called)
            self.assertTrue(replace_all_mathes.called)
            self.assertTrue(has_comparator.called)
            self.assertTrue(check_expression.called)
            self.assertTrue(convert_answer.called)

        with self.subTest("catchs exception"), \
                patch('pycalc.parse_query') as parse_query, \
                patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            main()
            self.assertTrue(mock_stdout.getvalue().startswith('ERROR: '))


if __name__ == '__main__':
    unittest.main()
