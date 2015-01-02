import curses
import curseslib


_cur = None

_topmsg = None
_mapwin = None
_lowmsg = None

#curseslib.create_region(1, 0, 40, 3, 'TOPMSG')
#curseslib.create_region(1, 3, 40, 40, 'MAPWIN')
#curseslib.create_region(1, 43, 40, 3, 'LOWMSG')


def setup():

    # curseslib.setup()
    global _cur
    global _topmsg
    global _mapwin
    global _lowmsg

    _cur = curseslib.CursesSession()

    _topmsg = curseslib.CursesMessageWidget(_cur, 1, 0, 40, 2)
    _mapwin = curseslib.CursesCharmapWidget(_cur, 1, 3, 40, 40)
    _lowmsg = curseslib.CursesMessageWidget(_cur, 1, 44, 40, 3)


def display_top_message(msg):

    # curseslib.display_string(0, 1, msg, region='TOPMSG')
    global _topmsg
    _topmsg.display_message(msg)


def display_bottom_message(msg):

    #curseslib.display_string(0, 1, msg, region='LOWMSG')
    global _lowmsg
    _lowmsg.display_message(msg)


def display_map_char(x, y, char, color=1):

    global _mapwin
    _mapwin.draw_char(x, y, char, color)
    _cur.refresh


def display_char_array(the_array):
    global _mapwin
    _mapwin.draw_array(the_array)


def end_curses():
    #curseslib.end_curses()
    global _cur
    _cur.end()


def wait_char():
    #return curseslib.wait_keypress()
    global _cur
    return _cur.wait_keypress()
