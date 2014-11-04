import turnmgr
from . import creature


class Player(creature.Creature, turnmgr.HasPlayerTurn):

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
