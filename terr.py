#import numpy as np
#import maplayer as ml
import cursesdisplay as cd
import arena
import blocks


width = 40
height = 40
depth = 10

#worldmap = ml.WorldMap((width, height))

#for i in range(1, 9):
#    worldmap += worldmap.gen_perlin(octaves=i)

#for i in range(1, 5):
#    worldmap.apply_automata()

#worldmap.display_rougelike_map()

blocks.load_all()
arena.create_arena((10, 10, 4))
display = cd.CursesDisplay()
arena.draw_level(0, display)
display.wait_char()
arena.draw_level(1, display)
display.wait_char()
arena.draw_level(2, display)
display.wait_char()
display.end_curses()
