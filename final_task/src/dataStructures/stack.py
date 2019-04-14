class Stack:
    def __init__(self, *args):
        self.items = [] if len(args) == 0 else args
    def isEmpty(self):
        return self.size() == 0
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def size(self):
        return len(self.items)
