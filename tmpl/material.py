tmpl = {

    'MATERIAL_STONE': {
        'classname': 'MaterialSolid',
        'istransparent': False,
        'isflamable': False
    },
    'MATERIAL_AIR': {
        'classname': 'MaterialGaseous',
        'istransparent': True,
        'isflamable': False
    },
    'MATERIAL_GLASS': {
        'classname': 'MaterialSolid',
        'istransparent': True,
        'isflamable': False
    },
    'MATERIAL_WATER': {
        'classname': 'MaterialLiquid',
        'istransparent': True,
        'isflamable': False
    },
    'MATERIAL_WOOD': {
        'classname': 'MaterialSolid',
        'istransparent': False,
        'isflamable': True
    }
}


allmats = {}


class Material(object):

    def __init__(self, token, template):
        self.token = token
        self.template = template
        self.isTransparent = template['istransparent']
        self.isFlamable = template['isflamable']


class MaterialSolid(Material):
    pass


class MaterialLiquid(Material):
    pass


class MaterialGaseous(Material):
    pass


class MaterialPlasm(Material):
    pass


def load_mats():

    global allmats

    if allmats:
        return

    for token in tmpl:
        template = tmpl[token]
        the_class = globals()[template['classname']]
        allmats[token] = the_class(token, template)


load_mats()
