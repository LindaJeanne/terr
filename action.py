import numpy as np

class Action(object):

    def __init__(self, actor, target=None, item=None):
        self.actor = actor
        self.target = target
        self.item = item

    def execute(self):
        return 0

    def on_fail(self):
        print("ACTION FAILED:", self)
        return 1


class NullAction(Action):

    def execute(self):
        return 10


class MovementAction(Action):

    def execute(self):
        target_block = self.actor.arena.grid[self.target]
        if target_block.add_actor(self.actor):
            return 10
        else:
            return self.on_fail()


class StepDirectionAction(MovementAction):

    def __init__(self, actor, direction_vector, item=None):

        destination = tuple(np.add(actor.container.location, direction_vector))
        super().__init__(actor, destination)

def create_action(classname, actor, target=None, item=None):
    the_class = globals()[classname]
    return the_class(actor, target, item)
