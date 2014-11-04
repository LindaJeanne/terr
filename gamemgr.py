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


def new_creature(templ_token, location):
    global the_arena
    global turn_list

    if not gameobj.Creature.is_valid_tile(the_arena, location):
        return False

    assert(templ_token in templ.creatureinfo)
    template = templ.creatureinfo[templ_token]

    the_creature = gameobj.create(template)
    the_creature.add_to_arena(the_arena, location)
    #turn_list.append(the_creature)
    #the_arena.creatureset.add(the_creature)

    #_set_creature_location(the_creature, location)

    return the_creature


def teleport_creature(creature, location):
    global the_arena

    if not gameobj.Creature.is_valid_tile(the_arena, location):
        return False

    if not creature in the_arena.creatureset:
        return False

    _set_creature_location(creature, location)

    return True


def new_item(templ_token, location):

    global the_arena

    if not gameobj.Item.is_valid_tile(the_arena, location):
        return False

    assert(templ_token in templ.iteminfo)
    template = templ.iteminfo[templ_token]

    the_item = gameobj.create(template)
    the_item.add_to_arena(the_arena, location)

    #the_arena.itemset.add(the_item)
    #_set_item_location(the_item, location)

    return the_item


def teleport_item(item, location):
    global the_arena

    if not item.is_valid_tile(the_arena, location):
        return False

    if not item in the_arena.itemset:
        return False

    _set_item_location(item, location)

    return True


def new_player(templ_token, location):
    global the_arena
    global turn_list

    if not gameobj.Player.is_valid_tile(the_arena, location):
        return False

    assert(templ_token in templ.playerclassinfo)
    template = templ.playerclassinfo[templ_token]
    the_player = gameobj.create(template)
    the_player.add_to_arena(the_arena, location)

    #the_arena.player = the_player
    #turn_list.append(the_player)
    #the_arena.creatureset.add(the_player)

    #_set_creature_location(the_player, location)

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


def quit():
    display.end_curses()
    raise SystemExit
