from . import action


class HasTurn(object):

    def take_turn(self):
        action_list = list()
        action_list.append(action.NullAction())
        return action_list


class Creature(object):

    def __init__(self, creaturedetails):
        assert(creaturedetails.token)
        assert(creaturedetails.glyph)

        self.token = creaturedetails.token
        self.glyph = creaturedetails.glyph
        self.detail = creaturedetails
        self.arena = None
        self.node = None


class AiCreature(Creature, HasTurn):

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)


class NorthGoingZax(AiCreature):
    '''For unit testsing'''

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)

    def take_turn(self):

        action_list = list()

        action_list.append(
            action.StepAction((0, -1)))
        action_list.append(
            action.TeleportAction((25, 25)))
        action_list.append(
            action.TeleportAction((33, 33)))

        return action_list


def create(template):

    assert('objclass' in template.template)
    class_name = template.template['objclass']

    assert(class_name in globals())
    the_class = globals()[class_name]

    return the_class(template)
