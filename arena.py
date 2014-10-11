import numpy as np
import blocks
import cursesdisplay as cd

arena = []


class ArenaTile():

    def __init__(self, block_token, floor_token, location):
        self.block = blocks.blocks[block_token]
        self.floor = blocks.floor_tiles[floor_token]
        self.location = location

    def char(self):
        if (self.block.token == 'BLOCK_AIR'):
            return self.floor.char
        else:
            return self.block.char


def create_arena(shape):
    global arena

    arena = np.empty(shape, ArenaTile)

    for i, v in np.ndenumerate(arena):
        arena[i] = ArenaTile('BLOCK_AIR', 'FLOOR_AIR', i)
    for index in np.ndindex(shape[0], shape[1], 2):
        arena[index] = ArenaTile('BLOCK_AIR', 'FLOOR_STONE', index)
    for index in np.ndindex(shape[0], shape[1], 1):
        arena[index] = ArenaTile('BLOCK_STONE', 'FLOOR_STONE', index)
    for i in range(5, 8):
        arena[i, 3, 1] = ArenaTile('BLOCK_STONE', 'FLOOR_STONE', (i, 3, 1))


def draw_level(z, display, screen="SCREEN"):
    for i, v in np.ndenumerate(arena[:, :, z]):
        display.display_char(i[0], i[1], v.char())

    display.refresh()
