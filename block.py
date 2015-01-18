import tmpl.blocktmpl as tp
import gridgraph as gg


class Block(gg.GridNode):

    def __init__(self, coords, token, template, the_arena=None):

        super().__init__(coords, self._get_key_dict())
        self.token = token
        self.template = template
        self.arena = the_arena

        self.item_list = list()
        self.actor_list = list()
        self.structure = None
        self.player = None

    def _get_key_dict(self):
        '''Will be overriden by subclasses'''

        return {
            'WALKING': False,
            'FLYING': False,
            'SWIMMING': False,
            'PHASING': False
        }

    def add_player(self, the_player):
        if self.keys['WALKING']:
            if the_player.location:
                the_player.location.the_player = None
            the_player.location = self
            return True
        else:
            return False

    def add_creature(self, the_creature):
        if self.keys['WALKING']:
            if the_creature.container:
                the_creature.container.remove_creature(the_creature)
            the_creature.container = self
            self.actor_list.append(the_creature)
            return True
        else:
            return False

    def remove_creature(self, the_creature):
        if the_creature in self.actor_list:
            self.actor_list.remove(the_creature)
            return True
        else:
            return False

    def add_item(self, the_item):
        if self.keys['WALKING']:
            if the_item.container:
                the_item.container.remove_item(the_item)
            the_item.container = self
            self.item_list.append(the_item)
            return True
        else:
            return False

    def remove_item(self, the_item):
        if the_item in self.item_list:
            self.item_list.remove(the_item)
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


class SolidBlock(Block):

    def _get_key_dict(self):

        return {
            'WALKING': False,
            'FLYING': False,
            'SWIMMING': False,
            'PHASING': True
        }


class AirBlock(Block):

    def _get_key_dict(self):

        return {
            'WALKING': False,
            'FLYING': True,
            'SWIMMING': False,
            'PHASING': True
        }


class FloorBlock(Block):

    def _get_key_dict(self):

        return {
            'WALKING': True,
            'FLYING': True,
            'SWIMMING': False,
            'PHASING': True
        }


class LiquidBlock(Block):

    def _get_key_dict(self):

        return {
            'WALKING': False,
            'FLYING': False,
            'SWIMMING': True,
            'PHASING': True
        }


def create_block(block_token, the_arena=None):
    template = tp.tmpl[block_token]
    class_name = template['classname']
    the_class = globals()[class_name]
    return the_class((0, 0), block_token, template, the_arena)
