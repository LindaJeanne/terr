import templtempl


class PlayerTemplate(templtempl.TemplateTemplate):
    pass


def load_playerclasses():
    playerclassinfo = {
        'PLAYER_DEFAULT': PlayerTemplate(
            token='PLAYER_DEFAULT',
            char=64,
            turn_handler='PlayerTurnHandler',
            combat_info={
                'attack_handler': 'PlayerAttackHandler',
                'defense_handler': 'PlayerDefenseHandler',
                'hit': 5,
                'damage': (5, 5),
                'dodge': 5,
                'soak': (5, 5)})}

    return playerclassinfo
