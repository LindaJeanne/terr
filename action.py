import numpy as np
import display
import keymap


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

    def _ask(self, ask_msg):
        display.the_display.display_top_message(ask_msg)
        return display.the_display.wait_keypress()

    def _get_coords_from_dir(self, dir_vector):
        return tuple(np.add(self.actor.container.location, dir_vector))

    def _block_at(self, coords):
        return self.actor.arena.cell_at(coords)


class NullAction(Action):

    def execute(self):
        return 10


class MovementAction(Action):

    def execute(self):
        the_dest = self._block_at(self.target)
        if all((
                the_dest,
                the_dest.add_creature(self.actor))):
            return 10
        else:
            return self.on_fail()


class StepDirectionAction(MovementAction):

    def __init__(self, actor, direction_vector, item=None):
        super().__init__(actor, None, item)
        self.target = self._get_coords_from_dir(direction_vector)


class QuitAction(Action):

    def execute(self):
        raise SystemExit


class BuildAction(Action):

    def __init__(self, actor, target=None, item=None):
        super().__init__(self, actor, target, item)
        if not self.target:
            self.target = keymap.get_dir(
                self._ask("Build in which direction?"))

    def execute(self):
        pass


def create_action(classname, actor, target=None, item=None):
    the_class = globals()[classname]
    return the_class(actor, target, item)
