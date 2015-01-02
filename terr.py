import numpy as np
import display as cd
import turnmgr
import gridgen
import util
import arena
import creature
import player
import item

global the_arena
utgg = gridgen.UnitTestGridGenerator()
the_arena = arena.Arena(utgg.create((40, 40)))

the_player = util.create(player, 'PLAYER_DEFAULT')
the_arena.player = the_player
the_arena.place_creature(the_player, (5, 5))

the_arena.place_creature(util.create(creature, 'FIRE_ELEMENTAL'), (7, 7))
the_arena.place_creature(util.create(creature, 'NORTH_GOING_ZAX'), (31, 31))
the_arena.place_creature(util.create(creature, 'PICKUP_DROPPER'), (25, 25))
the_arena.place_item(util.create(item, 'APPLE'), (11, 11))
the_arena.place_item(util.create(item, 'APPLE'), (25, 25))
the_arena.place_item(util.create(item, 'PICKAXE'), (31, 29))

turnmgr.turn_list = list(the_arena.creatureset)

cd.setup()

turnmgr.setup()

while(True):
    for i, v in np.ndenumerate(the_arena.grid):

        cd.display_map_char(i[0], i[1], v.get_glyph(), 1)
        # cd.display_char(i[0], i[1], v.get_glyph(), 1)

    turnmgr.tick()

    cd.display_bottom_message(
        "Tick Counter is:" + str(turnmgr._counter))
