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


def tick(gamemgr):

    global _tickloop
    global _counter

    if _tickloop[_counter]:
        for actor in list(_tickloop[_counter]):
            action_list = actor.take_turn()
            if not(_try_actions(actor, action_list, gamemgr)):
                _free_action(actor)
    _increment_counter()


def _try_actions(actor, actionlist, gamemgr):

    for an_action in actionlist:
        if not isinstance(an_action, action.Action):
            print("non-action encountered:", an_action)
            print("actor:", actor)
            print("type:", type(an_action))
            return False
        result = an_action.execute(actor, gamemgr)
        if result:
            _advance_turn(actor, result)
            return result
    return False


def _free_action(the_obj):

    global _tickloop
    global _counter

    _tickloop[_counter].remove(the_obj)
    next_count = (_counter + 1) % LOOP_SIZE

    if not _tickloop[next_count]:
        _tickloop[next_count] = list()
    _tickloop[next_count].append(the_obj)


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
