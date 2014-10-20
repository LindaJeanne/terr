import templtempl


class BlockTemplate(templtempl.TemplateTemplate):

    def __init__(
        self,
        token,
        isPassable,
        isTransparent,
        char
    ):
        super().__init__(token, char)
        self.isPassable = isPassable
        self.isTransparent = isTransparent


def load_blocks():

    blocks = dict()

    blocks['FLOOR_STONE'] = BlockTemplate(
        'FLOOR_STONE', True, True, 46)

    blocks['BLOCK_STONE'] = BlockTemplate(
        'BLOCK_STONE', False, False, 35)

    blocks['BLOCK_GLASS'] = BlockTemplate(
        'BLOCK_GLASS', False, True, 34)

    blocks['DOORWAY_SECRET'] = BlockTemplate(
        'DOORWAY_SECRET', True, False, 35)

    return blocks
