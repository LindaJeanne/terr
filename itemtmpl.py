class ItemDetails(object):

    def __init__(self, token, char):
        self.token = token
        self.char = char

    def as_tuple(self):
        return((self.token, self.char))


def load_items():

    iteminfo = dict()

    iteminfo['PICKAXE'] = ItemDetails(
        'PICKAXE', 91)

    iteminfo['APPLE'] = ItemDetails(
        'APPLE', 37)

    return iteminfo
