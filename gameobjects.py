class GameObject(object):

    def __init__(self, location):
        self.location = location


class Item(GameObject):

    def __init__(self, item_token, location):
        super().__init__(location)


class Creature(GameObject):

    def __init__(self, creature_token, location):
        super().__init__(location)


class Player(Creature):

    def __init__(self, location):
        super().__init__('PLAYER', location)
        self.char = ord('@')
