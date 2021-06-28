from gamemodule.entity.base import Entity
import pygame
import random

gases = []
gas_cap = 1000

class GasEntity(Entity):

    def __init__(self, game, amount, xstep=1, ystep=1, life=5, stretch=50, spawn=(10, 10), colour=(255, 255, 255), origin=None):

        super().__init__(game, spawn, (stretch, stretch), colour)

        self.ro, self.go, self.bo = self.r, self.g, self.b

        self.justify = True
        self.amount = amount
        self.life = life
        self.stretch = stretch
        self.deviation = 0
        self.origin = origin

        self.xstep, self.ystep = xstep, ystep

        self.living_frames = 0

        global gases, gas_cap

        gases.append(self)

        r, g, b = self.colour

        self.die = False

        if (len(gases) >= gas_cap) or (r <= 10 and g <= 10 and b <= 10):

            self.die = True


    def draw(self, surface, **kwargs):

        global gases, gas_cap

        r, g, b = self.colour

        if (len(gases) >= gas_cap) or (r <= 10 and g <= 10 and b <= 10): self.die = True

        if self.die:

            if self in self.game.entities.list:

                self.game.entities.remove(self)

            if self in gases:

                gases.remove(self)

        r -= self.life if r > self.life else 0; g -= self.life if g > self.life else 0; b -= self.life if b > self.life else 0; self.r, self.g, self.b = r, g, b

        su = pygame.Surface(pygame.rect.Rect(self.get_rect()).size, pygame.SRCALPHA)
        su.set_alpha(255)
        pygame.draw.circle(su, (r, g, b), (self.x, self.y), 20)
        surface.blit(su, (self.x, self.y))

        pygame.draw.circle(surface, (r, g, b), (self.x, self.y), 10)

        # Lighting

    def frame(self):

        global gases, gas_cap

        r, g, b = self.colour

        if (len(gases) >= gas_cap) or (r <= 10 and g <= 10 and b <= 10): self.die = True

        if self.die:

            if self in self.game.entities.list:

                self.game.entities.remove(self)

            if self in gases:

                gases.remove(self)

        self.x += self.xstep
        self.y += self.ystep + random.randint(-1, 1)
        self.deviation += int((self.xstep + self.ystep) / 2)

        if (-50 > self.x > self.game.ww + 50) or (-50 > self.y > self.game.wh + 50) :

            self.game.entities.remove(self)

    def get_rect(self):

        self_rect = (self.x - 5, self.y - 5, 10, 10)

        return self_rect

    def colliderect(self, rect):

        self_rect = (self.x - 5, self.y - 5, 10, 10)
        return pygame.rect.Rect(self_rect).colliderect(rect)

    def collidepos(self, pos):

        self_rect = (self.x - 5, self.y - 5, 10, 10)
        return pygame.rect.Rect(self_rect).collidepoint(pos)

    def draw_hitbox(self, screen):

        self_rect = (self.x - 5, self.y - 5, 10, 10)
        x, y, w, h = self_rect

        x, y = int(x), int(y)
        w, h = int(w), int(h)

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