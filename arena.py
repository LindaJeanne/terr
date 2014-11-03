import numpy as np
import gameobj as go
import templ

dir_north = (0, -1)
dir_ne = (1, -1)
dir_east = (1, 0)
dir_se = (1, 1)
dir_south = (0, 1)
dir_sw = (-1, 1)
dir_west = (-1, 0)
dir_nw = (-1, -1)


class ArenaGenerator(object):

    def create(self, shape, blockinfo):

        new_arena = Arena(shape)

        for i, v in np.ndenumerate(new_arena.blockArray):
            new_arena.blockArray[i] = templ.blockinfo['FLOOR_STONE'].create()
            new_arena.blockArray[i].location = i

        return new_arena


class UnitTestArenaGenerator(ArenaGenerator):

    def create(self, shape, blockinfo):

        new_arena = super().create(shape, blockinfo)

        for i, v in np.ndenumerate(new_arena.blockArray):
            x_even = ((i[0] % 2) == 0)
            y_even = ((i[1] % 2) == 0)
            if x_even and y_even:
                new_block = templ.blockinfo['BLOCK_STONE'].create()
                new_block.location = i
                new_arena.blockArray[i] = new_block

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

        self.blockArray = np.empty(shape, go.Block)
        self.itemset = set()
        self.creatureset = set()

    def inside_arena(self, point):

        #if len(self._tileArray.shape) != len(point):
        if len(self.blockArray.shape) != len(point):
            # if 'point' has a different number of dimentions than the array,
            # then it's not "inside"
            return False

        #if any coord is less than zero, it's out of bounds
        for i in point:
            if i < 0:
                return False

        #check if any coord too large
        difference = np.subtract(self.blockArray.shape, point)
        for i in difference:
            if i <= 0:
                return False

        return True
