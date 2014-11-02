import templ


def load_blocks():

    blocks = {
        'FLOOR_STONE': templ.Template({
            'token': 'FLOOR_STONE',
            'glyph': 46,
            'is_walkable': True,
            'is_transparent': True}),
        'BLOCK_STONE': templ.Template({
            'token': 'BLOCK_STONE',
            'glyph': 35,
            'is_walkable': False,
            'is_transparent': False}),
        'BLOCK_GLASS': templ.Template({
            'token': 'BLOCK_GLASS',
            'glyph': 34,
            'is_walkable': False,
            'is_transparent': True}),
        'DOORWAY_SECRET': templ.Template({
            'token': 'DOORWAY_SECRET',
            'glyph': 35,
            'is_walkable': True,
            'is_transparent': False})}

    return blocks
