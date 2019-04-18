import unittest, mymodule,math

class Testmyfunction(unittest.TestCase):

  def test_del_space(self):
      self.assertEqual(mymodule.del_space(' + 1'),'+1')
      self.assertEqual(mymodule.del_space('1 + + -1 +'),'1++-1+')

  def test_replace_many_plus_minus(self):
      self.assertEqual(mymodule.replace_many_plus_minus('+-1*3+++2'),'-1*3+2')
  
  def test_plus_reject(self):
      self.assertEqual(mymodule.plus_reject('3'), ['3'])
      self.assertEqual(mymodule.plus_reject('3+2'), ['3','2'])
      self.assertEqual(mymodule.plus_reject('3-1'), ['3','-1'])
      self.assertEqual(mymodule.plus_reject('3+'), ['3',''])
  
  
  def test_result(self):
      self.assertEqual(mymodule.result('1*3'),3.0)
      self.assertEqual(mymodule.result('1*3/3'),1.0)
      self.assertEqual(mymodule.result('1*3^2*2'),18.0)
      self.assertEqual(mymodule.result('1*-3'),-3.0)
      self.assertEqual(mymodule.result(' 1 *-3'),-3.0)
      self.assertEqual(mymodule.result('3%3'),0)
      self.assertEqual(mymodule.result('-1^3^2'),-1.0)
      self.assertEqual(mymodule.result('e*-3'),-3.0*math.e)
      self.assertEqual(mymodule.result('pi*e*-tau'),-math.pi*math.e*math.tau)
      with self.assertRaises(ValueError):
          mymodule.result('1*')
          mymodule.result('1-')
          mymodule.result('p*2')
          mymodule.result('2**2')
          mymodule.result('/2')
          mymodule.result('')
  def test_calc(self):
      self.assertEqual(mymodule.calc('- - 1* 3'), 3.0)
      self.assertEqual(mymodule.calc('  2 - -1^ - 3'), 3)
      self.assertEqual(mymodule.calc('1-5 / 5* 3'),-2.0)
      self.assertEqual(mymodule.calc('1* 3^2/ - 1'),-9.0)
      with self.assertRaises(ValueError):
          mymodule.calc('1 *')
          mymodule.calc('p * 2')
          mymodule.calc(' * -e')
          mymodule.calc('1-')
  def test_find_brakets(self):
      self.assertEqual(mymodule.find_brackets('(- - 1* 3  )'), '3.0')
      with self.assertRaises(ValueError):
          mymodule.find_brackets('1+2)')
          mymodule.find_brackets('( 1+2')
          mymodule.find_brackets('( (')
  def test_find_func(self):
      self.assertEqual(mymodule.find_func('sin3',3,[3]), str(math.sin(3)))
      self.assertEqual(mymodule.find_func('  sin  3',7,[3]), str(math.sin(3)))
      with self.assertRaises(KeyError):
          mymodule.find_func('si(3)',2,[3])
          





if __name__ == '__main__':
    unittest.main()
