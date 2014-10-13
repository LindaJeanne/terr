import numpy as np
import blocks
import collections as cn

stepDirection = cn.namedtuple('stepDirection', 'South East')


class ArenaTile(object):

    def __init__(
            self,
            block_token,
            floor_token,
            myarena,
            location):
        self.block = blocks.blocks[block_token]
        self.floor = blocks.floor_tiles[floor_token]
        self.myarena = myarena
        self.location = location
        self.items = list()
        self.creatures = list()

    def char(self):

        if self is self.myarena.index[self.myarena.player.location]:
            return ord('@')
        elif self.creatures:
            return self.creatures[:-1].char
        elif self.items:
            return self.items[:-1].char
        elif self.block.token == 'BLOCK_AIR':
            return self.floor.char
        else:
            return self.block.char


class Arena(object):

    def __init__(self, shape, generator):
        self.index = np.ndarray(shape, ArenaTile)
        self.shape = shape
        self.player = None
        generator.generate(self)

    def draw(self, curses_display, slice):

        for i, v in np.ndenumerate(slice):
            #print(i[0], i[1], v.char())
            curses_display.display_char(i[0], i[1], v.char())

    def set_player(self, sapient):
        self.player = sapient


class Overworld(Arena):

    def __init__(self, x, y, z, overworld_generator):
        super().__init__((x, y, z), overworld_generator)

    def draw(self, curses_display, z):
        super().draw(curses_display, self.index[:, :, z])


class ArenaGenerator(object):

    def generate(self, thearena):

            for i, v in np.ndenumerate(thearena.index):
                thearena.index[i] = ArenaTile(
                    'BLOCK_AIR', 'FLOOR_AIR', thearena, i)
            for j in np.ndindex(thearena.shape[0], thearena.shape[1], 2):
                thearena.index[j] = ArenaTile(
                    'BLOCK_AIR', 'FLOOR_STONE', thearena, j)
            for j in np.ndindex(thearena.shape[0], thearena.shape[1], 1):
                thearena.index[j] = ArenaTile(
                    'BLOCK_STONE', 'FLOOR_STONE', thearena, j)
            for i in range(5, 8):
                thearena.index[i, 3, 1] = ArenaTile(
                    'BLOCK_STONE', 'FLOOR_STONE', thearena, (i, 3, 1))
