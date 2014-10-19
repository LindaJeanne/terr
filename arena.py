import numpy as np
import gameobjects as go
import templ

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


class ArenaGenerator():

    def run(self, shape, blockinfo):
        new_arena = np.empty(shape, ArenaTile)
        for i, v in np.ndenumerate(new_arena):
            new_arena[i] = ArenaTile(i, blockinfo['FLOOR_STONE'])
        return new_arena


class UnitTestArenaGenerator(ArenaGenerator):

    def run(self, shape, blockinfo):

        new_arena = super().run(shape, blockinfo)

        for i, v in np.ndenumerate(new_arena):
            x_even = ((i[0] % 2) == 0)
            y_even = ((i[1] % 2) == 0)
            if x_even and y_even:
                new_arena[i] = ArenaTile(i, blockinfo['BLOCK_STONE'])

        return new_arena


_tileArray = np.array([])
_itemSet = set()
_creatureSet = set()


def setup(generator, shape):
    global _tileArray
    _tileArray = generator.run(shape, templ.blockinfo)


def create_player(location):
    global _tileArray
    global _creatureSet

    if not inside_arena(location):
        return False

    if not _tileArray[location].block.isPassable:
        return False

    if _tileArray[location].creature:
        return False

    player = go.Player()
    _tileArray[location].creature = player
    player.location = _tileArray[location]
    _creatureSet.add(player)
    return player


def create_creature(template, location):
    global _tileArray
    global _creatureSet

    if not inside_arena(location):
        return None

    if not _tileArray[location].block.isPassable:
        return None

    if _tileArray[location].creature:
        return None

    new_creature = go.Creature(template)
    _tileArray[location].creature = new_creature
    new_creature.location = _tileArray[location]
    _creatureSet.add(new_creature)
    return new_creature


def teleport_creature(creature, location):
    global _tileArray
    global _creatureSet

    assert(creature in _creatureSet)

    if not inside_arena(location):
        return False
    if not _tileArray[location].block.isPassable:
        return False
    if _tileArray[location].creature:
        return False

    creature.location.creature = None
    creature.location = _tileArray[location]
    creature.location.creature = creature

    return True


def step_creature(creature, direction):
    global _tileArray
    global _creatureSet

    assert(creature in _creatureSet)

    old_loc = creature.location._coords
    new_loc = tuple(np.add(old_loc, direction))

    if not inside_arena(new_loc):
        return False

    if not _tileArray[new_loc].block.isPassable:
        return False

    if _tileArray[new_loc].creature:
        return False

    creature.location.creature = None
    creature.location = _tileArray[new_loc]
    creature.location.creature = creature

    return True


def destroy_creature(creature):
    global _tileArray
    global _creatureSet

    assert(creature in _creatureSet)

    creature.location.creature = None
    creature.location = None
    _creatureSet.remove(creature)


def creature_death(creature):
    #message, or whatever else happens here
    destroy_creature(creature)


def create_item(template, location):
    global _tileArray
    global _itemSet

    if not inside_arena(location):
        return None

    if not _tileArray[location].block.isPassable:
        return None

    new_item = go.Item(template)

    new_item.location = _tileArray[location]
    new_item.location.itemlist.append(new_item)
    _itemSet.add(new_item)

    return new_item


def teleport_item(item, location):
    global _tileArray
    global _itemSet

    assert(item in _itemSet)

    if not inside_arena(location):
        return False

    if not _tileArray[location].block.isPassable:
        return False

    item.location.itemlist.remove(item)
    item.location = _tileArray[location]
    item.location.itemlist.append(item)

    return True


def destroy_item(item):
    global _tileArray
    global _itemSet

    if item not in _itemSet:
        return False

    item.location.itemlist.remove(item)
    item.location = None
    _itemSet.remove(item)

    return True


def inside_arena(point):
    global _tileArray

    if len(_tileArray.shape) != len(point):
        # if 'point' has a different number of dimentions than the array,
        # then it's not "inside"
        return False

    difference = np.subtract(_tileArray.shape, point)
    #If any of the values in point are greater than the corresponding
    #value of the arena's shape, then at least one of the element-wise
    #difference elements will be negative.

    for i in difference:
        if i <= 0:
            return False

    return True
