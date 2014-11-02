import display
import arena

hasTurn = list()


class TurnHandler(object):

    def __init__(self, actor):
        self._skip = False
        self._extra = False
        self._countdown = 0
        self._modulo = 0
        self._mode = 'NORMAL'
        self._ticker = 0
        self._actor = actor

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


class DefaultTurnHandler(TurnHandler):

    pass


class PlayerTurnHandler(TurnHandler):

    def __init__(self, actor):
        super().__init__(actor)

        self.movement = {
            55: arena.Arena.dir_nw,
            56: arena.Arena.dir_north,
            57: arena.Arena.dir_ne,
            54: arena.Arena.dir_se,
            50: arena.Arena.dir_south,
            49: arena.Arena.dir_sw,
            52: arena.Arena.dir_west}

        self.non_turn = {
            #ord('q'): self._actor.arena.quit
        }

        self.turn = {
            #ord('5'): self._actor.arena.pass_turn
        }

    def take_turn(self, actor):
        self.next()
        if self._skip:
            return False

        end_turn = False

        while not end_turn:

            end_turn = self._handle_key(display.wait_char(), actor)

        if self._extra:
            self.take_turn(actor)

    def _handle_key(self, keypressed, actor):

        #if keypressed in keys.movement:
            #actor.arena.step_creature(actor, keys.movement[keypressed])
            #return True
        #elif keypressed in keys.turn:
            #keys.turn[keypressed]
            #return True
        #elif keypressed in keys.non_turn:
            #keys.non_turn[keypressed]

        return False


class TurnHandlerPrint(TurnHandler):

    def take_turn(self, actor):
        self.next()
        if self._skip:
            return False

        print("Turn Handler taking turn", self)

        if self._extra:
            self.take_turn()


class AttackHandler(object):
    def __init__(self, actor, hit, damage):
        self._actor = actor
        self.hit = hit
        self.damage = damage


class DefaultAttackHandler(AttackHandler):
    pass


class PlayerAttackHandler(AttackHandler):
    pass


class DefenseHandler(object):
    def __init__(self, actor, dodge, soak):
        self._actor = actor
        self.dodge = dodge
        self.soak = soak


class DefaultDefenseHandler(DefenseHandler):
    pass


class PlayerDefenseHandler(DefenseHandler):
    pass
