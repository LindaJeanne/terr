import templ


def load_creatures():

    creatureinfo = {
        'FIRE_ELEMENTAL': templ.Template({
            'token': 'FIRE_ELEMENTAL',
            'glyph': ord('E'),
            'objclass': 'AiCreature'}),

        'RABBIT': templ.Template({
            'token': 'RABBIT',
            'glyph': ord('r'),
            'objclass': 'AiCreature'}),

        'NORTH_GOING_ZAX': templ.Template({
            'token': 'NORTH_GOING_ZAX',
            'glyph': ord('Z'),
            'objclass': 'NorthGoingZax'})}

    return creatureinfo
