import numpy as np
import cursesdisplay as cd
import arena
import templ
import gameobjects as go

keypad_directions = dict((
    (55, arena.dir_nw),
    (56, arena.dir_north),
    (57, arena.dir_ne),
    (54, arena.dir_east),
    (51, arena.dir_se),
    (50, arena.dir_south),
    (49, arena.dir_sw),
    (52, arena.dir_west)))

templ.loadBlockXML('blocks.xml')
templ.loadCreatureXML('creatures.xml')
templ.loadItemXML('items.xml')

template_array = np.asanyarray(
    (('FLOOR_STONE', 'FLOOR_STONE', 'FLOOR_STONE',
        'FLOOR_STONE', 'FLOOR_STONE'),
        ('FLOOR_STONE', 'BLOCK_STONE', 'BLOCK_STONE',
            'BLOCK_STONE', 'FLOOR_STONE'),
        ('FLOOR_STONE', 'FLOOR_STONE', 'FLOOR_STONE',
            'FLOOR_STONE', 'FLOOR_STONE'),
        ('FLOOR_STONE', 'BLOCK_STONE', 'BLOCK_STONE',
            'BLOCK_STONE', 'FLOOR_STONE'),
        ('FLOOR_STONE', 'FLOOR_STONE', 'FLOOR_STONE',
            'FLOOR_STONE', 'FLOOR_STONE')))

game_arena = arena.Arena(template_array, templ.blockinfo)

player = go.Player()
game_arena.add_creature(player, (0, 0))
fire_elemental = go.Creature(templ.creatureinfo['FIRE_ELEMENTAL'])
game_arena.add_creature(fire_elemental, (4, 4))

display = cd.CursesDisplay()

#display.new_window('MAP_WINDOW', 30, 80, 0, 0)
#display.new_window('STATUS_LINE', 5, 80, 0, 31)

exit_now = False

while(not exit_now):
    for i, v in np.ndenumerate(game_arena.tile_array):
        display.display_char(i[0], i[1], v.get_display_char(), 1)

    keypressed = display.wait_char()
    #print("Key pressed:", keypressed)
    display_string = "Key pressed: " + str(keypressed)
    display.display_string(display_string, 1, 41)

    if keypressed == ord('q'):
        exit_now = True
    elif keypressed == 53:
        pass
    elif keypressed in range(49, 57):
        game_arena.step_creature(player, keypad_directions[keypressed])

display.wait_char()
display.end_curses()
