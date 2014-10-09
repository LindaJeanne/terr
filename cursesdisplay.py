import curses


class CursesDisplay():
    #color pairs
    COLOR_WHITE_ON_BLACK = 1
    COLOR_BLUE_ON_BLACK = 2
    COLOR_GREEN_ON_BLACK = 3
    COLOR_RED_ON_BLACK = 4
    COLOR_YELLOW_ON_BLACK = 5

    def __init__(self):

        self.panels = dict()
        self.panels['SCREEN'] = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        self.panels['SCREEN'].keypad(True)
        self.initializeColors()

    def initializeColors(self):

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def addPanel(screenToken, shape):
        pass

    def display_char(self, x, y, char, color, screenToken='SCREEN'):
        '''displays a character at a given location on the given screen.

        'color' is a number representing a curses color pair; those
        initialized in this class are given as class-level constants'''

        self.panels[screenToken].addch(y, x, char, curses.color_pair(color))

    def display_string(self, string, x, y, color, screenToken='SCREEN'):
        pass

    def end_screen(self, screenToken):
        '''close out the screen with the given token.

        Other screens will still be active, and curses will not
        be shut down. In order to shut down curses, call
        end_curses()'''

        self.panels[screenToken].screen.keypad(False)

    def end_curses(self):
        '''close all curses screens and return terminal to normal'''

        for screen in self.panels:
            self.panels[screen].keypad(False)
        self.finalize()

    def finalize(self):
        '''called by end_curses to clean up'''

        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def refresh(self, screenToken='SCREEN'):
        '''call this to redraw the screen and see your updates'''

        self.panels[screenToken].refresh()

    def wait_char(self, screenToken='SCREEN'):
        '''wait until a key is pressed, and get the key'''

        return self.panels[screenToken].getch()
