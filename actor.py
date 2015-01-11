import gameobj as ob
import tmpl.actortmpl as tp
import action

class Actor(ob.GameObj):

    def __init__(self, token, template, the_arena=None):
        super().__init__(token, template, the_arena)

        self.movement_profile = self._component(template['movement_profile'])
        self.attack_profile = self._component(template['attack_profile'])
        self.defense_profile = self._component(template['defense_profile'])
        self.magic_profile = self._component(template['magic_profile'])
        self.equip_profile = self._component(template['equip_profile'])

    def _component(self, comp_tmpl):

        class_name = comp_tmpl['classname']
        args = comp_tmpl['args']
        the_class = globals()[class_name]
        return the_class(args)

    def take_turn(self, player_action):
        return action.NullAction(self)


class AiCreature(Actor):
    pass


class Player(Actor):
    def take_turn(self, player_action):
        return player_action


class ActorComponentProfile(object):

    def __init__(self, args):
        pass


class MovementProfile(ActorComponentProfile):

    def get_nav_graph(self):
        return None

    def is_step_legal(self, direction):
        return False

    def is_space_legal(self, coords):
        return False


class WalkerProfile(MovementProfile):
    ''' For creatures who's only transportation is to walk. '''


class AttackProfile(ActorComponentProfile):
    pass


class DefenseProfile(ActorComponentProfile):
    pass


class MagicProfile(ActorComponentProfile):
    pass


class EquipmentProfile(ActorComponentProfile):
    pass


class NullActorProfile(
        MovementProfile,
        AttackProfile,
        DefenseProfile,
        MagicProfile,
        EquipmentProfile):
    pass


def create_actor(token, the_arena=None):

    template = tp.tmpl[token]
    class_name = template['classname']
    the_class = globals()[class_name]
    return the_class(token, template, the_arena)
