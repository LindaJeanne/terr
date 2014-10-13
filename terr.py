#import numpy as np
#import maplayer as ml
import cursesdisplay as cd
import arena
import blocks
import gameobjects as go


width = 40
height = 40
depth = 10

blocks.load_all()
arena_generator = arena.ArenaGenerator()
thearena = arena.Overworld(width, height, depth, arena_generator)

display = cd.CursesDisplay()
player = go.Player((3, 3, 1))
thearena.set_player(player)

print(thearena.index[player.location].char())
thearena.draw(display, 1)

display.wait_char()

display.end_curses()


#arena.draw(display, 1)

#display.wait_char()
#worldmap = ml.WorldMap((width, height))

#for i in range(1, 9):
#    worldmap += worldmap.gen_perlin(octaves=i)

#for i in range(1, 5):
#    worldmap.apply_automata()

#worldmap.display_rougelike_map()
