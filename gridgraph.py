import networkx as nx
import numpy as np


compas_rose = list((
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),  (1, 0),
    (-1, 1), (0, 1), (1, 1)))


class GridGraphSet(object):

    def __init__(self, node_array, key_list):
        self.grid = node_array
        self.key_list = key_list
        self.graphs = {}

        for key in key_list:
            self.build_graph(key)

    def build_graph(self, key):
        self.graphs[key] = nx.Graph()
        for i, cell in np.ndenumerate(self.grid):
            if cell.nav_value(key):
                self.graphs[key].add_node(cell)
        self.rebuild_edges(key)

    def rebuild_edges(self, key):
        for i, cell in np.ndenumerate(self.grid):
            for neighbor in self.get_neighbors(cell):
                if all((
                        cell.nav_value(key),
                        neighbor.nav_value(key))):
                    self.graphs[key].add_edge(cell, neighbor)

    def get_neighbors(self, cell):
        global compas_rose
        res_list = list()
        for dir_vec in compas_rose:
            next_cell = self.cell_step(cell, dir_vec)
            if next_cell:
                res_list.append(next_cell)
        return res_list

    def cell_at(self, coords):

        for i in coords:
            if i < 0:
                return None

        try:
            result = self.grid[coords]
        except Exception:
            result = None
        finally:
            return result

    def cell_step(self, the_start, the_dir):
        return self.cell_at(tuple(np.add(the_start.location, the_dir)))

    def get_graph(self, key):
        return self.graphs[key]


class GridNode(object):

    def __init__(self, coords, key_dict):
        self.location = coords
        self.keys = key_dict

    def get_loc(self):
        return self.location

    def nav_value(self, key):
        try:
            result = self.keys[key]
        except Exception:
            result = None
        finally:
            return result
