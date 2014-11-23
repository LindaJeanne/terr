tmpl = {
    'BLOCKTYPE_SOLID': {
        'classname': 'BlockType',
        'ispassable': False
    },
    'BLOCKTYPE_WALL': {
        'classname': 'BlockType',
        'ispassable': False
    },
    'BLOCKTYPE_OPEN': {
        'classname': 'BlockType',
        'ispassable': True
    },
    'BLOCKTYPE_LIQUID': {
        'classname': 'BlockType',
        'ispassable': True
    },
    'BLOCKTYPE_PASSAGE': {
        'classname': 'BlockType',
        'ispassable': True
    },
    'BLOCKTYPE_FENCE': {
        'classname': 'BlockType',
        'ispassable': False
    }
}


alltypes = {}


class BlockType(object):

    def __init__(self, token, template):
        self.token = token
        self.template = template
        self.isPassable = template['ispassable']


def load_blocktypes():

    global alltypes

    if alltypes:
        return

    for token in tmpl:
        template = tmpl[token]
        the_class = globals()[template['classname']]
        alltypes[token] = the_class(token, template)


load_blocktypes()
