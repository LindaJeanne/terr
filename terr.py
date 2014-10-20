import numpy as np
import display as cd
import arena
import templ

keypad_directions = dict((
    (55, arena.dir_nw),
    (56, arena.dir_north),
    (57, arena.dir_ne),
    (54, arena.dir_east),
    (51, arena.dir_se),
    (50, arena.dir_south),
    (49, arena.dir_sw),
    (52, arena.dir_west)))

templ.load_templates()
generator = arena.UnitTestArenaGenerator()
arena.setup(generator, (20, 20))
player = arena.create_player((5, 5))
fire_elemental = arena.create_creature(
    templ.creatureinfo['FIRE_ELEMENTAL'],
    (7, 7))

cd.setup()

#display.new_window('MAP_WINDOW', 30, 80, 0, 0)
#display.new_window('STATUS_LINE', 5, 80, 0, 31)

exit_now = False

while(not exit_now):
    for i, v in np.ndenumerate(arena._tileArray):
        cd.display_char(i[0], i[1], v.get_display_char(), 1)

    keypressed = cd.wait_char()
    display_string = "Key pressed: " + str(keypressed)
    cd.display_string(display_string, 1, 41)

    if keypressed == ord('q'):
        exit_now = True
    elif keypressed == 53:
        pass
    elif keypressed in range(49, 57):
        arena.step_creature(
            player, keypad_directions[keypressed])

cd.end_curses()
