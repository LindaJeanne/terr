import numpy as np


class Action(object):
    pass

    def execute(self, actor, the_gamemgr):
        return 10


class MovementAction(Action):

    def __init__(self, location):
        self.location = location

    def execute(self, actor, the_gamemgr):

        try:
            the_gamemgr.the_arena.place_creature(actor, self.location)
        except:
            return 0

        return 10


class StepAction(MovementAction):

    def __init__(self, direction):
        self.direction = direction
        self.location = None

    def execute(self, actor, the_gamemgr):

        new_loc = tuple(np.add(
            actor.node.location, self.direction))

        self.location = new_loc

        return super().execute(actor, the_gamemgr)


class TeleportAction(MovementAction):

    def __init__(self, location):
        self.location = location

    def execute(self, actor, the_gamemgr):

        return super().execute(actor, the_gamemgr)


class QuitAction(Action):

    def execute(self, actor, the_gamemgr):

        the_gamemgr.display.end_curses()
        raise SystemExit


class NullAction(Action):

    def execute(self, actor, the_gamemgr):
        return 0
