import numpy as np

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
            self.neighbors[i] = {
                'vector': new_xy + (suffix),
                'weight': named_dirs[i]['weight']}

    def iter_vectors(self):

        for i in self.neighbors:
            yield self.neighbors[i]['vector']

    def iter_vectors_weights(self):

        for i in self.neighbors:
            yield self.neighbors[i]
