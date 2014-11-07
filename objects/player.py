from . import creature
from . import action
import display
import compassrose as cr


class Player(creature.Creature, creature.HasTurn):

    movement_keys = cr.key_dirs

    turn_action_keys = {}

    free_action_keys = {
        ord('q'): 'quit'}

    def take_turn(self):

        action_list = list()

        keypressed = display.wait_char()
        display.display_top_message("Key pressed =" + str(keypressed))

        if keypressed in self.movement_keys:
            action_list.append(
                action.StepAction(self.movement_keys[keypressed]))

        elif keypressed in self.turn_action_keys:
            action_list.append(action.NullAction())

        elif keypressed in self.free_action_keys:
            action_list.append(action.QuitAction())

        else:
            action_list.append(action.NullAction())

        return action_list

    def __init__(self, playerdetails):
        super().__init__(playerdetails)


def create(template):

    assert('objclass' in template.template)
    class_name = template.template['objclass']

    assert(class_name in globals())
    the_class = globals()[class_name]

    return the_class(template)
