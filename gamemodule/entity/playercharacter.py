from gamemodule.entity.base import Entity
from gamemodule.utl.datastructure.gameoperation import *
from gamemodule.entity.enemy.enemy import Enemy
from gamemodule.entity.gas import GasEntity
from gamemodule.entity.enemy.infernoturret import InfernoTurret
import pygame

class PlayerCharacterEntity(Entity):

    def __meta_init__(self):

        self.keypress_d = self.keypress_d
        self.keypress_a = self.keypress_a
        self.keypress_w = self.keypress_w
        self.keypress_e = self.keypress_e
        self.keypress_q = self.keypress_q
        self.keypress_p = self.keypress_p

    def __init__(self, game, spawn, dimensions, colour):

        super().__init__(game, spawn, dimensions, colour)

        self.__meta_init__()

        self.jump_active = False
        self.jump_start = None
        self.fall_velocity = 0
        self.jump_velocity = 0
        self.jump_size = 100
        self.move_velocity = 3

        self.do_gravity = True
        self.do_jump = True

        self.double_jump = False

    @property
    def jumping(self):

        return False if self.jump_velocity == 10 else True

    @property
    def falling(self):

        return False if self.fall_velocity == 0 else True

    @property
    def grounded(self):

        if (self.y + self.h >= self.game.wh) or self.collidingbottom():

            return True

        else:

            return False # Check

    def colliding(self):

        colliding = None

        for entity in self.game.entities.list:

            if entity is not self:

                if entity.colliderect(self.rect):

                    colliding = entity

                    break

                if self.colliderect((entity.x, entity.y - self.h, entity.w, entity.h)):

                    colliding = entity

                    break

        return colliding

    def collidingtop(self):

        colliding = None
        tr = (self.x, self.y, self.w, 1)

        for entity in self.game.entities.list:

            if entity is not self:

                if entity.colliderect(tr):

                    colliding = entity
                    break

        return colliding

    def collidingbottom(self):

        colliding = None
        tr = (self.x, self.y + self.h, self.w, 1)

        for entity in self.game.entities.list:

            if entity is not self and isinstance(entity, (PlayerCharacterEntity, Enemy)):

                if entity.colliderect(tr):

                    colliding = entity
                    break

        return colliding

    def bottom(self):

        # Does not like looking at entities

        for entity in self.game.entities.list:

            if entity is not self and isinstance(entity, (PlayerCharacterEntity, Enemy)):

                if entity.colliderect(self.rect):

                    return entity.x, entity.y

        return self.x, self.game.wh - self.h

    def draw(self, surface, **kwargs):

        Entity.draw(self, surface, **kwargs)

    def keypress_q(self):

        if self.game.player.character is self:

            if self.game.player.staminagauge.gauge > 10:

                self.game.player.staminagauge -= 1

                if pygame.key.get_pressed()[pygame.K_p]:

                    self.tv = 5

                    self.tx -= 1
                    self.ty = 10

                @GameOperation.s(self.game, 1, xstep=-4, ystep=-0.5, colour=(255, 150, 255),
                                 spawn=(self.x, self.y + self.h/2), origin=self)
                def add_gas_entity3(*args, **kwargs):
                    self.game.entities.push(GasEntity(
                        *args, **kwargs
                    ))
                    self.game.operations.remove(add_gas_entity3)

                self.game.operations.push(add_gas_entity3)

                @GameOperation.s(self.game, 1, xstep=-4, ystep=0, colour=(255, 150, 255),
                                 spawn=(self.x, self.y + self.h/2), origin=self)
                def add_gas_entity(*args, **kwargs):
                    self.game.entities.push(GasEntity(
                        *args, **kwargs
                    ))
                    self.game.operations.remove(add_gas_entity)

                self.game.operations.push(add_gas_entity)

                @GameOperation.s(self.game, 1, xstep=-4, ystep=0.5,
                                 colour=(255, 150, 255), spawn=(self.x, self.y + self.h/2), origin=self)
                def add_gas_entity1(*args, **kwargs):
                    self.game.entities.push(GasEntity(
                        *args, **kwargs
                    ))
                    self.game.operations.remove(add_gas_entity1)

                self.game.operations.push(add_gas_entity1)

                return

    def keypress_e(self):

        if self.game.player.character is self:

            if self.game.player.staminagauge.gauge >= 10:

                self.game.player.staminagauge -= 1

                # Add propulsion

                if pygame.key.get_pressed()[pygame.K_p]:

                    self.tv = 5

                    self.tx += 1
                    self.ty = 10

                @GameOperation.s(self.game, 1, xstep=4, ystep=-0.5, colour=(255, 150, 255),
                                 spawn=(self.x + self.w, self.y + self.h/2), origin=self)
                def add_gas_entity3(*args, **kwargs):
                    self.game.entities.push(GasEntity(
                        *args, **kwargs
                    ))
                    self.game.operations.remove(add_gas_entity3)

                self.game.operations.push(add_gas_entity3)

                @GameOperation.s(self.game, 1, xstep=4, ystep=0, colour=(255, 150, 255),
                                 spawn=(self.x + self.w, self.y + self.h/2), origin=self)
                def add_gas_entity(*args, **kwargs):
                    self.game.entities.push(GasEntity(
                        *args, **kwargs
                    ))
                    self.game.operations.remove(add_gas_entity)

                self.game.operations.push(add_gas_entity)

                @GameOperation.s(self.game, 1, xstep=4, ystep=0.5, colour=(255, 150, 255),
                                 spawn=(self.x + self.w, self.y + self.h/2), origin=self)
                def add_gas_entity1(*args, **kwargs):
                    self.game.entities.push(GasEntity(
                        *args, **kwargs
                    ))
                    self.game.operations.remove(add_gas_entity1)

                self.game.operations.push(add_gas_entity1)

                return

    def keypress_d(self):

        if self.game.player.character is self and self.game.player.staminagauge.gauge >= 0.3:

            self.x += self.move_velocity
            self.game.player.staminagauge -= 0.3

    def keypress_a(self):

        if self.game.player.character is self and self.game.player.staminagauge.gauge >= 0.3:

            self.x -= self.move_velocity
            self.game.player.staminagauge -= 0.3

    def keypress_w(self):

        if self.game.player.character is self:

            if self.game.player.staminagauge.gauge >= 0.5:

                self.game.player.staminagauge -= 0.5

                if self.grounded:

                    self.jump_start = self.y
                    self.jump_active = True
                    self.double_jump = True

    def move(self):

        # Go up

        if self.tx > 0:
            self.x -= self.tv
            self.tx -= 1
        elif self.tx < 0:
            self.x += self.tv
            self.tx += 1

        if self.ty > 0:
            self.y -= self.tv
            self.ty -= 1
        elif self.ty < 0:
            self.y += self.tv
            self.ty += 1

        if self.jump_start is not None:

            self.jump()

        else:

            self.gravity()

    def jump(self):

        if self.do_jump:

            self.fall_velocity = 0

            if self.y >= self.jump_start - self.jump_size:

                self.game.log.push(f'Began jumping *{self} with expected peak @ (x:{self.x}, y:{self.jump_size})')

                self.y -= int(self.jump_velocity * 3 - self.jump_velocity)
                self.jump_velocity += 1

            else:

                self.jump_velocity = 0
                self.jump_start = None
                self.jump_active = False

    def gravity(self):

        if self.do_gravity and self.game.get_condition('gravity') == True:

            self.jump_velocity = 0

            if not self.grounded:

                self.y += int(self.fall_velocity / 2)
                self.fall_velocity += 1

            else:

                self.fall_velocity = 0

                if e := self.collidingbottom():

                    self.y = e.y - self.h

                elif self.y + self.h >= self.game.wh:

                    self.y = self.game.wh - self.h

                else:

                    self.y = self.game.wh - self.h

    def frame(self):

        for entity in self.game.entities.list:

            if entity is not self:

                if type(entity) in (GasEntity, ):

                    if entity.colliderect(self.rect) and not entity.origin is self:

                        entity.die = True

                        if self.game.player.character is self:

                            self.game.player.healthgauge -= .1 - (0.1 * entity.deviation) / 1000

    def keypress_p(self):

        if self.game.player.character is self:

            keys = pygame.key.get_pressed()

            if keys[pygame.K_q] and keys[pygame.K_e] and self.game.player.staminagauge.gauge > 30:

                self.game.player.staminagauge -= 5

                self.jump_velocity = 1
                self.jump_start = self.y