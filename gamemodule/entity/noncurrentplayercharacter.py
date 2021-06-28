from gamemodule.entity.playercharacter import PlayerCharacterEntity
import pygame

class NonCurrentPlayerCharacterEntity(PlayerCharacterEntity):

    def __init__(self, game, spawn, dimensions, colour):

        super().__init__(game, spawn, dimensions, colour)

    def gravity(self):

        if self.do_gravity and self.game.get_condition('gravity') == True:

            self.jump_velocity = 0

            if not self.grounded:

                self.y += int(self.fall_velocity / 2)
                self.fall_velocity += 1

            else:

                self.jump_velocity = 1
                self.fall_velocity = 1 * self.jump_velocity
                self.jump_start = self.y

    def draw(self, surface, **kwargs):

        c, x, y, w, h = self.modular_traits(**kwargs)

        # Split difference for radius
        sd = int((w/h)*w)
        sd /= 2

        pygame.draw.circle(surface, c, (x+sd, y+sd), sd)

NCPC = NonCurrentPlayerCharacterEntity