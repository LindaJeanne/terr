import blocktmpl
import creaturetmpl
import itemtmpl

blockinfo = dict()
creatureinfo = dict()
iteminfo = dict()


def load_templates():
    global blockinfo
    global creatureinfo
    global iteminfo

    blockinfo = blocktmpl.load_blocks()
    creatureinfo = creaturetmpl.load_creatures()
    iteminfo = itemtmpl.load_items()
