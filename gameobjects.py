import templ


class GameObject(object):

    def __init__(self, details):
        assert(details.token)
        assert(details.char)
        self.detail = details


class Item(GameObject):
    index = set()

    def __init__(self, itemdetails):
        super().__init__(itemdetails)
        Item.index.add(self)

    def destroy(self):
        Item.index.remove(self)


class Creature(GameObject):
    index = set()

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails)
        Creature.index.add(self)

    def destroy(self):
        Creature.index.remove(self)


class Player(GameObject):

    def __init__(self):
        super().__init__(templ.ObjDetails('PLAYER', 64))
