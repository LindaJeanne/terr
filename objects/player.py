from . import gameobj
from . import creature
from . import action
import display


class HasPlayerTurn(gameobj.HasTurn):

    movement_keys = {
        ord('7'): (-1, -1),
        ord('8'): (0, -1),
        ord('9'): (1, -1),
        ord('4'): (-1, 0),
        ord('6'): (1, 0),
        ord('1'): (-1, 1),
        ord('2'): (0, 1),
        ord('3'): (1, 1)}

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


class Player(creature.Creature, HasPlayerTurn):

    def __init__(self, playerdetails):
        super().__init__(playerdetails)

    def add_to_arena(self, arena, location):
        if not super().add_to_arena(arena, location):
            return False

        arena.player = self

        return True


def create(template):

    assert('objclass' in template.template)
    class_name = template.template['objclass']

    assert(class_name in globals())
    the_class = globals()[class_name]

    return the_class(template)
