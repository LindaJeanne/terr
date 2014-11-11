import tmpl.attacktmpl
import mixins


def templ():
    return tmpl.attacktmpl


# ========================================================
# Attack profiles
# ========================================================


class AttackProfile(mixins.IsTemplated):

    def __init__(self, token, template):
        super().__init__(token, template)
        self.attacks = template['attacks']
        self.useWeaopon = template['useweapon']


class BasicAttackProfile(AttackProfile):
    pass


# ========================================================
# Attack objects
# ========================================================


class Attack(object):
    def __init__(self, profile, which_attack):
        self.info = profile.which_attack
