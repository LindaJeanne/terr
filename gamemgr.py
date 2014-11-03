import templ
import display

the_arena = None
turn_list = list()


def setup(generator, shape):
    global the_arena

    templ.load_templates()
    the_arena = generator.create(shape=shape, blockinfo=templ.blockinfo)


def playermsg(msg):
    pass


def generalmsg(msg):
    pass


def get_block(location):
    return the_arena.blockArray[location]


def add_creature(creature, location):
    global the_arena
    global turn_list

    if not _valid_move_creature(location):
        return False

    if creature in the_arena.creatureset:
        return False

    turn_list.append(creature)

    the_arena.blockArray[location].creature = creature
    creature.block = the_arena.blockArray[location]
    creature.location = location
    the_arena.creatureset.add(creature)
    creature.arena = the_arena

    return True


def teleport_creature(creature, location):
    global the_arena

    if not _valid_move_creature(location):
        return False

    if creature not in the_arena.creatureset:
        return False

    creature.block.creature = None
    creature.block = the_arena.blockArray[location]
    creature.location = location
    creature.block.creature = creature

    return True


def add_item(item, location):
    global the_arena

    if not _valid_move_item(location):
        return False

    if item in the_arena.itemset:
        return False

    the_arena.itemset.add(item)

    item.location = location
    item.block = the_arena.blockArray[location]
    item.block.itemlist.append(item)
    item.arena = the_arena

    return True


def teleport_item(item, location):
    global the_arena

    if not _valid_move_item(location):
        return False

    if item not in the_arena.itemset:
        return False

    item.block.itemlist.remove(item)
    item.location = location
    item.block = the_arena.blockArray[location]
    item.block.itemlist.append(item)

    return True


def add_player(player, location):
    global the_arena
    global turn_list

    if not _valid_move_creature(location):
        return False

    the_arena.player = player
    add_creature(player, location)

    return True


def _valid_move_creature(location):

    if not _valid_move_item(location):
        return False

    if the_arena.blockArray[location].creature:
        return False

    return True


def _valid_move_item(location):
    global the_arena

    if not the_arena.inside_arena(location):
        return False

    if not get_block(location).detail.template['is_walkable']:
        return False

    return True


def quit():
    display.end_curses()
    raise SystemExit
