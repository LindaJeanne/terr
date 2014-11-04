from . import blocktmpl
from . import creaturetmpl
from . import itemtmpl
from . import playertmpl

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


def load_template_list(inlist):
    outlist = {}
    for i in inlist:
        token = i['token']
        outlist[token] = Template(i)

    return outlist


def load_templates():
    global blockinfo
    global creatureinfo
    global iteminfo
    global playerclassinfo

    blockinfo = load_template_list(blocktmpl.tmpl)
    creatureinfo = load_template_list(creaturetmpl.tmpl)
    iteminfo = load_template_list(itemtmpl.tmpl)
    playerclassinfo = load_template_list(playertmpl.tmpl)
