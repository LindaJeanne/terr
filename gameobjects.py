class PlayerDetails(object):

    def __init__(self, token, char):
        self.token = token
        self.char = char

    def as_tuple(self):
        return((self.token, self.char))


class GameObject(object):

    def __init__(self, details):
        assert(details.token)
        assert(details.char)
        self.detail = details
        self.location = None


class Item(GameObject):

    def __init__(self, itemdetails):
        super().__init__(itemdetails)


class Creature(GameObject):

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)


class Player(GameObject):

    def __init__(self):
        super().__init__(PlayerDetails('PLAYER', 64))
