import templates.templ as templ
import display
import gameobj

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


def new_creature(template, location):
    global the_arena
    global turn_list

    if not _valid_move_creature(location):
        return False

    the_creature = gameobj.create(template)
    turn_list.append(the_creature)
    the_creature.arena = the_arena
    the_arena.creatureset.add(the_creature)

    _set_creature_location(the_creature, location)

    return the_creature


def teleport_creature(creature, location):
    global the_arena

    if not _valid_move_creature(location):
        return False

    if creature not in the_arena.creatureset:
        return False

    _set_creature_location(creature, location)

    return True


def new_item(template, location):

    global the_arena

    if not _valid_move_item(location):
        return False

    the_item = gameobj.create(template)
    the_item.arena = the_arena
    the_arena.itemset.add(the_item)

    _set_item_location(the_item, location)

    return the_item


def teleport_item(item, location):
    global the_arena

    if not _valid_move_item(location):
        return False

    if item not in the_arena.itemset:
        return False

    _set_item_location(item, location)

    return True


def new_player(tempalte, location):
    global the_arena
    global turn_list

    if not _valid_move_creature(location):
        return False

    the_player = gameobj.create(tempalte)
    the_arena.player = the_player
    the_player.arena = the_arena
    turn_list.append(the_player)
    the_arena.creatureset.add(the_player)

    _set_creature_location(the_player, location)

    return the_player


def _set_creature_location(creature, location):

    if creature.block:
        creature.block.creature = None
    creature.block = get_block(location)
    creature.block.creature = creature
    creature.location = location


def _set_item_location(item, location):

    if item.block:
        item.block.itemlist.remove(item)
    item.block = get_block(location)
    item.block.itemlist.append(item)
    item.location = location


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
