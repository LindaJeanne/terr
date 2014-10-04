import curses
import numpy as np


def display_array_mask(the_array, the_screen):

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    for i, j in np.ndenumerate(the_array):
        print(i, j)
        if j > 0:
            #note: curses wants the coordinates backwards y,x
            the_screen.addch(i[1], i[0], "#", curses.color_pair(2))
        elif j == 0:
            the_screen.addch(i[1], i[0], "=", curses.color_pair(2))
        else:
            the_screen.addch(i[1], i[0], "~", curses.color_pair(1))

    the_screen.refresh()
    the_screen.getch()
