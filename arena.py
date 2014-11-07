import numpy as np
import networkx as nx
import compassrose as cr
import node


class Arena(object):

    def __init__(self, tokenarray):

        self.grid = np.empty(tokenarray.shape, node.Node)
        self.graph = nx.DiGraph()
        self.creatureset = set()
        self.itemset = set()
        self.player = None

        self._build_nodes(tokenarray)
        self._build_edges()

    def _build_nodes(self, tokenarray):

        for i, v in np.ndenumerate(tokenarray):
            self.grid[i] = node.Node(tokenarray[i], self, i)
            self.graph.add_node(self.grid[i])

    def _build_edges(self):

        for i, v in np.ndenumerate(self.grid):
            rose = cr.CompassRose(i)
            for neighbor in rose.iter_vectors_weights():
                point = neighbor['vector']
                if self.in_bounds(point):
                    self._add_edge(self.grid[i], neighbor)

    def _add_edge(self, source, neighbor):

        point = neighbor['vector']

        isPassable = all((
            source.isPassable,
            self.grid[point].isPassable))

        self.graph.add_edge(
            source,
            self.grid[point],
            {
                'weight': neighbor['weight'],
                'is_passable': isPassable})

    def in_bounds(self, point):

        if len(self.grid.shape) != len(point):
            return False

        for i in point:
            if i < 0:
                return False

        difference = np.subtract(self.grid.shape, point)
        for i in difference:
            if i <= 0:
                return False

        return True

    def place_creature(self, creature, location):

        assert(self.in_bounds(location))
        assert(not self.grid[location].creature)
        if not self.grid[location].isPassable:
            raise Exception("non walkable block error")

        if creature in self.creatureset:
            creature.node.creature = None
        else:
            self.creatureset.add(creature)

        creature.node = self.grid[location]
        creature.node.creature = creature
        creature.arena = self

    def remove_creature(self, creature):

        if creature not in self.creatureset:
            return False

        creature.node.creature = None
        creature.node = None
        self.creatureset.remove(creature)
        creature.arena = None
        return True

    def place_item(self, item, location):

        assert(self.in_bounds(location))
        if not self.grid[location].isPassable:
            raise Exception("Trying to place item on non walkable tile")

        if item in self.itemset:
            item.contain.itemlist.remove(item)
        else:
            self.itemset.add(item)

        item.contain = self.grid[location]
        item.contain.itemlist.append(item)
        item.arena = self

    def remove_item(self, item):

        if item not in self.itemset:
            return False

        item.contain.itemlist.remove(item)
        item.contain = None
        item.arena = None
        self.itemset.remove(item)


class Arena2D(Arena):

    def __init__(self, tokenarray):
        assert(len(tokenarray.shape) == 2)

        super().__init__(tokenarray)


class Arena3D(Arena):

    def __init__(self, tokenarray):
        assert(len(tokenarray.shape) == 3)

        super().__init__(tokenarray)
