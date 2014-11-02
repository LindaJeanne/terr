import templ


def load_items():

    iteminfo = {
        'PICKAXE': templ.Template({
            'token': 'PICKAXE',
            'glyph': ord('[')}),
        'APPLE': templ.Template({
            'token': 'APPLE',
            'glyph': ord('%')})}

    return iteminfo
