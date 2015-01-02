import curses
import curseslib


curseslib.create_region(1, 0, 40, 3, 'TOPMSG')
curseslib.create_region(1, 3, 40, 40, 'MAPWIN')
curseslib.create_region(1, 43, 40, 3, 'LOWMSG')


def display_top_message(msg):

    curseslib.display_string(0, 1, msg, region='TOPMSG')


def display_bottom_message(msg):

    curseslib.display_string(0, 1, msg, region='LOWMSG')


def setup():

    curseslib.setup()


def display_map_char(x, y, char, color=1):

    curseslib.display_char(x, y, char, color, 'MAPWIN')


def end_curses():
    curseslib.end_curses()


def wait_char():
    return curseslib.wait_keypress()
