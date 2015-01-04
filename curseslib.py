import curses
import numpy as np


# _scr = None
# _regions = {}


class CursesSession(object):

    # color pairs
    COLOR_WHITE_ON_BLACK = 1
    COLOR_BLUE_ON_BLACK = 2
    COLOR_GREEN_ON_BLACK = 3
    COLOR_RED_ON_BLACK = 4
    COLOR_YELLOW_ON_BLACK = 5

    def __init__(self):
        self._scr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self._scr.keypad(True)

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)


    def display_char(self, x, y, the_char, color=1):
        self._scr.addch(y, x, the_char, curses.color_pair(color))


    def display_string(self, x, y, the_str):
        if the_str:
            self._scr.addstr(y, x, the_str)

    def wait_keypress(self):
        return self._scr.getch()

    def refresh(self):
        self._scr.refresh()

    def end(self):
        self._scr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


class CursesWidget(object):

    def __init__(self, csess, x, y, width, height):
        self.session = csess
        self.x = x
        self.y = y
        self.width = width
        self.height = height


    def display_string(self, x, y, the_str):
        self.session.display_string(x + self.x, y + self.y, the_str)

    def display_char(self, x, y, the_char, color=1):
        self.session.display_char(
            x + self.x,
            y + self.y,
            the_char,
            color)

    def clear_widget(self):
        for i in self.x:
            for j in self.y:
                display_char(i, j, ' ')

        self.session.refresh()


class CursesMessageWidget(CursesWidget):

    def display_message(self, the_str):
        #self.clear_widget()
        self.display_string(0, 0, the_str)
        self.session.refresh()


class CursesCharmapWidget(CursesWidget):

    def draw_array(self, the_char_array):

        for i, v in np.ndenumerate(the_char_array):
            self.display_char(i[0], i[1], v)
        self.session.refresh()

    def draw_char(self, x, y, the_char, color=1):

        self.display_char(x, y, the_char, color)
        self.session.refresh()

