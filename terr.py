import numpy as np
import display as cd
import arena
import gamemgr
import turnmgr

gamemgr.setup(
    arena.UnitTestGridGenerator(),
    (40, 40))

the_arena = gamemgr.the_arena

gamemgr.new_player('PLAYER_DEFAULT', (5, 5))
gamemgr.new_creature('FIRE_ELEMENTAL', (7, 7))
gamemgr.new_creature('NORTH_GOING_ZAX', (31, 31))

cd.setup()

turnmgr.setup(gamemgr.turn_list)

while(True):
    for i, v in np.ndenumerate(the_arena.grid):
        cd.display_char(i[0], i[1], v.get_glyph(), 1)

    turnmgr.tick(gamemgr)

    cd.display_bottom_message(
        "Tick Counter is:" + str(turnmgr._counter))
