import pygame

class Mouse:

    def __init__(self):

        self.grabbed = None

    @property
    def pos(self):

        return pygame.mouse.get_pos()

    def leftdown(self):

        return pygame.mouse.get_pressed()[0]