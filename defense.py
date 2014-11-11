import tmpl.defensetmpl


def templ():
    return tmpl.defensetmpl


class DefenseProfile(object):

    def __init__(self, token, template):
        self.token = token
        self.dodge_chance = template['dodge_chance']
        self.soak_range = template['soak_range']
        self.template = template


class BasicDefenseProfile(DefenseProfile):
    pass
