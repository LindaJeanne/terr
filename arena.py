import numpy as np

dir_north = (0, -1)
dir_ne = (1, -1)
dir_east = (1, 0)
dir_se = (1, 1)
dir_south = (0, 1)
dir_sw = (-1, 1)
dir_west = (-1, 0)
dir_nw = (-1, -1)


class ArenaTile(object):

    def __init__(self, coords, blockinfo):
        self.creature = None
        self.itemlist = list()
        self.block = blockinfo.template
        self._coords = coords

    def get_display_char(self):

        if self.creature:
            return self.creature.detail.glyph
        elif self.itemlist:
            return self.itemlist[-1].detail.glyph
        else:
            return self.block['glyph']


class ArenaGenerator(object):

    def create(self, shape, blockinfo):

        new_arena = Arena(shape)
        for i, v in np.ndenumerate(new_arena._tileArray):
            new_arena._tileArray[i] = ArenaTile(i, blockinfo['FLOOR_STONE'])
        return new_arena


class UnitTestArenaGenerator(ArenaGenerator):

    def create(self, shape, blockinfo):

        new_arena = super().create(shape, blockinfo)

        for i, v in np.ndenumerate(new_arena._tileArray):
            x_even = ((i[0] % 2) == 0)
            y_even = ((i[1] % 2) == 0)
            if x_even and y_even:
                new_arena._tileArray[i] = ArenaTile(
                    i, blockinfo['BLOCK_STONE'])

        return new_arena


class Arena(object):

    dir_north = (0, -1)
    dir_ne = (1, -1)
    dir_east = (1, 0)
    dir_se = (1, 1)
    dir_south = (0, 1)
    dir_sw = (-1, 1)
    dir_west = (-1, 0)
    dir_nw = (-1, -1)

    def __init__(self, shape):
        '''Use and ArenaGenerator rather than instantizing directly'''
        self._tileArray = np.empty(shape, ArenaTile)
        self._itemSet = set()
        self._creatureSet = set()

    def step_creature(self, creature, direction):

        assert(creature in self._creatureSet)

        old_loc = creature.tile._coords
        new_loc = tuple(np.add(old_loc, direction))

        if not self.inside_arena(new_loc):
            return False

        if not self._tileArray[new_loc].block['is_walkable']:
            return False

        if self._tileArray[new_loc].creature:
            return False

        creature.tile.creature = None
        creature.tile = self._tileArray[new_loc]
        creature.tile.creature = creature

        return True

    def inside_arena(self, point):

        if len(self._tileArray.shape) != len(point):
            # if 'point' has a different number of dimentions than the array,
            # then it's not "inside"
            return False

        difference = np.subtract(self._tileArray.shape, point)
        #If any of the values in point are greater than the corresponding
        #value of the arena's shape, then at least one of the element-wise
        #difference elements will be negative.

        for i in difference:
            if i <= 0:
                return False

        return True
