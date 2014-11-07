import action
import creaturetmpl


class HasTurn(object):

    def take_turn(self):
        action_list = list()
        action_list.append(action.NullAction())
        return action_list


class Creature(object):

    def __init__(self, token, creaturedetails):

        self.token = token
        self.glyph = creaturedetails['glyph']
        self.detail = creaturedetails
        self.arena = None
        self.node = None


class AiCreature(Creature, HasTurn):

    def __init__(self, token, creaturedetails):
        super().__init__(token, creaturedetails)


class NorthGoingZax(AiCreature):
    '''For unit testsing'''

    def __init__(self, token, creaturedetails):
        super().__init__(token, creaturedetails)

    def take_turn(self):

        action_list = list()

        action_list.append(
            action.StepAction((0, -1)))
        action_list.append(
            action.TeleportAction((25, 25)))
        action_list.append(
            action.TeleportAction((33, 33)))

        return action_list


class PlayerChaser(AiCreature):
    '''For unit testing'''

    def __init__(self, token, creaturedetails):
        super().__init__(token, creaturedetails)

    def take_turn(self):

        action_list = list()

        action_list.append(action.PathTowardsAction(
            self.arena.player.node))

        return action_list


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
