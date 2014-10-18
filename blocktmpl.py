class BlockDetails(object):

    def __init__(
        self,
        token,
        isPassable,
        isTransparent,
        char
    ):
        self.token = token
        self.char = char
        self.isPassable = isPassable
        self.isTransparent = isTransparent

    def as_tuple(self):
        return((
            self.token,
            self.isPassable,
            self.isTransparent,
            self.char))


def load_blocks():

    blocks = dict()

    blocks['FLOOR_STONE'] = BlockDetails(
        'FLOOR_STONE', True, True, 46)

    blocks['BLOCK_STONE'] = BlockDetails(
        'BLOCK_STONE', False, False, 35)

    blocks['BLOCK_GLASS'] = BlockDetails(
        'BLOCK_GLASS', False, True, 34)

    blocks['DOORWAY_SECRET'] = BlockDetails(
        'DOORWAY_SECRET', True, False, 35)

    return blocks
