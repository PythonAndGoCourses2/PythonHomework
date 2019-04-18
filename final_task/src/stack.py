class Stack:
    """Standart stack implementation"""
    def __init__(self, *args):
        """initializes stack object

        Parameters
        ----------
        args : list
            if provided stack will be initialized with args values
        """
        self.items = args if args else []

    def isEmpty(self):
        """
        Returns
        -------
        bool
            true if stack is empty
        """
        return self.size() == 0

    def push(self, item):
        """Pushes item in stack head
             
        Parameters
        ----------
        item : any
            item to push in stack
        """
        self.items.append(item)

    def pop(self):
        """Deletes head value of stack
        Returns
        -------
        any
            item from stack head
        """
        return self.items.pop()

    def size(self):
        """
        Returns
        -------
        int
            number of elements in stack
        """
        return len(self.items)

    def lastItem(self):
        """Returns value of last item from stack
        Returns
        -------
        any
            value of stack head
        """
        return self.items[len(self.items)-1]
