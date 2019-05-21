class Stack:
    __stack = []

    def push(self, element):
        try:
            self.__stack.append(element)
            return True
        except:
            return False

    def pop(self):
        try:
            return self.__stack.pop()
        except:
            return False

    def is_empty(self):
        if len(self.__stack) == 0:
            return True
        else:
            return False
