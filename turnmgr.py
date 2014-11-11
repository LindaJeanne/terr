import numpy as np
import action


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

    return_dict = {}

    if _tickloop[_counter]:
        for actor in list(_tickloop[_counter]):

            the_action = actor.take_turn()

            if not isinstance(the_action, action.Action):
                print("non-action encountered:", the_action)
                print("actor:", actor)
                print("type:", type(the_action))
                return False

            result = the_action.execute(actor)
            _advance_turn(actor, max(result, 1))
            return_dict[actor] = the_action

    _increment_counter()
    return return_dict


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
