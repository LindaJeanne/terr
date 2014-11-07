from . import creaturetmpl
from . import itemtmpl
from . import playertmpl

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
    global creatureinfo
    global iteminfo
    global playerclassinfo

    creatureinfo = load_template_list(creaturetmpl.tmpl)
    iteminfo = load_template_list(itemtmpl.tmpl)
    playerclassinfo = load_template_list(playertmpl.tmpl)
