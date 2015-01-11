import curses
import curseslib


class TerrDisplay(object):

    def __init__(self):
        pass

    def display_top_message(self, msg):
        pass

    def display_bottom_message(self, msg):
        pass

    def display_map_char(self, x, y, tileinfo):
        pass

    def display_char_array(self, the_array):
        pass

    def end(self):
        pass

    def wait_keypress(self):
        pass


class TerrCursesDisplay(TerrDisplay):

    def __init__(self):

        self._cur = curseslib.CursesSession()

        self._topmsg = curseslib.CursesMessageWidget(self._cur, 1, 0, 40, 2)
        self._mapwin = curseslib.CursesCharmapWidget(self._cur, 1, 3, 40, 40)
        self._lowmsg = curseslib.CursesMessageWidget(self._cur, 1, 44, 40, 3)

    def display_top_message(self, msg):

        self._topmsg.display_message(msg)

    def display_bottom_message(self, msg):

        self._lowmsg.display_message(msg)

    def display_map_char(self, x, y, tileinfo):

        char = tileinfo['ascii_code']
        color = tileinfo['curses_colorpair']

        self._mapwin.draw_char(x, y, char, color)
        self._cur.refresh

    def display_char_array(self, the_array):
        self._mapwin.draw_array(the_array)

    def end(self):
        self._cur.end()

    def wait_keypress(self):
        return self._cur.wait_keypress()

class TerrTkinterDisplay(TerrDisplay):

    def __init__(self):
        pass

    def display_top_message(self, msg):
        pass

    def display_bottom_message(self, msg):
        pass

    def display_map_char(self, x, y, tileinfo):
        pass

    def display_char_array(self, the_array):
        pass

    def end(self):
        pass

    def wait_keypress(self):
        pass


class TerrUnitTestDisplay(object):

    def __init__(self):
        print("\nInitializing display.")

    def display_top_message(self, msg):
        print("\nTopMessage: ", msg)

    def display_bottom_message(self, msg):
        print("\nBottomMessage: ", msg)

    def display_map_char(self, x, y, tileinfo):
        pass

    def display_char_array(self, the_array):
        print("\nDisplay full character array")

    def end(self):
        print("\nEnding display")

    def wait_keypress(self):
        entered_text = input("\nPress enter to continue ")
        print("entered text:", entered_text)
        return entered_text

def create_display(class_name):

    the_class = globals()[class_name]
    return the_class()
