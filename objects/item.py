class Item(object):

    def __init__(self, itemdetails):
        assert(itemdetails.token)
        assert(itemdetails.glyph)

        self.token = itemdetails.token
        self.glyph = itemdetails.glyph
        self.detail = itemdetails
        self.arena = None
        self.contain = None


def create(template):

    assert('objclass' in template.template)
    class_name = template.template['objclass']

    assert(class_name in globals())
    the_class = globals()[class_name]

    return the_class(template)
