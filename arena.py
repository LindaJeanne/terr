import numpy as np
import networkx as nx
import compassrose as cr
import node


class Arena(object):

    def __init__(self, tokenarray):

        self.grid = np.empty(tokenarray.shape, node.Node)
        self.graph = nx.DiGraph()
        self.navgraph = nx.DiGraph()
        self.creatureset = set()
        self.itemset = set()
        self.player = None

        self._build_nodes(tokenarray)
        self._build_edges()
        self._build_navgraph()

    def _build_nodes(self, tokenarray):

        for i, v in np.ndenumerate(tokenarray):
            self.grid[i] = node.Node(tokenarray[i], self, i)
            self.graph.add_node(
                self.grid[i],
                {'ispassable': self.grid[i].isPassable})

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
                'ispassable': isPassable})

    def _build_navgraph(self):

        navnodes = (
            n for n in self.graph if self.graph.node[n]['ispassable'])
        self.navgraph = self.graph.subgraph(navnodes)

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

        if self.grid[location].creature:
            print("Cannot place", creature)
            print("Bcause", self.grid[location].creature)
            print("Is alreayd occupying", location)
            raise Exception

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
            item.contain.inv_remove_item(item)
            # item.contain.itemlist.remove(item)
        else:
            self.itemset.add(item)
            item.arena = self

        self.grid[location].inv_add_item(item)

    def remove_item(self, item):

        if item not in self.itemset:
            return False

        item.contain.inv_remove_item(item)
        item.arena = None
        self.itemset.remove(item)

    def find_creatures_in_radius(self, node, radius):

        egograph = nx.ego_graph(self.graph, node, radius)

        return_list = list()

        for i in egograph:
            if i.creature:
                # returning i.creature will return a copy that
                # was created along with the egograph. We need
                # to pull in the one from self instead.
                return_list.append(self.grid[i.location].creature)

        return return_list

    def find_items_in_radius(self, node, radius):

        egograph = nx.ego_graph(self.graph, node, radius)
        return_list = list()

        for i in egograph:
            if i.itemlist:
                # need to use the itemlist from self rather
                # than i.itemlist, which has copies made
                # when the egograph was created.
                the_items = self.grid[i.location].itemlist
                return_list = return_list + the_items
        return return_list

    def get_closest_creature(self, node, radius):

        candidates = self.find_creatures_in_radius(node, radius)

        if node.creature:
            candidates.remove(node.creature)

        if not candidates:
            return False

        current_candidate = {}

        # just calculating a fast-and-simple manhatten distance to
        # each candidate for now. May want to graduate to something
        # like K-d tress when I have more agents running around, but
        # this will do for now.

        for i in candidates:
            next_candidate = {
                'creature': i,
                'distance': self._get_manhatten_distance(
                    node.location, i.node.location)}

            if not current_candidate:
                current_candidate = next_candidate
            elif next_candidate['distance'] < current_candidate['distance']:
                current_candidate = next_candidate

        # Since we've been looking at copies produced by the generation of
        # the egograph, we need to go back and get the actual one.

        return self.grid[current_candidate['creature'].node.location].creature

    def _get_manhatten_distance(self, point_one, point_two):

        assert(len(point_one) == len(point_two))

        the_distance = 0
        for i in range(0, len(point_one)):
            the_distance += abs(point_one[i] - point_two[i])

        return the_distance


class Arena2D(Arena):

    def __init__(self, tokenarray):
        assert(len(tokenarray.shape) == 2)

        super().__init__(tokenarray)


class Arena3D(Arena):

    def __init__(self, tokenarray):
        assert(len(tokenarray.shape) == 3)

        super().__init__(tokenarray)
