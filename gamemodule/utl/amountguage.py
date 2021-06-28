import pygame
from time import sleep
from _thread import start_new_thread

gauges = []

def timer():

    while True:

        for g in gauges:

            g.refill()

        sleep(0.01)

#start_new_thread(timer, ())

class Gauge:

    def __add__(self, other):

        return self.add(other)

    def __iadd__(self, other):

        return self.add(other)

    def __sub__(self, other):

        return self.sub(other)

    def __isub__(self, other):

        return self.sub(other)

    def __init__(self, default, min=0, max=100, refill=0.2, w=500, h=40, colour=(255, 0, 0), spawn=(10, 10)):

        self.refill_rate = refill
        self.min, self.max = min, max
        self.w, self.h = w, h
        self.colour = colour
        self.r, self.g, self.b = self.colour
        self.spawn = spawn
        self.x, self.y = self.spawn
        self.default = default
        self.__gauge__ = self.default

        if self.max == 0:

            raise ZeroDivisionError('Setting the maximum for a gauge as zero prefaces a zero divison error and shouldn\'t happen anyway')

        gauges.append(self)

    @property
    def gauge(self):

        return self.__gauge__

    def add(self, new):

        if self.min <= self.__gauge__ + new <= self.max:

            self.__gauge__ += new

        return self

    def sub(self, amt):

        if self.max >= self.__gauge__ - amt >= self.min:

            self.__gauge__ -= amt

        return self

    def draw(self, surface):

        notch = self.w // self.max

        # Gauge outlien
        pygame.draw.rect(surface, (51, 51, 51), (self.x - 2, self.y - 2, self.w + 4, self.h + 4))

        # Gauge representation
        for i in range(int(self.gauge)):

            r, g, b = self.colour
            r = r - i * 2 if r - i * 2 >= 0 else 0
            g = g - i * 2 if g - i * 2 >= 0 else 0
            b = b - i * 2 if b - i * 2 >= 0 else 0

            pygame.draw.rect(surface, (r, g, b), (self.x + i * notch, self.y, notch, self.h))

    def refill(self):

        self.add(self.refill_rate)