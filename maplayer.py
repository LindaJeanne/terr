import numpy as np
import noise
import random

#@staticmethod
#@classmethod


class MapLayer(np.ndarray):

    '''Subclass of ndarray for creating 2D map layers.

    Contains additional functions for generating perlin
    noise, arrays filled with random numbers, smoothing,
    and the like. Will always cast itself as 2D.'''

    def gen_random(self):
        ''' generate a 2D array of random numbers

        returns a MapLayer array (subclas of ndarray) of
        the same size and shape of 'self'. This array is
        then filled with random numbers on a linear scale
        between 0 and 1. '''

        return np.fromfunction(
            lambda x, y: random.random(),
            (self.shape))

    # Generate an array of perlin noise
    def gen_perlin(
            self,
            offset=.5,
            octaves=1,
            persistence=0.5,
            lacunarity=2.0):
        ''' generate a 2D array of Perlin noise

            returns a MapLayer array (subclass of ndarray) of
            the same size and shape as 'self'. This array is
            filled with perlin noise.'''

        perlin_array = np.zeros(self.shape)
        for i, v in np.ndenumerate(perlin_array):
            x = i[0]
            y = i[1]
            perlin_array[x][y] = noise.pnoise2(
                x + offset,
                y + offset,
                octaves,
                persistence,
                lacunarity)
        return perlin_array

    def get_sum_neighbors(self):
        '''Generates array conaining sums from another array

        Creates a new MapLayer (subclas of ndarray) array,
        of the same size and shape as the current array. Every
        cell of the new array conains the sum of all the values
        in the eight neighbor-cells of the corresponding cell
        in the original array.'''

        neighbor_array = np.zeros(self.shape)
        for i, j in np.ndenumerate(self):
            x = i[0]
            y = i[1]
            cell_sum = 0
            for m in (-1, 0, 1):
                for n in (-1, 0, 1):
                    if (x + m >= 0 and
                            x + m < self.shape[0] and
                            y + n >= 0 and
                            y + n < self.shape[1]):
                        cell_sum = cell_sum + self[x + m][y + n]
            neighbor_array[x][y] = cell_sum
        return neighbor_array

    def apply_automata(self):
        '''Apply a cellular automata function to this array

        Currently, this is very basic and inflexable, mostly here
        for proof of concept. Later, there should be a way of
        generating different types of cellular automata.'''

        neighbors = self.get_sum_neighbors()
        for i, j in np.ndenumerate(self):
            x = i[0]
            y = i[1]
            if (neighbors[x][y] > 0 and j < 0):
                self[x][y] = j + (neighbors[x][y] / 8)
            elif (neighbors[x][y] < 0 and j > 0):
                self[x][y] = j + (neighbors[x][y] / 24)
