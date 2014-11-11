import display
import arena

the_arena = None
turn_list = list()


def setup(generator, shape):
    global the_arena
    the_arena = arena.Arena(generator.create(shape))


# def new_creature(token, location):
#    global the_arena
#    global turn_list

#    the_creature = util.cr(creature, token)
#    the_arena.place_creature(the_creature, location)
#    turn_list.append(the_creature)

#    return the_creature


# def new_item(token, location):

#    global the_arena

#    the_item = item.create(token)
#    the_arena.place_item(the_item, location)

#    return the_item


# def new_player(token, location):
#    global the_arena
#    global turn_list

#    the_player = player.create(token)
#    the_arena.place_creature(the_player, location)
#    the_arena.player = the_player
#    turn_list.append(the_player)

#    return the_player


def quit():
    display.end_curses()
    raise SystemExit
