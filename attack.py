import tmpl.attacktmpl


def templ():
    return tmpl.attacktmpl


# ========================================================
# Attack profiles
# ========================================================


class AttackProfile(object):

    def __init__(self, token, template):
        self.token = token
        self.attacks = template['attacks']
        self.useWeaopon = template['useweapon']
        self.template = template


class BasicAttackProfile(AttackProfile):
    pass


# ========================================================
# Attack objects
# ========================================================


class Attack(object):
    def __init__(self, profile, which_attack):
        self.info = profile.which_attack
