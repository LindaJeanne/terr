import curses


_scr = None
_regions = {}


# color pairs
COLOR_WHITE_ON_BLACK = 1
COLOR_BLUE_ON_BLACK = 2
COLOR_GREEN_ON_BLACK = 3
COLOR_RED_ON_BLACK = 4
COLOR_YELLOW_ON_BLACK = 5


def setup():

    global _scr

    _scr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    _scr.keypad(True)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    global _regions
    _regions['NONE'] = (0, 0, 0, 0)


def create_region(x, y, width, height, scr_token):

    _regions[scr_token] = (x, y, width, height)


def end_curses():

    global _scr

    _scr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def display_char(x, y, char, color=1, region='NONE'):

    global _scr
    global _regions

    _scr.addch(
        y + _regions[region][1],
        x + _regions[region][0],
        char,
        curses.color_pair(color))

    refresh()


def display_string(x, y, str, region='NONE'):

    global _scr
    global _regions

    _scr.addstr(y + _regions[region][1], x + _regions[region][0], str)

    refresh()


def wait_keypress():
    global _scr
    return _scr.getch()


def end_curses():

    global _scr
    _scr.keypad(False)

    curses.nocbreak()
    curses.echo()
    curses.endwin()

def refresh():
    global _scr
    _scr.refresh()


#class CursesWidget(object):
#
#    def __init__(self, x, y, width, height):
#        global _regions
#        self.rect = (x, y, width, height)
#        _regions[self] = self.rect
#
#
#class CursesAsciiWidget(object):
#
#    def display_char(self, x, y, char, color=1):
#
#        global _regions
#        display_char(x, y, char, color, _regions[self])
#        curses.refresh()
#
#
#class CursesMsgWidget(object):
#
#    def display_string(self, str):
#
#        global _regions
#        display_string(1, 1, str, _regions[self])
#        curses.refresh()
