import numpy as np

dir_north = (0, -1)
dir_ne = (1, -1)
dir_east = (1, 0)
dir_se = (1, 1)
dir_south = (0, 1)
dir_sw = (-1, 1)
dir_west = (-1, 0)
dir_nw = (-1, -1)


class ArenaTile(object):

    def __init__(self, coords, blockinfo):
        self.creature = None
        self.itemlist = list()
        self.block = blockinfo
        self._coords = coords

    def add_creature(self, creature):
        if self.creature:
            return False  # remove current creature before adding new one.
        else:
            self.creature = creature

        assert(creature.detail.token)
        assert(creature.detail.char)

        return True

    def rmv_creature(self):
        if self.creature:
            self.creature = False
            return True
        else:
            return False  # There is no creature to remove

    def add_item(self, item):
        if item in self.itemlist:
            return False  # we don't need to add it, it's there already
        else:
            assert(item.detail.token)
            assert(item.detail.char)
            self.itemlist.append(item)
            return True

    def rmv_item(self, item):
        if item in self.itemlist:
            self.itemlist.remove(item)
            return True
        else:
            return False

    def get_display_char(self):

        if self.creature:
            return self.creature.detail.char
        elif self.itemlist:
            return self.itemlist[-1].detail.char
        else:
            return self.block.char


class Arena(object):

    def __init__(self, template_arr, blockinfo_arr):

        self.tile_array = np.empty_like(template_arr, ArenaTile)
        self.creatureset = set()
        self.itemset = set()

        for i, v in np.ndenumerate(template_arr):
            self.tile_array[i] = ArenaTile(
                i, blockinfo_arr[v])

    def add_item(self, item, location):
        assert(self.tile_array[location])
        assert(item not in self.itemset)

        self.tile_array[location].itemlist.append(item)
        self.itemset.add(item)
        item.location = self.tile_array[location]

    def destroy_item(self, item):
        assert(item in self.itemset)

        item.location.itemlist.remove(item)
        item.location = None
        self.itemset.remove(item)

    def teleport_item(self, item, location):
        assert(item in self.itemset)
        assert(self.tile_array[location])

        item.location.itemlist.remove(item)
        item.location = self.tile_array[location]
        item.location.itemlist.append(item)

    def add_creature(self, creature, location):
        assert(self.tile_array[location])
        assert(creature not in self.creatureset)
        assert(not self.tile_array[location].creature)

        self.tile_array[location].creature = creature
        creature.location = self.tile_array[location]
        self.creatureset.add(creature)

    def teleport_creature(self, creature, location):
        assert(self.tile_array[location])
        assert(creature in self.creatureset)
        assert(not self.tile_array[location].creature)

        creature.location.creature = None
        self.tile_array[location].creature = creature
        creature.location = self.tile_array[location]

    def destroy_creature(self, creature):
        assert(creature in self.creatureset)

        creature.location.creature = None
        creature.location = None
        self.creatureset.remove(creature)

    def step_creature(self, creature, direction):

        assert(creature in self.creatureset)
        old_x = creature.location._coords[0]
        old_y = creature.location._coords[1]
        old_loc = (old_x, old_y)
        new_loc = tuple(np.add(old_loc, direction))

        x_in_bounds = self.tile_array.shape[0] > new_loc[0]
        y_in_bounds = self.tile_array.shape[1] > new_loc[1]

        if not (x_in_bounds and y_in_bounds):
            return False  # can't move off the grid

        elif self.tile_array[new_loc].creature:
            return False  # alread a crature there.

        elif self.tile_array[new_loc].block.isPassable:
            self.tile_array[new_loc].creature = creature
            creature.location = self.tile_array[new_loc]
            self.tile_array[old_loc].creature = None
            return True

        else:
            return False  # Tile wasn't enterable.

    def creature_death(self, creature):
        assert(creature in self.creatureset)
        self.destroy_creature(creature)
        #placeholder for dynamic message
        return "A creature has died!"
