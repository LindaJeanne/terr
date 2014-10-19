
turnHandlers = {}
attackHandlers = {}
defenseHandlers = {}
hasTurn = list()


def load_action_handlers():
    global turnHandlers
    global attackHandlers
    global defenseHandlers

    turnHandlers = {
        'NULL_TURN_HANDLER': None,
        'PLAYER_TURN_HANDLER': None}

    attackHandlers = {
        'NULL_ATTACK_HANDLER': None,
        'PLAYER_ATTACK_HANDLER': None}

    defenseHandlers = {
        'NULL_DEFENSE_HANDLER': None,
        'PLAYER_DEFENSE_HANDLER': None}

load_action_handlers()


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
        return(not self._skip)

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


class TurnHandlerPrint(TurnHandler):

    def take_turn(self):
        self.next()
        if self._skip:
            return False

        print("Turn Handler taking turn", self)

        if self._extra:
            self.take_turn()


class AttackHandler(object):
    pass


class DefenseHandler(object):
    pass
