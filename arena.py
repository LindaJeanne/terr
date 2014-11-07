import numpy as np
import templates.templ as templ

dir_north = (0, -1)
dir_ne = (1, -1)
dir_east = (1, 0)
dir_se = (1, 1)
dir_south = (0, 1)
dir_sw = (-1, 1)
dir_west = (-1, 0)
dir_nw = (-1, -1)


class Block(object):

    def __init__(self, blockdetails):
        assert(blockdetails.token)
        assert(blockdetails.glyph)

        self.token = blockdetails.token
        self.glyph = blockdetails.glyph
        self.detail = blockdetails
        self.location = None
        self.creature = None
        self.itemlist = list()

    def get_glyph(self):

        if self.creature:
            return self.creature.glyph
        elif self.itemlist:
            return self.itemlist[-1].glyph
        else:
            return self.glyph


def create_block(token, arena, location):

    assert(token in templ.blockinfo)
    assert(arena.in_bounds(location))

    new_block = Block(templ.blockinfo[token])
    new_block.location = location
    return new_block


class ArenaGenerator(object):

    def create(self, shape, blockinfo):

        new_arena = Arena(shape)

        for i, v in np.ndenumerate(new_arena.blockArray):
            new_arena.blockArray[i] = create_block('FLOOR_STONE', new_arena, i)
            new_arena.blockArray[i].location = i

        return new_arena


class UnitTestArenaGenerator(ArenaGenerator):

    def create(self, shape, blockinfo):

        new_arena = super().create(shape, blockinfo)

        for i, v in np.ndenumerate(new_arena.blockArray):
            x_even = ((i[0] % 2) == 0)
            y_even = ((i[1] % 2) == 0)
            if x_even and y_even:
                new_arena.blockArray[i] = create_block(
                    'BLOCK_STONE', new_arena, i)
                new_arena.blockArray[i].location = i

        return new_arena


class Arena(object):

    def __init__(self, shape):
        '''Use and ArenaGenerator rather than instantizing directly'''

        self.blockArray = np.empty(shape, Block)
        self.itemset = set()
        self.creatureset = set()

    def place_creature(self, creature, location):

        assert(self.in_bounds(location))
        assert(not self.blockArray[location].creature)
        if not self.blockArray[location].detail.template['is_walkable']:
            raise Exception("non walkable block error")

        if creature in self.creatureset:
            creature.node.creature = None
        else:
            self.creatureset.add(creature)

        creature.node = self.blockArray[location]
        creature.node.creature = creature
        creature.arena = self

    def remove_creature(self, creature):

        if creature not in self.creatureset:
            return False

        creature.node.creature = None
        creature.node = None
        self.creatureset.remove(creature)
        creature.arena = None
        return True

    def place_item(self, item, location):

        assert(self.in_bounds(location))
        if not self.blockArray[location].detail.template['is_walkable']:
            raise Exception("Trying to place item on non walkable tile")

        if item in self.itemset:
            item.contain.itemlist.remove(item)
        else:
            self.itemset.add(item)

        item.contain = self.blockArray[location]
        item.contain.itemlist.append(item)
        item.arena = self

    def remove_item(self, item):

        if item not in self.itemset:
            return False

        item.contain.itemlist.remove(item)
        item.contain = None
        item.arena = None
        self.itemset.remove(item)

    def in_bounds(self, point):

        # if len(self._tileArray.shape) != len(point):
        if len(self.blockArray.shape) != len(point):
            return False

        # if any coord is less than zero, it's out of bounds
        for i in point:
            if i < 0:
                return False

        # check if any coord too large
        difference = np.subtract(self.blockArray.shape, point)
        for i in difference:
            if i <= 0:
                return False

        return True
