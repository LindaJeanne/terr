import numpy as np

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


def _advance_turn(gameobj, num_ticks):

    global LOOP_SIZE
    global _tickloop
    global _counter

    assert(gameobj in _tickloop[_counter])
    new_tick = (_counter + num_ticks) % LOOP_SIZE

    if not _tickloop[new_tick]:
        _tickloop[new_tick] = list()

    _tickloop[_counter].remove(gameobj)
    _tickloop[new_tick].append(gameobj)


def _increment_counter():

    global LOOP_SIZE
    global _counter

    _counter = (_counter + 1) % LOOP_SIZE
