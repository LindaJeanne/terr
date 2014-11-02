import blocktmpl
import creaturetmpl
import itemtmpl
import playertempl

blockinfo = dict()
creatureinfo = dict()
iteminfo = dict()
playerclassinfo = dict()


class Template(object):

    all_templates = set()

    def __init__(self, template):
        assert(template['token'])
        assert(template['glyph'])

        self.token = template['token']
        self.glyph = template['glyph']
        self.template = template


def load_templates():
    global blockinfo
    global creatureinfo
    global iteminfo
    global playerclassinfo

    blockinfo = blocktmpl.load_blocks()
    creatureinfo = creaturetmpl.load_creatures()
    iteminfo = itemtmpl.load_items()
    playerclassinfo = playertempl.load_playerclasses()
