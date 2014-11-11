import action


class HasTurn(object):

    def take_turn(self):
        return action.NullAction()


class HasInventory(object):

    def init_inv(self, invsize):
        self.invsize = invsize
        self.itemlist = list()

    def inv_empty(self):
        return not self.itemlist

    def inv_full(self):
        if not self.itemlist:
            return False

        if len(self.itemlist) >= self.invsize:
            return True

        return False

    def inv_add_item(self, item):

        if self.inv_full():
            return False

        if item.contain:
            item.contain.inv_remove_item(item)

        self.itemlist.append(item)
        item.contain = self

        return True

    def inv_remove_item(self, item):
        if item not in self.itemlist:
            return False

        self.itemlist.remove(item)
        item.contain = None

        return True

    def in_inv(self, item):

        return item in self.itemlist


class CanMove(object):

    def load_movement(self, profile):
        self.movement = profile


class CanAttack(object):

    def load_attack(self, profile):
        self.attack = profile


class CanDefend(object):

    def load_defense(self, profile):
        self.defence = profile


class CanCombat(CanAttack, CanDefend):

    def load_attack_defense(self, attackprofile, defenseprofile):
        self.load_attack(attackprofile)
        self.load_defense(defenseprofile)


class IsTemplated(object):

    def __init__(self, token, template):
        self.token = token
        self.tempalte = template
