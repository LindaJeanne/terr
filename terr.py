import numpy as np
import cursesdisplay as cd
import arena
import templ
import gameobjects as go


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
game_arena.tile_array[(0, 0)].add_creature(player)

display = cd.CursesDisplay()

for i, v in np.ndenumerate(game_arena.tile_array):
    display.display_char(i[0], i[1], v.get_display_char())

display.wait_char()
display.end_curses()
