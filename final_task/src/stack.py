class Stack:
    """Standart stack implementation

    Attributes
    ----------
    items : list
        items stored in stack

    Methods
    -------
    isEmpty()
        returns true if the stack is empty
    push(item)
        inserts item on stack head
    pop()
        deletes stack head and returns it value
    size()
        returns number of items stored in stack
    lastItem()
        returns value of stack head

    """
    def __init__(self, *args):
        """initializes stack object

        Parameters
        ----------
        args : list
            if provided stack will be initialized with args values
        """
        self.items = args if args else []

    def is_empty(self):
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

    def last_item(self):
        """Returns value of last item from stack
        Returns
        -------
        any
            value of stack head
        """
        return self.items[len(self.items)-1]
