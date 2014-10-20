import templtempl


class ItemTemplate(templtempl.TemplateTemplate):
    pass


def load_items():

    iteminfo = dict()

    iteminfo['PICKAXE'] = ItemTemplate(
        'PICKAXE', 91)

    iteminfo['APPLE'] = ItemTemplate(
        'APPLE', 37)

    return iteminfo
