from gamemodule.entity.base import Entity
from gamemodule.entity.gas import GasEntity

class PortalBlock(Entity):

    def __init__(self, game, spawn, dimensions, colour):

        super().__init__(game, spawn, dimensions, colour)
        self.pair = None
        self.direction = 0

    def frame(self):

        if not self.pair:

            raise ValueError('Cannot have a portal block with no pair assigned in frame, please use \'create_portal_pair()\'')

        for entity in self.game.entities.set:

            if entity is not self and entity is not self.pair:

                if entity.colliderect(self.rect):

                    px = self.pair.x + self.pair.w / 2
                    py = self.pair.y + self.pair.h / 2 + 1

                    entity.change_pos((px, py))

    def draw(self, surface):

        Entity.draw(self, surface)

        # Do aura here

        # Bigger circle, smaller circle, gears/ wheels

def create_portal_pair(game, spawn1, spawn2, dimensions1, dimensions2, colour1, colour2):

    portal1, portal2 = PortalBlock(game, spawn1, dimensions1, colour1), PortalBlock(game, spawn2, dimensions2, colour2)
    portal1.pair, portal2.pair = portal2, portal1
    portal1.direction, portal2.direction = 0, 1

    return portal1, portal2