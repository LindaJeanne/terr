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

    try:
        template = templ.creatureinfo[templ_token]

        the_creature = crea.create(template)
        the_arena.place_creature(the_creature, location)
        turn_list.append(the_creature)
    except:
        return False

    return the_creature


def new_item(templ_token, location):

    global the_arena

    try:
        template = templ.iteminfo[templ_token]
        the_item = it.create(template)
        the_arena.place_item(the_item, location)
    except:
        return False

    return the_item


def new_player(templ_token, location):
    global the_arena
    global turn_list

    try:
        template = templ.playerclassinfo[templ_token]
        the_player = pl.create(template)

        the_arena.place_creature(the_player, location)
        the_arena.player = the_player
        turn_list.append(the_player)
    except:
        return False

    return the_player


def quit():
    display.end_curses()
    raise SystemExit
