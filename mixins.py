import action
import attacktmpl
import defensetmpl


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


class AttackProfile(object):

    def __init__(self, token, template):
        self.token = token
        self.attacks = template['attacks']
        self.useWeaopon = template['useweapon']
        self.template = template


class BasicAttackProfile(AttackProfile):
    pass


class DefenseProfile(object):

    def __init__(self, token, template):
        self.token = token
        self.dodge_chance = template['dodge_chance']
        self.soak_range = template['soak_range']
        self.template = template


class BasicDefenseProfile(DefenseProfile):
    pass


def attack_profile_create(token):

    template = attacktmpl.tmpl[token]
    classname = template['classname']
    the_class = globals()[classname]

    return the_class(token, template)


def defense_profile_create(token):

    template = defensetmpl.tmpl[token]
    classname = template['classname']
    the_class = globals()[classname]

    return the_class(token, template)
