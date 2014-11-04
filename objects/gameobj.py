import display
from . import action


class GameObject(object):

    has_turn_list = list()

    def __init__(self, details):
        assert(details.token)
        assert(details.glyph)

        self.token = details.token
        self.glyph = details.glyph
        self.detail = details
        self.location = None
        self.arena = None

    @classmethod
    def is_valid_tile(cls, arena, location):

        if not arena.inside_arena(location):
            return False

        if not arena.blockArray[location].detail.template['is_walkable']:
            return False

        return True

    def add_to_arena(self, arena, location):
        pass


def create(template):

    class_name = template.template['objclass']
    the_class = globals()[class_name]
    return the_class(template)


class HasTurn(object):

    def take_turn(self):
        action_list = list()
        action_list.append(action.NullAction())
        return action_list


class HasAiTurn(HasTurn):
    pass


class HasPlayerTurn(HasTurn):

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
