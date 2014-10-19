class TurnHandler(object):

    def __init__(self):
        self._skip = False
        self._extra = False
        self._countdown = 0
        self._modulo = 0
        self._mode = 'NORMAL'
        self._ticker = 0

    def take_turn(self):
        self.next()

    def next(self):
        if self._mode == 'NORMAL':
            return

        self._countdown = self._countdown - 1
        if self._countdown <= 0:
            self.normal()
            return

        self._ticker = self._ticker + 1
        if ((self._ticker % self._modulo) == 0):
            if self._mode == 'SLOW':
                self._skip = True
                self._extra = False
            else:  # self._mode == 'FAST'
                self._skip = False
                self._extra = True
        else:
            self._skip = False
            self._extra = False

    def normal(self):
        self._skip = False
        self._extra = False
        self._countdown = 0
        self._modulo = 0
        self._mode = 'NORMAL'
        self._ticker = 0

    def slow(self, amount, turns):
        if self._mode == 'FAST':
            self.normal()
        else:
            self._countdown = turns
            self._modulo = amount
            self._mode = 'SLOW'
            self._skip = True
            self._extra = False

    def fast(self, amount, turns):
        if self._mode == 'SLOW':
            self.normal()
        else:
            self._countdown = turns
            self._modulo = amount
            self._mode = 'FAST'
            self._skip = False
            self._extra = True


class TurnHandlerNull(TurnHandler):
    pass


class PlayerDetails(object):

    def __init__(self, token, char):
        self.token = token
        self.char = char

    def as_tuple(self):
        return((self.token, self.char))


class GameObject(object):

    has_turn_list = list()

    def __init__(self, details, has_turn):
        assert(details.token)
        assert(details.char)
        self.detail = details
        self.location = None


class Item(GameObject):

    def __init__(self, itemdetails):
        super().__init__(itemdetails, False)


class Creature(GameObject):

    def __init__(self, creaturedetails):
        super().__init__(creaturedetails, True)


class Player(GameObject):

    def __init__(self):
        super().__init__(PlayerDetails('PLAYER', 64), True)
