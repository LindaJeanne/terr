import gameobj as ob
import tmpl.itemtmpl as tp


class Item(ob.GameObj):

    def __init__(self, token, template, the_arena=None):
        super().__init__(token, template, the_arena)

        self.decay_profile = self._component(template['decay_profile'])
        self.throw_profile = self._component(template['throw_profile'])
        self.damage_profile = self._component(template['damage_profile'])
        self.treasure_profile = self._component(template['treasure_profile'])

    def _component(self, comp_tmpl):

        class_name = comp_tmpl['classname']
        args = comp_tmpl['args']
        the_class = globals()[class_name]
        return the_class(args)


class ConsumableItem(Item):

    def consume(self):
        pass


class FoodItem(ConsumableItem):
    pass


class PotionItem(ConsumableItem):
    pass


class EquipableItem(Item):

    def equip(self):
        pass

    def use(self):
        pass


class ItemComponentProfile(object):

    def __init__(self, args):
        pass


class ThrowableProfile(ItemComponentProfile):

    def throw(self):
        pass


class DecayableProfile(ItemComponentProfile):

    def decay(self):
        pass


class DamagableProfile(ItemComponentProfile):

    def damage(self):
        pass


class TreasureProfile(ItemComponentProfile):

    def value(self):
        return None


class NullItemProfile(
        ThrowableProfile,
        DecayableProfile,
        DamagableProfile,
        TreasureProfile):
    pass


def create_item(item_token, the_arena=None):

    item_template = tp.tmpl[item_token]
    class_name = item_template['classname']
    the_class = globals()[class_name]

    return the_class(item_token, item_template, the_arena)
