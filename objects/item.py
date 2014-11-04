from . import gameobj


class Item(gameobj.GameObject):

    def __init__(self, itemdetails):
        super().__init__(itemdetails)
        self.block = None

    def add_to_arena(self, arena, location):

        if not self.is_valid_tile(arena, location):
            return False

        if self in arena.itemset:
            return False

        arena.itemset.add(self)
        arena.blockArray[location].itemlist.append(self)
        self.location = location
        self.block = arena.blockArray[location]
        self.arena = arena

        return True

    def teleport(self, location):

        if not self.arena:
            return False

        if not self.is_valid_tile(self.arena, location):
            return False

        self.block.itemlist.remove(self)
        self.block = self.arena.blockArray[location]
        self.block.itemlist.append(self)
        self.location = location

        return True


def create(template):

    assert('objclass' in template.template)
    class_name = template.template['objclass']

    assert(class_name in globals())
    the_class = globals()[class_name]

    return the_class(template)
