import blocktmpl
import mixins


NODE_ITEM_INVENTORY_SIZE = 100


class Node(mixins.HasInventory):

    def __init__(self, token, arena=None, location=None):

        template = blocktmpl.tmpl[token]

        self.token = token
        self.glyph = template['glyph']
        self.isPassable = template['ispass']
        self.isLiquid = template['isliquid']
        self.isTransparent = template['istransparent']

        self.arena = arena
        self.location = location
        self.creature = None

        global NODE_ITEM_INVENTORY_SIZE
        self.init_inv(NODE_ITEM_INVENTORY_SIZE)

    def get_glyph(self):

        if self.creature:
            return self.creature.glyph
        elif self.itemlist:
            return self.itemlist[-1].glyph
        else:
            return self.glyph

    def is_adjacent(self, node):

        return node in self.arena.graph.neighbors(self)
