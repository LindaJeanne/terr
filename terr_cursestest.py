import arena
import actor
import display
import gameloop
import numpy as np


the_game_loop = gameloop.GameLoop(
    (40, 40),
    'GenUnitTestArena',
    'PopUnitTestArena',
    'TerrCursesDisplay',
    'UNIT_TEST_PLAYER')

while True:
    #TODO: Yes, ineficient. Yes, I will fix.
    for index, cell in np.ndenumerate(the_game_loop.the_arena.grid):
        the_game_loop.the_display.display_map_char(index[0], index[1], cell.get_display_tile())

    the_game_loop.tick()

the_game_loop.the_display.end()
