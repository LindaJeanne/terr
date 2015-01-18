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

    def ask_char(self, msg):
        pass

    def ask_tile(self, msg):
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


class TerrUnitTestDisplay(TerrDisplay):

    def display_top_message(self, msg):
        print("\nTopMessage: ", msg)

    def display_bottom_message(self, msg):
        print("\nBottomMessage: ", msg)

    def wait_keypress(self):
        # print("Wait_keypress called. Returning ord('2').")
        return ord('2')


class TerrTextDisplay(TerrUnitTestDisplay):
    def __init__(self):
        print("\nInitializing display.")

    def display_char_array(self, the_array):
        print("\nDisplay Full character array")

    def end(self):
        print("\nEnding display.")

    def wait_keypress(self):
        the_input = input("Input function called. Hit one key, then return.")
        return ord(the_input)

    def ask_char(self, msg):
        pass

    def ask_tile(self, msg):
        pass

# adding this so that I can access it from within action.py without
# creating a circular dependency.
# TODO: either remove the need for this, or remove the implication
#       that it should be possible to have more than one display
#       at once.

the_display = None


def create_display(class_name):
    global the_display

    the_class = globals()[class_name]
    the_display = the_class()
    return the_display
