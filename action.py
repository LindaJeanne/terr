import numpy as np
import networkx as nx


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


class PathTowardsAction(Action):

    def __init__(self, node):
        self.node = node

    def execute(self, actor, the_gamemgr):

        the_graph = the_gamemgr.the_arena.navgraph
        the_path = nx.astar_path(
            the_graph,  self.node, actor.node)

        try:
            the_gamemgr.the_arena.place_creature(actor, the_path[-2].location)
        except:
            return 0

        return 10


class QuitAction(Action):

    def execute(self, actor, the_gamemgr):

        the_gamemgr.display.end_curses()
        raise SystemExit


class NullAction(Action):

    def execute(self, actor, the_gamemgr):
        return 0
