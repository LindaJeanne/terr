import creature
import action
import tmpl.playertmpl
import display
import mixins
import util


def templ():
    return tmpl.playertmpl


class Player(creature.Creature, mixins.HasTurn):

    movement_keys = util.key_dirs

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
