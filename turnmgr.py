import numpy as np
import display

LOOP_SIZE = 1000
_tickloop = np.empty((LOOP_SIZE), list)
_counter = 0


def setup(has_turn_list):

    global _tickloop
    global _counter

    _tickloop = np.empty((LOOP_SIZE), list)
    _counter = 0
    _tickloop[_counter] = has_turn_list


def tick():

    global _tickloop
    global _counter

    if _tickloop[_counter]:
        for i in list(_tickloop[_counter]):
            _advance_turn(i, i.take_turn())

    _increment_counter()


def _advance_turn(the_obj, num_ticks):

    global LOOP_SIZE
    global _tickloop
    global _counter

    assert(the_obj in _tickloop[_counter])
    new_tick = (_counter + num_ticks) % LOOP_SIZE

    if not _tickloop[new_tick]:
        _tickloop[new_tick] = list()

    _tickloop[_counter].remove(the_obj)
    _tickloop[new_tick].append(the_obj)


def _increment_counter():

    global LOOP_SIZE
    global _counter

    _counter = (_counter + 1) % LOOP_SIZE


class HasTurn(object):

    def take_turn(self):
        return 10


class HasAiTurn(HasTurn):
    pass


class HasPlayerTurn(HasTurn):

    movement_keys = {
        ord('7'): (-1, -1),
        ord('8'): (0, -1),
        ord('9'): (1, -1),
        ord('4'): (1, 0),
        ord('6'): (-1, 0),
        ord('1'): (-1, 1),
        ord('2'): (0, 1),
        ord('3'): (1, 1)}

    turn_action_keys = {}

    free_action_keys = {
        ord('q'): 'quit'}

    def take_turn(self):

        keypressed = display.wait_char()

        if keypressed in self.movement_keys:
            new_loc = tuple(np.add(
                self.location,
                self.movement_keys[keypressed]))
            self.teleport(new_loc)
            return 10

        if keypressed in self.turn_action_keys:
            pass

        if keypressed in self.free_action_keys:
            #temporary, until I can get input organized.
            display.end_curses()
            raise SystemExit

        return 10
