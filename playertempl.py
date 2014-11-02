import templ


def load_playerclasses():

    playerclassinfo = {
        'PLAYER_DEFAULT': templ.Template({
            'token': 'PLAYER_DEFAULT',
            'glyph': ord('@'),
            'objclass': 'Player',
            'turn_handler': 'PlayerTurnHandler',
            'combat_info': {
                'attack_handler': 'PlayerAttackHandler',
                'defense_handler': 'PlayerDefenseHandler',
                'hit': 5,
                'damage': (5, 5),
                'dodge': 5,
                'soak': (5, 5)}})}

    return playerclassinfo
