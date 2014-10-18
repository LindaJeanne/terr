class CreatureDetails(object):
    def __init__(self, token, char, hit, damage, dodge, soak):
        self.token = token
        self.char = char
        self.hit = hit
        self.damage = damage
        self.dodge = dodge
        self.soak = soak

    def as_tuple(self):
        return((
            self.token,
            self.char,
            self.hit,
            self.damage,
            self.dodge,
            self.soak))


def load_creatures():
    creatureinfo = dict()

    creatureinfo['FIRE_ELEMENTAL'] = CreatureDetails(
        'FIRE_ELEMENTAL', 69, 10, (5, 11), 8, (4, 9))

    creatureinfo['RABBIT'] = CreatureDetails(
        'RABBIT', 114, 5, (1, 3), (3), (0, 2))

    return creatureinfo
