import numpy as np
import templates.templ as templ
import networkx as nx
import compassrose as cr


class Node(object):

    def __init__(self, blockdetails):
        assert(blockdetails.token)
        assert(blockdetails.glyph)

        self.token = blockdetails.token
        self.glyph = blockdetails.glyph
        self.detail = blockdetails
        self.location = None
        self.creature = None
        self.itemlist = list()

    def get_glyph(self):

        if self.creature:
            return self.creature.glyph
        elif self.itemlist:
            return self.itemlist[-1].glyph
        else:
            return self.glyph


def create_block(token, arena=None, location=None):

    assert(token in templ.blockinfo)
    if arena:
        assert(arena.in_bounds(location))

    new_block = Node(templ.blockinfo[token])
    new_block.location = location
    return new_block


class GridGenerator(object):

    def create(self, shape):

        new_grid = np.empty(shape, object)

        for i, v in np.ndenumerate(new_grid):
            new_grid[i] = 'FLOOR_STONE'

        return new_grid


class UnitTestGridGenerator(GridGenerator):

    def create(self, shape):

        new_grid = super().create(shape)

        for i, v in np.ndenumerate(new_grid):
            x_even = ((i[0] % 2) == 0)
            y_even = ((i[1] % 2) == 0)
            if x_even and y_even:
                new_grid[i] = 'BLOCK_STONE'

        return new_grid


class Arena(object):

    def __init__(self, tokenarray):

        self.grid = np.empty(tokenarray.shape, Node)
        self.graph = nx.DiGraph()
        self.creatureset = set()
        self.itemset = set()
        self.player = None

        self._build_nodes(tokenarray)
        self._build_edges()

    def _build_nodes(self, tokenarray):

        for i, v in np.ndenumerate(tokenarray):
            self.grid[i] = create_block(tokenarray[i], self, i)
            self.graph.add_node(self.grid[i])

    def _build_edges(self):

        for i, v in np.ndenumerate(self.grid):
            rose = cr.CompassRose(i)
            for neighbor in rose.iter_vectors_weights():
                point = neighbor['vector']
                if self.in_bounds(point):
                    self.graph.add_edge(
                        self.grid[i], self.grid[point])

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
        if not self.grid[location].detail.template['is_walkable']:
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
        if not self.grid[location].detail.template['is_walkable']:
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
