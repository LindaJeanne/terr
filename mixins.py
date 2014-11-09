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
