import numpy as np
import networkx as nx


class Action(object):
    pass

    def execute(self, actor):
        return 10


class NullAction(Action):

    def execute(self, actor):
        return 1


# ========================================================
# Movement Actions
# ========================================================


class MovementAction(Action):

    def _path_dir_from_dest(self, actor, dest_node):

        the_graph = actor.arena.navgraph

        the_path = nx.astar_path(
            the_graph, dest_node, actor.node)

        return tuple(np.subtract(
            the_path[-2].location,
            actor.node.location))

    def _coords_from_direction(self, actor, dir_vector):

        return tuple(np.add(actor.node.location, dir_vector))

    def _move_if_legal(self, actor, dest_coords):

        if actor.is_legal_loc(dest_coords):
            actor.arena.place_creature(actor, dest_coords)
            return 10

        return 1


class TeleportAction(MovementAction):

    def __init__(self, dest_coords):
        self.dest_coords = dest_coords

    def execute(self, actor):

        return self._move_if_legal(actor, self.dest_coords)


class StepAction(MovementAction):

    def __init__(self, direction_vector):
        self.direction_vector = direction_vector

    def execute(self, actor):

        dest_coords = self._coords_from_direction(actor, self.direction_vector)

        return self._move_if_legal(actor, dest_coords)


class PathTowardsAction(MovementAction):

    def __init__(self, dest_node):
        self.dest_node = dest_node

    def execute(self, actor):

        dir_vector = self._path_dir_from_dest(actor, self.dest_node)
        dest_coords = self._coords_from_direction(actor, dir_vector)

        return self._move_if_legal(actor, dest_coords)


class PathAwayAction(MovementAction):

    def __init__(self, avoid_node):
        self.avoid_node = avoid_node

    def execute(self, actor):

        un_dir_vector = self._path_dir_from_dest(actor, self.avoid_node)
        dir_vector = tuple(np.multiply(-1, un_dir_vector))
        dest_coords = self._coords_from_direction(actor, dir_vector)

        return self._move_if_legal(actor, dest_coords)


# ========================================================
# Inventory Actions
# ========================================================


class PickUpAction(Action):

    def __init__(self, item):
        self.item = item

    def execute(self, actor):

        if actor.pickup_item(self.item):
            return 10
        else:
            return 1


class DropAction(Action):

    def __init__(self, item):
        self.item = item

    def execute(self, actor):

        if actor.drop_item(self.item):
            return 10
        else:
            return 1


# ========================================================
# Combat
# ========================================================

class MeleeAction(Action):

    def __init__(self, target):
        self.target = target

    def execute(self, actor):
        return 10


# ========================================================
# Construction
# ========================================================

class BuildAction(Action):
    '''Abstract class -- instantize through subclass.'''

    def __init__(self, node, item):
        self.node = node
        self.item = item
        self.blocktoken = item.buildToken

        assert(item.buildToken)
        assert(node.isPassable)

    def execute(self, actor):

        assert(self.node.isPassable)
        assert(self.item in actor.itemlist)

        actor.inv_remove_item(self.item)
        self.node.arena.itemset.remove(self.item)

        self.node.change_template(self.blocktoken)

        return 10
