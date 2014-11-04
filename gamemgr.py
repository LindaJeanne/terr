import templates.templ as templ
import display
import objects.player as pl
import objects.item as it
import objects.creature as crea

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

    if not crea.Creature.is_valid_tile(the_arena, location):
        return False

    assert(templ_token in templ.creatureinfo)
    template = templ.creatureinfo[templ_token]

    the_creature = crea.create(template)
    the_creature.add_to_arena(the_arena, location)
    turn_list.append(the_creature)

    return the_creature


#def teleport_creature(creature, location):
#    global the_arena

#    if not crea.Creature.is_valid_tile(the_arena, location):
#        return False

#    if not creature in the_arena.creatureset:
#        return False

#    _set_creature_location(creature, location)

#    return True


def new_item(templ_token, location):

    global the_arena

    if not it.Item.is_valid_tile(the_arena, location):
        return False

    assert(templ_token in templ.iteminfo)
    template = templ.iteminfo[templ_token]

    the_item = it.create(template)
    the_item.add_to_arena(the_arena, location)

    return the_item


def new_player(templ_token, location):
    global the_arena
    global turn_list

    if not pl.Player.is_valid_tile(the_arena, location):
        return False

    assert(templ_token in templ.playerclassinfo)
    template = templ.playerclassinfo[templ_token]
    the_player = pl.create(template)
    the_player.add_to_arena(the_arena, location)
    turn_list.append(the_player)

    return the_player


def quit():
    display.end_curses()
    raise SystemExit
