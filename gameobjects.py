import action


class GameObject(object):

    has_turn_list = list()

    def __init__(self, details, arena=None):
        assert(details.token)
        assert(details.glyph)

        self.token = details.token
        self.glyph = details.glyph
        self.detail = details
        self.location = None
        self.arena = arena

        if 'turn_handler' in details.template:
            self.turn_handler = vars(
                action)[details.template['turn_handler']](self)
            action.hasTurn.append(self)
        else:
            self.turn_handler = None

        if 'combat_info' in details.template:

            combat = details.template['combat_info']

            self.attack_handler = vars(
                action)[combat['attack_handler']](
                self,
                combat['hit'],
                combat['damage'])

            self.defense_handler = vars(
                action)[combat['defense_handler']](
                self,
                combat['dodge'],
                combat['soak'])
        else:
            self.attack_handler = None
            self.defense_handler = None
            self.stats = None


class Block(GameObject):

    def __init__(self, blockdetails, arena=None):
        super().__init__(blockdetails, arena)


class Item(GameObject):

    def __init__(self, itemdetails, arena=None):
        super().__init__(itemdetails, arena)
        self.tile = None


class Creature(GameObject):

    def __init__(self, creaturedetails, arena=None):
        super().__init__(creaturedetails, arena)
        self.tile = None


class AiCreature(Creature):

    def __init__(self, creaturedetails, arena=None):
        super().__init__(creaturedetails, arena)


class Player(Creature):

    def __init__(self, playerdetails, arena=None):
        super().__init__(playerdetails, arena)
