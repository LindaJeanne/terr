import creature
import action
import playertmpl
import display
import compassrose as cr
import mixins


class Player(creature.Creature, mixins.HasTurn):

    movement_keys = cr.key_dirs

    turn_action_keys = {}

    free_action_keys = {
        ord('q'): 'quit'}

    def __init__(self, token, playerdetails):
        super().__init__(token, playerdetails)

    def take_turn(self):

        keypressed = display.wait_char()
        display.display_top_message("Key pressed =" + str(keypressed))

        if keypressed == ord('q'):
            display.end_curses()
            raise SystemExit
        if keypressed in self.movement_keys:
            return action.StepAction(self.movement_keys[keypressed])

        elif keypressed in self.turn_action_keys:
            return action.NullAction()

        elif keypressed in self.free_action_keys:
            return action.QuitAction(display)

        else:
            return action.NullAction()


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
