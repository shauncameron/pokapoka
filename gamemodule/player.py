from gamemodule.entity.hotbar import Hotbar
from gamemodule.utl.datastructure.stack import Stack

class Player:

    def s(self, entity, func):

        def donothing(): pass

        return func if self.character == entity else donothing

        return self.character == entity

    def __init__(self, game, healthgauge, staminagauge):

        self.hotbar = Hotbar(10, game, (25, 25), (50, 50), (200, 200, 200))
        self.operations = Stack()
        self.character = None
        self.healthgauge, self.staminagauge = healthgauge, staminagauge