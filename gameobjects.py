import action


class PlayerDetails(object):

    def __init__(self, token, char):
        self.token = token
        self.char = char
        self.turn_handler = action.turnHandlers['PLAYER_TURN_HANDLER']
        self.combat_info = {
            'attack_handler': 'PLAYER_ATTACK_HANDLER',
            'defense_handler': 'PLAYER_DEFENSE_HANDLER',
            'hit': 5,
            'damage': (5, 5),
            'dodge': 5,
            'soak': (5, 5)}

    def as_tuple(self):
        return((self.token, self.char))


class GameObject(object):

    has_turn_list = list()

    def __init__(self, details):
        assert(details.token)
        assert(details.char)
        self.detail = details
        self.location = None

        if details.turn_handler:
            self.turn_handler = action.turnHandlers[details.turn_handler]
            action.hasTurn.append(self)
        else:
            self.turn_handler = None

        if details.combat_info:

            attack = details.combat_info['attack_handler']
            defense = details.combat_info['defense_handler']

            self.attack_handler = action.attackHandlers[attack]
            self.defense_handler = action.defenseHandlers[defense]
            self.stats = details.combat_info
        else:
            self.attack_handler = None
            self.defense_handler = None
            self.stats = None


class Item(GameObject):

    def __init__(self, itemdetails):
        super().__init__(itemdetails)


class Creature(GameObject):

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)


class Player(GameObject):

    def __init__(self):
        super().__init__(PlayerDetails('PLAYER', 64))
