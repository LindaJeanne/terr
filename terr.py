import numpy as np
import curses
import maplayer as ml
import curses_display as cd


def start_curses():
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    curses.start_color()
    return screen


def end_curses(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()


my_screen = start_curses()

width = 40
height = 40

height_map = ml.MapLayer((width, height))

for i in range(1, 9):
    height_map += height_map.gen_perlin(octaves=i)

for i in range(1, 5):
    height_map.apply_automata()

cd.display_array_mask(height_map, my_screen)

print(np.array_str(height_map))

end_curses(my_screen)
height_map.display()
