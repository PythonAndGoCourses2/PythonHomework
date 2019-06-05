"""Stack module"""


class Stack:
    """Stack class"""
    def __init__(self):
        """
        Generates an instance of the Stack object
        """
        self.stack = list()

    def put_on_stack(self, item):
        """
        Appends an item to the container
        """
        self.stack.append(item)

    def top(self):
        """
        Returns a last item from stack
        """
        return self.stack[-1]

    def take_from_stack(self):
        """
        Remove and returns a last item from stack
        """
        return self.stack.pop()

    def is_empty(self):
        """
        Returns True if no items on a stack, otherwise returns False
        """
        if len(self.stack) == 0:
            return True
        else:
            return False
