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
