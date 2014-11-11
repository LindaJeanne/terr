import tmpl.itemtmpl


def templ():
    return tmpl.itemtmpl


class Item(object):

    def __init__(self, token, itemdetails):

        self.token = token
        self.glyph = itemdetails['glyph']
        self.detail = itemdetails
        self.arena = None
        self.contain = None

    def get_loc(self):

        return self.contain.get_loc()
