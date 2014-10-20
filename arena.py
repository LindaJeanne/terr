import numpy as np
import gameobjects as go

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

    def get_display_char(self):

        if self.creature:
            return self.creature.detail.char
        elif self.itemlist:
            return self.itemlist[-1].detail.char
        else:
            return self.block.char


class ArenaGenerator(object):

    def create(self, shape, blockinfo):

        new_arena = Arena(shape)
        for i, v in np.ndenumerate(new_arena._tileArray):
            new_arena._tileArray[i] = ArenaTile(i, blockinfo['FLOOR_STONE'])
        return new_arena


class UnitTestArenaGenerator(ArenaGenerator):

    def create(self, shape, blockinfo):

        new_arena = super().create(shape, blockinfo)

        for i, v in np.ndenumerate(new_arena._tileArray):
            x_even = ((i[0] % 2) == 0)
            y_even = ((i[1] % 2) == 0)
            if x_even and y_even:
                new_arena._tileArray[i] = ArenaTile(
                    i, blockinfo['BLOCK_STONE'])

        return new_arena


class Arena(object):

    dir_north = (0, -1)
    dir_ne = (1, -1)
    dir_east = (1, 0)
    dir_se = (1, 1)
    dir_south = (0, 1)
    dir_sw = (-1, 1)
    dir_west = (-1, 0)
    dir_nw = (-1, -1)

    def __init__(self, shape):
        '''Use and ArenaGenerator rather than instantizing directly'''
        self._tileArray = np.empty(shape, ArenaTile)
        self._itemSet = set()
        self._creatureSet = set()

    def create_player(self, template, location):

        if not self.inside_arena(location):
            return False

        if not self._tileArray[location].block.isPassable:
            return False

        if self._tileArray[location].creature:
            return False

        player = go.Player(template, self)
        self._tileArray[location].creature = player
        player.location = self._tileArray[location]
        self._creatureSet.add(player)
        return player

    def create_creature(self, template, location):

        if not self.inside_arena(location):
            return None

        if not self._tileArray[location].block.isPassable:
            return None

        if self._tileArray[location].creature:
            return None

        new_creature = go.Creature(template, self)
        self._tileArray[location].creature = new_creature
        new_creature.location = self._tileArray[location]
        self._creatureSet.add(new_creature)
        return new_creature

    def teleport_creature(self, creature, location):

        assert(creature in self._creatureSet)

        if not self.inside_arena(location):
            return False
        if not self._tileArray[location].block.isPassable:
            return False
        if self._tileArray[location].creature:
            return False

        creature.location.creature = None
        creature.location = self._tileArray[location]
        creature.location.creature = creature

        return True

    def step_creature(self, creature, direction):

        assert(creature in self._creatureSet)

        old_loc = creature.location._coords
        new_loc = tuple(np.add(old_loc, direction))

        if not self.inside_arena(new_loc):
            return False

        if not self._tileArray[new_loc].block.isPassable:
            return False

        if self._tileArray[new_loc].creature:
            return False

        creature.location.creature = None
        creature.location = self._tileArray[new_loc]
        creature.location.creature = creature

        return True

    def destroy_creature(self, creature):

        assert(creature in self._creatureSet)

        creature.location.creature = None
        creature.location = None
        self._creatureSet.remove(creature)

    def creature_death(self, creature):
        #message, or whatever else happens here
        self.destroy_creature(creature)

    def create_item(self, template, location):

        if not self.inside_arena(location):
            return None

        if not self._tileArray[location].block.isPassable:
            return None

        new_item = go.Item(template, self)

        new_item.location = self._tileArray[location]
        new_item.location.itemlist.append(new_item)
        self._itemSet.add(new_item)

        return new_item

    def teleport_item(self, item, location):

        assert(item in self._itemSet)

        if not self.inside_arena(location):
            return False

        if not self._tileArray[location].block.isPassable:
            return False

        item.location.itemlist.remove(item)
        item.location = self._tileArray[location]
        item.location.itemlist.append(item)

        return True

    def destroy_item(self, item):

        if item not in self._itemSet:
            return False

        item.location.itemlist.remove(item)
        item.location = None
        self._itemSet.remove(item)

        return True

    def inside_arena(self, point):

        if len(self._tileArray.shape) != len(point):
            # if 'point' has a different number of dimentions than the array,
            # then it's not "inside"
            return False

        difference = np.subtract(self._tileArray.shape, point)
        #If any of the values in point are greater than the corresponding
        #value of the arena's shape, then at least one of the element-wise
        #difference elements will be negative.

        for i in difference:
            if i <= 0:
                return False

        return True
