import action
import creaturetmpl
import mixins
import display


class Creature(mixins.HasInventory):

    def __init__(self, token, creaturedetails):

        self.token = token
        self.glyph = creaturedetails['glyph']
        self.detail = creaturedetails
        self.arena = None
        self.node = None

        self.init_inv(creaturedetails['invsize'])

    def pickup_item(self, item):
        if self.inv_full():
            return False

        if self.node is item.contain:
            return self.inv_add_item(item)

        return False

    def drop_item(self, item):
        if item not in self.itemlist:
            return False

        self.inv_remove_item(item)
        return self.node.inv_add_item(item)

    def is_legal_loc(self, coords):

        if not self.arena.in_bounds(coords):
            return False

        node = self.arena.grid[(coords)]

        if any((node.creature, not node.isPassable)):
            return False

        return True


class AiCreature(Creature, mixins.HasTurn):

    def __init__(self, token, creaturedetails):
        super().__init__(token, creaturedetails)


class NorthGoingZax(AiCreature):
    '''For unit testsing'''

    def __init__(self, token, creaturedetails):
        super().__init__(token, creaturedetails)

    def take_turn(self):

        if self.node.location[1] > 0:
            return action.StepAction((0, -1))
        else:
            return action.TeleportAction((
                self.node.location[0],
                self.arena.grid.shape[1] - 1))


class PlayerChaser(AiCreature):
    '''For unit testing'''

    def __init__(self, token, creaturedetails):
        super().__init__(token, creaturedetails)

    def take_turn(self):

        return action.PathTowardsAction(
            self.arena.player.node)


class PickupDropper(AiCreature):
    '''For unit testing'''

    def __init__(self, token, creaturedetails):
        super().__init__(token, creaturedetails)

    def take_turn(self):

        if self.node.is_adjacent(self.arena.player.node):
            if self.inv_empty():
                display.display_top_message(
                    "next to player, inv empty, path away")
                return action.PathAwayAction(self.arena.player.node)
            else:
                display.display_top_message(
                    "next to player, inv not empty, drop item")
                return action.DropAction(self.itemlist[-1])
        elif all((not self.node.inv_empty(), not self.node.inv_full())):
                display.display_top_message(
                    "item on tile and inv not full: picking up.")
                return action.PickUpAction(self.node.itemlist[0])
        else:
                display.display_top_message(
                    "path towards player")
                return action.PathTowardsAction(self.arena.player.node)


def create(token):

    try:
        template = creaturetmpl.tmpl[token]
        class_name = template['classname']
        the_class = globals()[class_name]
        the_creature = the_class(token, template)
    except:
        print("Exception while creating creature from template")
        raise

    return the_creature
