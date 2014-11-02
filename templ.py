import blocktmpl
import creaturetmpl
import itemtmpl
import playertempl
import gameobjects

blockinfo = dict()
creatureinfo = dict()
iteminfo = dict()
playerclassinfo = dict()


class Template(object):

    all_templates = set()

    def __init__(self, template):
        assert(template['token'])
        assert(template['glyph'])
        assert(template['objclass'])

        self.token = template['token']
        self.glyph = template['glyph']
        self.template = template

    def create(self):
        obj_classname = self.template['objclass']
        obj_class = getattr(gameobjects, obj_classname)

        return obj_class(self)


def load_templates():
    global blockinfo
    global creatureinfo
    global iteminfo
    global playerclassinfo

    blockinfo = blocktmpl.load_blocks()
    creatureinfo = creaturetmpl.load_creatures()
    iteminfo = itemtmpl.load_items()
    playerclassinfo = playertempl.load_playerclasses()
