import templ


def load_creatures():

    creatureinfo = {
        'FIRE_ELEMENTAL': templ.Template({
            'token': 'FIRE_ELEMENTAL',
            'glyph': ord('E'),
            'objclass': 'AiCreature',
            'turn_handler': 'DefaultTurnHandler',
            'combat_info': {
                'attack_handler': 'DefaultAttackHandler',
                'defense_handler': 'DefaultDefenseHandler',
                'hit': 10,
                'damage': (5, 11),
                'dodge': 8,
                'soak': (4, 9)}}),

        'RABBIT': templ.Template({
            'token': 'RABBIT',
            'glyph': ord('r'),
            'objclass': 'AiCreature',
            'turn_handler': 'DefaultTurnHandler',
            'combat_info': {
                'attack_handler': 'DefaultAttackHandler',
                'defense_handler': 'DefaultDefenseHandler',
                'hit': 5,
                'damage': (1, 3),
                'dodge': 3,
                'soak': (0, 2)}}),

        'NORTH_GOING_ZAX': templ.Template({
            'token': 'NORTH_GOING_ZAX',
            'glyph': ord('Z'),
            'objclass': 'NorthGoingZax',
            'turn_handler': 'DefaultTurnHandler'})}

    return creatureinfo
