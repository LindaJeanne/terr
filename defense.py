import tmpl.defensetmpl
import mixins


def templ():
    return tmpl.defensetmpl


class DefenseProfile(mixins.IsTemplated):

    def __init__(self, token, template):
        super().__init__(token, template)
        self.dodge_chance = template['dodge_chance']
        self.soak_range = template['soak_range']


class BasicDefenseProfile(DefenseProfile):
    pass
