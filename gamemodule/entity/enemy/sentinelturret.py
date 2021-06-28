from gamemodule.entity.base import Entity
from gamemodule.utl.datastructure.gameoperation import GameOperation
from gamemodule.entity.gas import GasEntity
from gamemodule.entity.enemy.enemy import Enemy
from gamemodule.utl.util import get_travel_vector


class SentinelTurret(Entity, Enemy):

    def __init__(self, game, spawn, dimensions, colour):
        Entity.__init__(self, game, spawn, dimensions, colour)
        Enemy.__init__(self)

    def frame(self):

        xstep, ystep = get_travel_vector(self.game.player.character.pos, self.pos)

        """

        @GameOperation.s(self.game, 1, xstep=4, ystep=ystep+0.25, colour=(255, 50, 0),
                         spawn=(self.x + self.w, self.y + self.h / 2), life=2, origin=self)
        def add_gas_entity0(*args, **kwargs):
            self.game.entities.push(GasEntity(
                *args, **kwargs
            ))
            self.game.operations.remove(add_gas_entity0)

        self.game.operations.push(add_gas_entity0)
        
        """

        @GameOperation.s(self.game, 1, xstep=4, ystep=ystep, colour=(255, 50, 0),
                         spawn=(self.x + self.w, self.y + self.h / 2), life=2, origin=self)
        def add_gas_entity(*args, **kwargs):
            self.game.entities.push(GasEntity(
                *args, **kwargs
            ))
            self.game.operations.remove(add_gas_entity)

        self.game.operations.push(add_gas_entity)

        """
        
        @GameOperation.s(self.game, 1, xstep=4, ystep=ystep-0.25, colour=(255, 50, 0),
                         spawn=(self.x + self.w, self.y + self.h / 2), life=2, origin=self)
        def add_gas_entity1(*args, **kwargs):
            self.game.entities.push(GasEntity(
                *args, **kwargs
            ))
            self.game.operations.remove(add_gas_entity1)

        self.game.operations.push(add_gas_entity1)

        # Do other side

        @GameOperation.s(self.game, 1, xstep=-4, ystep=ystep + 0.25, colour=(255, 50, 0),
                         spawn=(self.x, self.y + self.h / 2), life=2, origin=self)
        def add_gas_entity0_(*args, **kwargs):
            self.game.entities.push(GasEntity(
                *args, **kwargs
            ))
            self.game.operations.remove(add_gas_entity0_)

        self.game.operations.push(add_gas_entity0_)
        
        """

        @GameOperation.s(self.game, 1, xstep=-4, ystep=ystep, colour=(255, 50, 0),
                         spawn=(self.x, self.y + self.h / 2), life=2, origin=self)
        def add_gas_entity_(*args, **kwargs):
            self.game.entities.push(GasEntity(
                *args, **kwargs
            ))
            self.game.operations.remove(add_gas_entity_)

        self.game.operations.push(add_gas_entity_)

        """

        @GameOperation.s(self.game, 1, xstep=-4, ystep=ystep - 0.25, colour=(255, 50, 0),
                         spawn=(self.x, self.y + self.h / 2), life=2, origin=self)
        def add_gas_entity1_(*args, **kwargs):
            self.game.entities.push(GasEntity(
                *args, **kwargs
            ))
            self.game.operations.remove(add_gas_entity1_)

        self.game.operations.push(add_gas_entity1_)
        """