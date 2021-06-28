import pygame
from gamemodule.utl.util import validate_rgb, is_negative, is_positive

class Entity:

    def __repr__(self):

        return f"""Entity[rgb({self.r}-{self.g}-{self.b}), size({self.w}-{self.h}) @ pos({self.x}-{self.y})]"""

    def __init__(self, game, spawn: [int, int] = (100, 100), dimensions: [int, int] = (50, 50), colour: [int, int, int] = (255, 255, 255), toss_velocity=4):


        self.tx, self.ty = 0, 0
        self.tv = toss_velocity

        self.__game__ = game

        self.__spawn__ = spawn
        self.__x__, self.__y__ = self.__spawn__

        self.__dimensions__ = dimensions
        self.__w__, self.__h__ = self.__dimensions__
        self.__width__, self.__height__ = self.__dimensions__

        self.__colour__ = colour
        self.__r__, self.__g__, self.__b__ = self.__colour__

        self.move_velocity = 0

    @property
    def left(self):

        return is_negative(self.x + self.move_velocity)

    @property
    def right(self):

        return not self.left

    @property
    def down(self):

        return is_negative(self.y + self.move_velocity)

    @property
    def up(self):

        return not self.down

    @property
    def game(self):

        return self.__game__

    @property
    def x(self):

        return self.__x__

    @x.setter
    def x(self, other: int):

        self.__x__ = other

    @property
    def y(self):

        return self.__y__

    @y.setter
    def y(self, other: int):

        self.__y__ = other

    @property
    def pos(self):

        return self.x, self.y

    @property
    def w(self):

        return self.__w__

    @w.setter
    def w(self, other: int):

        self.__w__ = other

    @property
    def h(self):

        return self.__h__

    @h.setter
    def h(self, other: int):

        self.__h__ = other

    @property
    def dimensions(self):

        return self.w, self.h

    @property
    def r(self):

        return self.__r__

    @r.setter
    def r(self, other: int):

        self.__r__ = other

    @property
    def g(self):

        return self.__g__

    @g.setter
    def g(self, other: int):

        self.__g__ = other

    @property
    def b(self):

        return self.__b__

    @b.setter
    def b(self, other: int):

        self.__b__ = other

    @property
    def colour(self):

        return self.r, self.g, self.b

    @property
    def rgb(self):

        return self.colour

    @property
    def rect(self):

        return pygame.rect.Rect(self.x, self.y, self.w, self.h)

    def change_pos(self, xy: [int, int] = None, x: int = None, y: int = None):

        if xy is not None:

            self.x, self.y = xy

            return self

        elif x is not None or y is not None:

            if x is not None:
                self.x = x

            if y is not None:
                self.y = y

            return self

        else:

            raise ReferenceError('Expected either \'xy\' or \'x\' or \'y\' to be set; instead got none')

    def change_size(self, wh: [int, int] = None, w: int = None, h: int = None):

        if wh is not None:

            self.w, self.h = wh

            return self

        elif w is not None or h is not None:

            if w is not None:
                self.w = w

            if h is not None:
                self.h = h

            return self

        else:

            raise ReferenceError('Expected either \'wh\' or \'w\' or \'h\' to be set; instead got none')

    def change_colour(self, rgb: [int, int, int] = None, r: int = None, g: int = None, b: int = None):

        if rgb is not None:

            # Validate rgb

            [validate_rgb(d) for d in rgb]

            self.r, self.g, self.b = rgb

        elif r is not None or g is not None or b is not None:

            if r is not None:
                validate_rgb(r)

                self.r = r

            if g is not None:
                validate_rgb(g)

                self.g = g

            if b is not None:
                validate_rgb(b)

                self.b = b

    def modular_traits(self, c: [int, int, int] = None, x: int = None, y: int = None, w: int = None, h: int = None,
                       *args, **kwargs):

        c, x, y, w, h = self.colour if c is None else c, self.x if x is None else x, self.y if y is None else y, self.w if w is None else w, self.h if h is None else h

        if len(args):

            raise ReferenceError(f'Expected no args but got {args} of len {len(args)}')

        if len(kwargs):
            raise ReferenceError(f'Expected no keyword args but got {kwargs} of len {len(kwargs)}')

        return c, x, y, w, h

    def colliderect(self, rect):

        return pygame.rect.Rect(*self.rect).colliderect(rect)

    def collidepos(self, pos):

        return pygame.rect.Rect(*self.rect).collidepoint(*pos)

    def draw(self, surface, **kwargs):

        c, x, y, w, h = self.modular_traits(**kwargs)

        pygame.draw.rect(surface, c, (x, y, w, h))
        pygame.draw.rect(surface, c, (x, y, w, h))

    def draw_hitbox(self, screen):

        x, y = int(self.x), int(self.y)
        w, h = int(self.w), int(self.h)

        # Bottom
        pygame.draw.line(screen, (255, 0, 0), (x, y + h),
                         (x + w, y + h), 2)
        # Left
        pygame.draw.line(screen, (0, 255, 0), (x, y),
                         (x, y + h), 2)
        # Top
        pygame.draw.line(screen, (0, 0, 255), (x, y),
                         (x + w, y), 2)
        # Right
        pygame.draw.line(screen, (255, 0, 255), (x + w, y),
                         (x + w, y + h), 2)

    def move(self):

        if self.tx > 0: self.tx -= self.tv
        elif self.tx < 0: self.tx += self.tv

        if self.tx > 0: self.tx -= self.tv
        elif self.tx < 0: self.tx += self.tv

    def frame(self):

      return self
