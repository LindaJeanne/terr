import numpy as np


def create(mod, token):
    template = mod.templ().tmpl[token]
    the_class = getattr(mod, template['classname'])
    return the_class(token, template)


def manhattan_dist(point_one, point_two):

    assert(len(point_one) == len(point_two))

    total_dist = 0
    for i in range(0, len(point_one)):
        total_dist += abs(point_one[i] - point_two[i])

    return total_dist


def cross_manhattan_dist(point_one, point_two):

    assert(len(point_one) == len(point_two))

    delta_dist = list()
    for i in range(0, len(point_one)):
        delta_dist[i] = abs(point_one[i] - point_two[i])

    # 2^(1/2), 3^(1/3), 4^(1/4), and 5^(1/5) are all pretty
    # close to 1.4. We can improve the return value of the
    # manhatten distance without adding root calculations
    # by using this approximation.

    min_side = min(delta_dist)

    total_dist = 0
    for i in len(point_one):
        total_dist += delta_dist[i] - min_side

    total_dist += 1.4 * min_side

    return total_dist


def modular_inc(counter, modulus, number):
    return (counter + number) % modulus


key_dirs = {
    ord('7'): (-1, -1),
    ord('8'): (0, -1),
    ord('9'): (1, -1),
    ord('4'): (-1, 0),
    ord('6'): (1, 0),
    ord('1'): (-1, 1),
    ord('2'): (0, 1),
    ord('3'): (1, 1)}


named_dirs = {
    'nw': {
        'vector': (-1, -1),
        'weight': 1.4},
    'north': {
        'vector': (0, -1),
        'weight': 1},
    'ne': {
        'vector': (1, -1),
        'weight': 1.4},
    'west': {
        'vector': (-1, 0),
        'weight': 1},
    'east': {
        'vector': (1, 0),
        'weight': 1},
    'sw': {
        'vector': (-1, 1),
        'weight': 1.4},
    'south': {
        'vector': (0, 1),
        'weight': 1},
    'se': {
        'vector': (1, 1),
        'weight': 1.4}}


class CompassRose(object):

    def __init__(self, coords):

        self.neighbors = {}

        prefix = coords[:2]
        if coords[2:]:
            suffix = coords[2:]
        else:
            suffix = None

        for i in named_dirs:
            new_xy = tuple(np.add(prefix, named_dirs[i]['vector']))
            if suffix:
                new_coord = new_xy + (suffix)
            else:
                new_coord = new_xy

            self.neighbors[i] = {
                'vector': new_coord,
                'weight': named_dirs[i]['weight']}

    def iter_vectors(self):

        for i in self.neighbors:
            yield self.neighbors[i]['vector']

    def iter_vectors_weights(self):

        for i in self.neighbors:
            yield self.neighbors[i]
