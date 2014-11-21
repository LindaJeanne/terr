import creature
import action
import tmpl.playertmpl
import display
import mixins
import util


def templ():
    return tmpl.playertmpl


def pickup_an_item(actor):
    return action.PickUpAction(actor.node.itemlist[-1])


def drop_an_item(actor):
    return action.DropAction(actor.itemlist[-1])


class Player(creature.Creature, mixins.CanMove):

    movement_keys = util.key_dirs

    turn_action_keys = {
        ord(','): pickup_an_item,
        ord('d'): drop_an_item}

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
            return self.turn_action_keys[keypressed](self)

        elif keypressed in self.free_action_keys:
            return action.QuitAction(display)

        else:
            return action.NullAction()


class UnitTestPlayer(Player):

    def take_turn(self):
        return action.NullAction()
