import unittest
from pycalc.stack_manager import Stack


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    def test_init_class(self):
        self.assertEqual([], self.stack.stack)

    def test_put_on_stack(self):
        self.stack.put_on_stack(42)
        self.assertEqual([42], self.stack.stack)

    def test_top(self):
        self.stack.put_on_stack(42)
        self.assertEqual(42, self.stack.top())
        self.assertEqual([42], self.stack.stack)

    def test_take_from_stack(self):
        self.stack.put_on_stack(42)
        result = self.stack.take_from_stack()
        self.assertEqual(42, result)
        self.assertEqual([], self.stack.stack)

    def test_is_empty_true(self):
        self.assertTrue(self.stack.is_empty())

    def test_is_empty_false(self):
        self.stack.put_on_stack(42)
        self.assertFalse(self.stack.is_empty())
