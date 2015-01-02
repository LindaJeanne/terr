import curses
import curseslib

#color pairs
# COLOR_WHITE_ON_BLACK = 1
# COLOR_BLUE_ON_BLACK = 2
# COLOR_GREEN_ON_BLACK = 3
# COLOR_RED_ON_BLACK = 4
# COLOR_YELLOW_ON_BLACK = 5

# _screenlist = {}

#screen regions

curseslib.create_region(1, 0, 40, 3, 'TOPMSG')
curseslib.create_region(1, 3, 40, 40, 'MAPWIN')
curseslib.create_region(1, 43, 40, 3, 'LOWMSG')
curseslib.create_region(45, 5, 20, 40, 'RIGHTBAR')

# SCREEN_REGION_TOPMSG = (1, 0)
# SCREEN_REGION_MAPWIN = (1, 3)
# SCREEN_REGION_LOWMSG = (1, 43)
# SCREEN_REGION_RIGHTBAR = (45, 5)


def display_top_message(msg):

    curseslib.display_string(0, 1, msg, region='TOPMSG')
#    display_string(
#        msg,
#        SCREEN_REGION_TOPMSG[0],
#        SCREEN_REGION_TOPMSG[1])

#    refresh()


def display_bottom_message(msg):

    curseslib.display_string(0, 1, msg, region='LOWMSG')

#    display_string(
#        msg,
#        SCREEN_REGION_LOWMSG[0],
#        SCREEN_REGION_LOWMSG[1])

#    refresh()


def setup():

    curseslib.setup()

#    global _screen_list
#
#    _screenlist['SCREEN'] = curses.initscr()
#    curses.start_color()
#    curses.noecho()
#    curses.cbreak()
#    _screenlist['SCREEN'].keypad(True)

#    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
#    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
#    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
#    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
#    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)


#def new_window(screenToken, lines, cols, upper_left_x, upper_left_y):
#    global _screenlist
#    _screenlist[screenToken] = curses.newwin(
#        lines, cols, upper_left_y, upper_left_x)



def display_map_char(x, y, char, color=1):

    curseslib.display_char(x, y, char, color, 'MAPWIN')
#    refresh()

#def display_char(
#        x, y, char,
#        color=1,
#        screenToken='SCREEN',
#        region=None):
#    '''displays a character at a given location on the given screen.
#
#    'color' is a number representing a curses color pair; those
#    initialized in this class are given as class-level constants'''
#
#    global _screenlist
#
#    global SCREEN_REGION_MAPWIN
#
#    if not region:
#        region = SCREEN_REGION_MAPWIN
#
#    aj_x = x + region[0]
#    aj_y = y + region[1]
#
#    _screenlist[screenToken].addch(aj_y, aj_x, char, curses.color_pair(color))


#def display_string(
#        string, x, y,
#        color=1, screenToken='SCREEN',
#        region=None):
#    global _screenlist
#
#    global SCREEN_REGION_TOPMSG
#
#    if not region:
#        region = SCREEN_REGION_TOPMSG
#
#    adj_x = x + region[0]
#    adj_y = y + region[1]
#
#    _screenlist[screenToken].addstr(adj_y, adj_x, string)


#def end_screen(screenToken):
#    '''close out the screen with the given token.
#
#    Other screens will still be active, and curses will not
#    be shut down. In order to shut down curses, call
#    end_curses()'''
#
#    global _screenlist
#    _screenlist[screenToken].screen.keypad(False)


def end_curses():
    curseslib.end_curses()
#    '''close all curses screens and return terminal to normal'''
#    global _screenlist
#
#    for screenToken in _screenlist:
#        _screenlist[screenToken].keypad(False)
#
#    curses.nocbreak()
#    curses.echo()
#    curses.endwin()


#def refresh(screenToken='SCREEN'):
#    '''call this to redraw the screen and see your updates'''
#
#    global _screenlist
#    _screenlist[screenToken].refresh()


#def wait_char(screenToken='SCREEN'):
#    '''wait until a key is pressed, and get the key'''
#
#    global _screenlist
#    return _screenlist[screenToken].getch()

def wait_char():
    return curseslib.wait_keypress()
