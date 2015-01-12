import tmpl.blocktmpl as tp

class GameObj(object):

    def __init__(self, token, template, the_arena=None):
        self.token = token
        self.template = template
        self.tileinfo = template['tileinfo']
        self.container = None
        self.arena = the_arena


class Block(GameObj):

    def __init__(self, token, template, the_arena=None):
        super().__init__(token, template, the_arena)

        self.item_list = list()
        self.actor_list = list()
        self.structure = None
        self.player = None
        self.location = (0, 0)

    def add_actor(self, actor):
        return False

    def add_item(self, item):
        return False

    def add_structure(self, structure):
        return False

    def add_player(self, player):
        return False

    def remove_actor(self, actor):
        if actor in self.actor_list:
            self.actor_list.remove(actor)
            return True
        else:
            return False

    def remove_item(self, item):
        if item in self.item_list:
            self.item_list.remove(item)
            return True
        else:
            return False

    def remove_structure(self):
        if self.structure:
            self.structure = None
            return True
        else:
            return False

    def remove_player(self):
        if self.player:
            self.player = None
            return True
        else:
            return False


    def get_display_tile(self):

        if self.player:
            return self.player.tileinfo
        elif self.actor_list:
            return self.actor_list[-1].tileinfo
        elif self.item_list:
            return self.item_list[-1].tileinfo
        elif self.structure:
            return self.structure.tileinfo
        else:
            return self.tileinfo


class OpenBlock(Block):
    pass


class FloorBlock(Block):

    def add_actor(self, actor):
        if actor not in self.actor_list:
            self.actor_list.append(actor)
            if actor.container:
                actor.container.remove_actor(actor)
            actor.container = self
            actor.arena = self.arena
        return True

    def add_item(self, item):
        if item not in self.item_list:
            self.item_list.append(item)
            if item.container:
                item.container.remove_item(item)
            item.container = self
            item.arena = self.arena
        return True

    def add_structure(self, structure):
        if self.structure:
            return False
        else:
            self.structure = structure
            structure.container = self
            structure.arena = self.arena
            return True

    def add_player(self, player):
        if self.player is player:
            return True
        elif self.player:
            return False
        else:
            self.player = player
            if player.container:
                player.container.remove_player()
            player.container = self
            player.arena = self.arena
            return True


class SolidBlock(Block):
    pass


class LiquidBlock(Block):
    pass


def create_block(block_token, the_arena=None):
    template = tp.tmpl[block_token]
    class_name = template['classname']
    the_class = globals()[class_name]
    return the_class(block_token, template, the_arena)
