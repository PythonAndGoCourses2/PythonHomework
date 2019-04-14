from collections import deque
class Queue:
    def __init__(self, *args):
        self.items = deque(args)
    def isEmpty(self):
        return len(self.items) == 0
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if self.isEmpty():
            return None
        return self.items.popleft()
    def pushFront(self, item):
        self.items.appendleft(item)
