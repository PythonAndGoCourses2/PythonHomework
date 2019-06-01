import unittest

from final_task.pycalc_proc import PyCalcProcessing


calc_obj = PyCalcProcessing('1')


class TestParsingNegativeCases(unittest.TestCase):
    def test1(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1+&6.0'))

    def test86(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1+6.0&'))

    def test87(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('_5+6'))

    def test88(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('5_+6'))

    def test89(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1>=@'))

    def test90(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1@>=9'))

    def test91(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('-2+(#+1)'))

    def test92(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('abs(@)'))

    def test93(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('round(@)'))

    def test94(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('sin(5+@)'))

    def test95(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('sin(@+5)'))

    def test96(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('(5+@)/7'))

    def test97(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1+#+6'))

    def test98(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1+#8+6'))

    # Number with more than one delimiter
    def test99(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1..5'))

    def test100(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('-1..5'))

    def test101(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1..5+3..7'))

    def test102(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1..5+3'))

    def test103(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('3+1..5'))

    def test104(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1+1..5-4'))

    def test105(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('sin(1..5)'))

    def test106(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('(1..5+3)/2'))

    def test107(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('round(1..5)'))

    def test108(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('abs(-1..5)'))

    def test109(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate('1>=1..5'))

    def test110(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate(''))

    def test111(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate(None))

    def test112(self):
        self.assertRaises(ValueError, lambda: calc_obj.pre_validate(18))


if __name__ == '__main__':
    unittest.main()
