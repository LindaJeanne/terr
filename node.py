# import tmpl.blocktmpl
import tmpl.blocks
import tmpl.blocktype
import tmpl.material
import mixins


NODE_ITEM_INVENTORY_SIZE = 100


class Node(mixins.HasInventory):

    def __init__(self, token, arena=None, location=None):

        self._set_template(token)

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

    def get_loc(self):
        '''used when we don't know what we're getting the loc of.'''
        return self.location

    def find_adj_creature(self):

        for i in self.arena.graph.neighbors(self):
            if i.creature:
                return i.creature

        return False

    def find_adj_item(self):

        for i in self.arena.graph.neighbors(self):
            if i.itemlist:
                return i.itemlist[0]

    def change_template(self, token):
        assert(not self.creature)
        assert(not self.itemlist)

        self._set_template(token)

    def _set_template(self, token):

        template = tmpl.blocks.tmpl[token]

        self.token = token
        self.glyph = template['glyph']
        self.material = tmpl.material.allmats[template['material']]
        self.blockType = tmpl.blocktype.alltypes[template['blocktype']]
        self.isPassable = self.blockType.isPassable
        self.isTransparent = self.material.isTransparent
        self.isLiquid = isinstance(self.material, tmpl.material.MaterialLiquid)
