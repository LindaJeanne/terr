import gamemgr
import numpy as np
import turnmgr


class GameObject(object):

    has_turn_list = list()

    def __init__(self, details):
        assert(details.token)
        assert(details.glyph)

        self.token = details.token
        self.glyph = details.glyph
        self.detail = details
        self.location = None

    @classmethod
    def is_valid_tile(cls, arena, location):

        if not arena.inside_arena(location):
            return False

        if not arena.blockArray[location].detail.template['is_walkable']:
            return False

        return True

    def add_to_arena(self, arena, location):
        pass


class Block(GameObject):

    def __init__(self, blockdetails):
        super().__init__(blockdetails)
        self.creature = None
        self.itemlist = list()

    def get_glyph(self):

        if self.creature:
            return self.creature.glyph
        elif self.itemlist:
            return self.itemlist[-1].glyph
        else:
            return self.glyph

    @classmethod
    def is_valid_tile(cls, arena, location):

        return arena.in_arena(location)


class Item(GameObject):

    def __init__(self, itemdetails):
        super().__init__(itemdetails)
        self.block = None

    def add_to_arena(self, arena, location):

        if not self.is_valid_tile(arena, location):
            return False

        if self in arena.itemset:
            return False

        arena.itemset.add(self)
        arena.blockArray[location].itemlist.append(self)
        self.location = location
        self.block = arena.blockArray[location]

        return True


class Creature(GameObject):

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
        gamemgr.turn_list.append(self)

        return True


class AiCreature(Creature, turnmgr.HasAiTurn):

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)


class NorthGoingZax(AiCreature):
    '''For unit testsing'''

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)

    def take_turn(self):
        new_loc = tuple(np.add(self.location, (0, -1)))
        result = gamemgr.teleport_creature(self, new_loc)
        if not result:
            result = gamemgr.teleport_creature(self, (25, 25))
            if not result:
                gamemgr.teleport_creature(self, (33, 33))
        return 10


class Player(Creature, turnmgr.HasPlayerTurn):

    def __init__(self, playerdetails):
        super().__init__(playerdetails)

    def add_to_arena(self, arena, location):
        if not super().add_to_arena(arena, location):
            return False

        arena.player = self

        return True


def create(template):

    class_name = template.template['objclass']
    the_class = globals()[class_name]
    return the_class(template)
