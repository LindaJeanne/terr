import numpy as np
import display as cd
import arena
import templ
import gamemgr

keypad_directions = dict((
    (55, arena.dir_nw),
    (56, arena.dir_north),
    (57, arena.dir_ne),
    (54, arena.dir_east),
    (51, arena.dir_se),
    (50, arena.dir_south),
    (49, arena.dir_sw),
    (52, arena.dir_west)))

gamemgr.setup(
    arena.UnitTestArenaGenerator(),
    (40, 40))

the_arena = gamemgr.the_arena

player = the_arena.create_player(
    templ.playerclassinfo['PLAYER_DEFAULT'],
    (5, 5))

fire_elemental = templ.creatureinfo['FIRE_ELEMENTAL'].create()
gamemgr.add_creature(fire_elemental, (7, 7))

cd.setup()

exit_now = False

while(not exit_now):
    for i, v in np.ndenumerate(the_arena._tileArray):
        cd.display_char(i[0], i[1], v.get_display_char(), 1)

    keypressed = cd.wait_char()
    display_string = "Key pressed: " + str(keypressed)
    cd.display_string(display_string, 1, 41)

    if keypressed == ord('q'):
        exit_now = True
    elif keypressed == 53:
        pass
    elif keypressed in range(49, 57):
        the_arena.step_creature(
            player, keypad_directions[keypressed])

cd.end_curses()
