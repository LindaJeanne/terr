import tmpl.itemtmpl
import mixins


def templ():
    return tmpl.itemtmpl


class Item(mixins.IsTemplated):

    def __init__(self, token, itemdetails):
        super().__init__(token, itemdetails)
        self.glyph = itemdetails['glyph']
        self.arena = None
        self.contain = None

    def get_loc(self):

        return self.contain.get_loc()


class ItemVehicle(Item, mixins.CanMove):
    pass


class ItemTrap(Item, mixins.CanCombat):
    pass


class ItemContainer(Item, mixins.HasInventory):
    pass


class ItemActive(Item, mixins.HasTurn):
    pass
