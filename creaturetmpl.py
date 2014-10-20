class CreatureDetails(object):
    #def __init__(self, token, char, hit, damage, dodge, soak):
        #self.token = token
        #self.char = char
        #self.hit = hit
        #self.damage = damage
        #self.dodge = dodge
        #self.soak = soak

    def __init__(self, token, char, turn_handler, combat_info):
        self.token = token
        self.char = char
        self.turn_handler = turn_handler
        self.combat_info = combat_info

    def as_tuple(self):
        return((
            self.token,
            self.char,
            self.turn_handler,
            self.combat_info))


def load_creatures():
    creatureinfo = dict()

    creatureinfo['FIRE_ELEMENTAL'] = CreatureDetails(
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

    creatureinfo['RABBIT'] = CreatureDetails(
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
