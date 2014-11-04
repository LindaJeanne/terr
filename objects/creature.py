from . import gameobj
import numpy as np


class Creature(gameobj.GameObject):

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)
        self.block = None

    @classmethod
    def is_valid_tile(cls, arena, location):
        if not super().is_valid_tile(arena, location):
            return False

        if arena.blockArray[location].creature:
            return False

        return True

    def add_to_arena(self, arena, location):

        if not self.is_valid_tile(arena, location):
            return False

        if self in arena.creatureset:
            return False

        arena.creatureset.add(self)
        arena.blockArray[location].creature = self
        self.block = arena.blockArray[location]
        self.location = location
        self.arena = arena

        return True

    def teleport(self, location):

        if not self.arena:
            return False

        if not self.is_valid_tile(self.arena, location):
            return False

        if self not in self.arena.creatureset:
            return False

        self.block.creature = None
        self.block = self.arena.blockArray[location]
        self.location = location
        self.block.creature = self

        return True


class AiCreature(Creature, gameobj.HasAiTurn):

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)


class NorthGoingZax(AiCreature):
    '''For unit testsing'''

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)

    def take_turn(self):
        new_loc = tuple(np.add(self.location, (0, -1)))
        if not self.teleport(new_loc):
            if not self.teleport((25, 25)):
                self.teleport((33, 33))

        return 10


def create(template):

    assert('objclass' in template.template)
    class_name = template.template['objclass']

    assert(class_name in globals())
    the_class = globals()[class_name]

    return the_class(template)
