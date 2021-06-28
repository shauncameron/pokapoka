class Stack:

    def __iter__(self):

        return self

    def __next__(self):

        if self.__iter_n__ < len(self.__stack__):

            item = self.__stack__[self.__iter_n__]
            self.__iter_n__ += 1

            return item

        else:

            self.__iter_n__ = 0
            raise StopIteration

    def __init__(self):

        self.__iter_n__ = 0
        self.__stack__ = []

    def pull(self):

        if len(self.__stack__):

            res = self.__stack__.pop(0)

            return res

        else:

            return None

    def push(self, other):

        self.__stack__.insert(0, other)

        return self

    def remove(self, other):

        if other in self.__stack__:

            self.__stack__.remove(other)

    @property
    def front(self):

        return self.__stack__[0] if len(self.__stack__) else None

    @property
    def back(self):

        return self.__stack__[-1] if len(self.__stack__) else None

    @property
    def list(self):

        return self.__stack__

    @property
    def set(self):

        return set(self.list)

class FixedSizeStack(Stack):

    def __init__(self, size):

        super().__init__()
        self.max = size

    def push(self, other):

        if len(self.__stack__) < self.max:

            return Stack.push(self, other)

        else:

            return None