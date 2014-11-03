import gamemgr
import numpy as np
import turnmgr


class GameObject(object):

    has_turn_list = list()

    def __init__(self, details, arena=None):
        assert(details.token)
        assert(details.glyph)

        self.token = details.token
        self.glyph = details.glyph
        self.detail = details
        self.location = None
        self.arena = arena


class Block(GameObject):

    def __init__(self, blockdetails, arena=None):
        super().__init__(blockdetails, arena)
        self.creature = None
        self.itemlist = list()

    def get_glyph(self):

        if self.creature:
            return self.creature.glyph
        elif self.itemlist:
            return self.itemlist[-1].glyph
        else:
            return self.glyph


class Item(GameObject):

    def __init__(self, itemdetails, arena=None):
        super().__init__(itemdetails, arena)
        self.block = None


class Creature(GameObject):

    def __init__(self, creaturedetails, arena=None):
        super().__init__(creaturedetails, arena)
        self.block = None


class AiCreature(Creature, turnmgr.HasAiTurn):

    def __init__(self, creaturedetails, arena=None):
        super().__init__(creaturedetails, arena)


class NorthGoingZax(AiCreature):
    '''For unit testsing'''

    def __init__(self, creaturedetails, arena=None):
        super().__init__(creaturedetails, arena)

    def take_turn(self):
        new_loc = tuple(np.add(self.location, (0, -1)))
        result = gamemgr.teleport_creature(self, new_loc)
        if not result:
            result = gamemgr.teleport_creature(self, (25, 25))
            if not result:
                gamemgr.teleport_creature(self, (33, 33))
        return 10


class Player(Creature, turnmgr.HasPlayerTurn):

    def __init__(self, playerdetails, arena=None):
        super(Creature, self).__init__(playerdetails, arena)
