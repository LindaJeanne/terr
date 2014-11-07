import creature
import action
import playertmpl
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

    def __init__(self, token, playerdetails):
        super().__init__(token, playerdetails)


def create(token):

    try:
        template = playertmpl.tmpl[token]
        class_name = template['classname']
        the_class = globals()[class_name]
        the_player = the_class(token, template)
    except:
        print("exception while trying to create player from template.")
        raise

    return the_player
