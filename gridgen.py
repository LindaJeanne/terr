import numpy as np


class GridGenerator(object):

    def create(self, shape):

        new_grid = np.empty(shape, object)

        for i, v in np.ndenumerate(new_grid):
            new_grid[i] = 'BLOCK_AIR'

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
