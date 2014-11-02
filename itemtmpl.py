import templ


def load_items():

    iteminfo = {
        'PICKAXE': templ.Template({
            'token': 'PICKAXE',
            'objclass': 'Item',
            'glyph': ord('[')}),
        'APPLE': templ.Template({
            'token': 'APPLE',
            'objclass': 'Item',
            'glyph': ord('%')})}

    return iteminfo
