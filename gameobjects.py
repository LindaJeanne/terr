import action


class PlayerDetails(object):

    def __init__(self, token, char):
        self.token = token
        self.char = char
        self.turn_handler = 'PlayerTurnHandler'
        self.combat_info = {
            'attack_handler': 'PlayerAttackHandler',
            'defense_handler': 'PlayerDefenseHandler',
            'hit': 5,
            'damage': (5, 5),
            'dodge': 5,
            'soak': (5, 5)}

    def as_tuple(self):
        return((self.token, self.char))


class GameObject(object):

    has_turn_list = list()

    def __init__(self, details, arena):
        assert(details.token)
        assert(details.char)
        self.detail = details
        self.location = None
        self.arena = arena

        if details.turn_handler:
            self.turn_handler = vars(
                action)[details.turn_handler](self)
            action.hasTurn.append(self)
        else:
            self.turn_handler = None

        if details.combat_info:

            self.attack_handler = vars(
                action)[details.combat_info['attack_handler']](
                self,
                details.combat_info['hit'],
                details.combat_info['damage'])

            self.defense_handler = vars(
                action)[details.combat_info['defense_handler']](
                self,
                details.combat_info['dodge'],
                details.combat_info['soak'])
        else:
            self.attack_handler = None
            self.defense_handler = None
            self.stats = None


class Item(GameObject):

    def __init__(self, itemdetails, arena):
        super().__init__(itemdetails, arena)


class Creature(GameObject):

    def __init__(self, creaturedetails, arena):
        super().__init__(creaturedetails, arena)


class Player(GameObject):

    def __init__(self, arena):
        super().__init__(PlayerDetails('PLAYER', 64), arena)
