import itemtmpl


class Item(object):

    def __init__(self, token, itemdetails):

        self.token = token
        self.glyph = itemdetails['glyph']
        self.detail = itemdetails
        self.arena = None
        self.contain = None


def create(token):

    try:
        template = itemtmpl.tmpl[token]
        class_name = template['classname']
        the_class = globals()[class_name]
        the_item = the_class(token, template)
    except:
        print("Exception while creating item from template.")
        raise

    return the_item
