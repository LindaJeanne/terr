import templ

the_arena = None


def setup(generator, shape):
    global the_arena

    templ.load_templates()
    the_arena = generator.create(shape=shape, blockinfo=templ.blockinfo)


def add_creature(creature, location):
    global the_arena

    if not _valid_move(location):
        return False

    if creature in the_arena._creatureSet:
        return False

    if the_arena._tileArray[location].creature:
        return False

    the_arena._tileArray[location].creature = creature
    creature.tile = the_arena._tileArray[location]
    creature.location = location
    the_arena._creatureSet.add(creature)
    creature.arena = the_arena

    return True


def teleport_creature(creature, location):
    global the_arena

    if not _valid_move(location):
        return False

    if creature not in the_arena._creatureSet:
        return False

    if the_arena._tileArray[location].creature:
        return False

    creature.tile.creature = None
    creature.tile = the_arena._tileArray[(location)]
    creature.location = location
    creature.tile.creature = creature

    return True


def add_item(item, location):
    global the_arena

    if not _valid_move(location):
        return False

    if item in the_arena._itemSet:
        return False

    the_arena._itemSet.add(item)

    the_arena._tileArray[location].itemlist.append(item)
    item.location = location
    item.tile = the_arena._tileArray[location]
    item.arena = the_arena

    return True


def teleport_item(item, location):
    global the_arena

    if not _valid_move(location):
        return False

    if item not in the_arena._itemSet:
        return False

    item.tile.itemlist.remove(item)
    item.location = location
    item.tile = the_arena._tileArray[location]
    item.tile.itemlist.append(item)

    return True


def _valid_move(location):
    global the_arena

    if not the_arena.inside_arena(location):
        return False

    if not the_arena._tileArray[location].block['is_walkable']:
        return False

    if the_arena._tileArray[location].creature:
        return False

    return True
