import templtempl


class CreatureTemplate(templtempl.TemplateTemplate):
    pass


def load_creatures():
    creatureinfo = dict()

    creatureinfo['FIRE_ELEMENTAL'] = CreatureTemplate(
        token="FIRE_ELEMENTAL",
        char=69,
        turn_handler="DefaultTurnHandler",
        combat_info={
            'attack_handler': "DefaultAttackHandler",
            'defense_handler': "DefaultDefenseHandler",
            'hit': 10,
            'damage': (5, 11),
            'dodge': 8,
            'soak': (4, 9)})

    creatureinfo['RABBIT'] = CreatureTemplate(
        token="RABBIT",
        char=114,
        turn_handler="DefaultTurnHandler",
        combat_info={
            'attack_handler': "DefaultAttackHandler",
            'defense_handler': "DefaultDefenseHandler",
            'hit': 5,
            'damage': (1, 3),
            'dodge': 3,
            'soak': (0, 2)})

    return creatureinfo
