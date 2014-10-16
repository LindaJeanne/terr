#import numpy as np


class ArenaTile(object):

    def __init__(self, x, y, blockinfo):
        self.creature = False
        self.itemlist = list()
        self.block = blockinfo
        self.x = x
        self.y = y

    def add_creature(self, creature):
        if self.creature:
            return False  # remove current creature before adding new one.
        else:
            self.creature = creature

        assert(creature.detail.token)
        assert(creature.detail.char)

        return True

    def rmv_creature(self):
        if self.creature:
            self.creature = False
            return True
        else:
            return False  # There is no creature to remove

    def add_item(self, item):
        if item in self.itemlist:
            return False  # we don't need to add it, it's there already
        else:
            assert(item.detail.token)
            assert(item.detail.char)
            self.itemlist.append(item)
            return True

    def rmv_item(self, item):
        if item in self.itemlist:
            self.itemlist.remove(item)
            return True
        else:
            return False

    def get_display_char(self):

        if self.creature:
            return self.creature.detail.char
        elif self.itemlist:
            return self.itemlist[-1].detail.char
        else:
            return self.block.char


class Arena(object):
    pass
