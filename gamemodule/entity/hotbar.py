from gamemodule.entity.base import Entity
import pygame

class Hotbar(Entity):

    def __init__(self, amount, game, spawn, dimensions, colour):

        super().__init__(game, spawn, dimensions, colour)
        self.amount = amount

        self.slots = {x: None for x in range(amount)}

    def draw(self, surface, **kwargs):

        c, x, y, w, h = self.modular_traits(**kwargs)

        for slot, val in self.slots.items():

            pygame.draw.rect(surface, c, ((x + (w * slot)), y, w, h), 2)

            if val is not None:

                vc = val.colour

                # For now, draw representation of it

                # pygame.draw.rect(surface, vc, ((x + (w * slot) + 5), y + 5, w-10, h-10))

                val.draw(surface, x=(x + (w * slot) + 5), y=y+5, w=w-10, h=h-10)

    def draw_hitbox(self, screen):

        x, y = int(self.x) - 2, int(self.y) - 2
        w, h = int(self.w), int(self.h)

        # Bottom
        pygame.draw.line(screen, (255, 0, 0), (x, y + h),
                         ((x + (w * len(self.slots))), y + h), 2)
        # Left
        pygame.draw.line(screen, (0, 255, 0), (x, y),
                         (x, y + h), 2)
        # Top
        pygame.draw.line(screen, (0, 0, 255), (x, y),
                         ((x + (w * len(self.slots))), y), 2)
        # Right
        pygame.draw.line(screen, (255, 0, 255), ((x + (w * len(self.slots))), y),
                         ((x + (w * len(self.slots))), y + h), 2)

    def frame(self):

        c, x, y, w, h = self.modular_traits()

        for slot, val in self.slots.items():

            r = pygame.Rect(((x + (w * slot)), y, w, h))

            if self.game.mouse.leftdown() and self.game.mouse.grabbed is None:

                if r.collidepoint(self.game.mouse.pos):

                    picked = self.slots[slot]

                    if picked is None:

                        return

                    self.game.mouse.grabbed = picked
                    self.game.entities.push(picked)
                    self.game.log.push(f'Mouse interacted with hotbar slot({slot}) --> removed from inventory')
                    self.slots[slot] = None

                    break