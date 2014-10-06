import numpy as np
import maplayer as ml
import curses_display as cd


my_screen = cd.start_curses()

width = 40
height = 40

height_map = ml.MapLayer((width, height))

for i in range(1, 9):
    height_map += height_map.gen_perlin(octaves=i)

for i in range(1, 5):
    height_map.apply_automata()

cd.display_array_mask(height_map, my_screen)

print(np.array_str(height_map))

cd.end_curses(my_screen)
height_map.display()
