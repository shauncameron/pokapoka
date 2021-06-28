class Queue:

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

        self.__queue__ = []

    def pull(self):

        if len(self.__queue__):

            return self.__queue__[0]

        else:

            return None

    def push(self, other):

        self.__queue__.append(other)

        return self

    def remove(self, other):

        self.__queue__.remove(other)

    @property
    def front(self):

        return self.__queue__[0] if len(self.__queue__) else None

    @property
    def back(self):

        return self.__queue__[-1] if len(self.__queue__) else None

    @property
    def list(self):

        return self.__queue__

class FixedSizeQueue(Queue):

    def __init__(self, size):

        super().__init__()
        self.max = size

    def push(self, other):

        if len(self.__queue__) < self.max:

            Queue.push(self, other)