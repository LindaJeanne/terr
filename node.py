import blocktmpl


class Node(object):

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
        self.itemlist = list()

    def get_glyph(self):

        if self.creature:
            return self.creature.glyph
        elif self.itemlist:
            return self.itemlist[-1].glyph
        else:
            return self.glyph
