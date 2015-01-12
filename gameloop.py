import numpy as np
import action
import arena
import display

player_commands = {
    ord('8'): ('StepDirectionAction', (0, -1), None),
    ord('9'): ('StepDirectionAction', (1, -1), None),
    ord('6'): ('StepDirectionAction', (1, 0), None),
    ord('3'): ('StepDirectionAction', (1, 1), None),
    ord('2'): ('StepDirectionAction', (0, 1), None),
    ord('1'): ('StepDirectionAction', (-1, 1), None),
    ord('4'): ('StepDirectionAction', (-1, 0), None),
    ord('7'): ('StepDirectionAction', (-1, -1), None),
    ord('q'): ('QuitAction', None, None)
}

class GameLoop(object):

    LOOP_SIZE = 10000
    DECAY_FREQ = 500

    def __init__(self, shape, generator_name, populator_name, display_name, player_token):

        self.the_arena = arena.generate_arena(generator_name, shape)
        self._populate_arena(populator_name, player_token)

        self.player_action = action.NullAction(self.the_player)
        self.last_actions = {}

        self.the_display = display.create_display(display_name)

        self.tickloop = np.empty(self.LOOP_SIZE, list)
        self.tickcount = 0
        self.decaycount = 0

        self.tickloop[1] = self.actor_list

    def _populate_arena(self, populator_name, player_token):

        the_lists = arena.populate_arena(populator_name, self.the_arena, player_token)
        self.actor_list = the_lists['actor_list']
        self.decay_list = the_lists['decay_list']

        self.the_player = self.the_arena.player
        if self.the_player not in self.actor_list:
            self.actor_list.append(self.the_player)

    def tick(self):

        self.tickcount = (self.tickcount + 1) % self.LOOP_SIZE
        self.decaycount = (self.decaycount + 1) % self.DECAY_FREQ

        if self.tickloop[self.tickcount]:
            self._do_tickloop()

        if self.decaycount == 0:
            self._do_decayloop()

    def _do_tickloop(self):
        self.current_actors = list(self.tickloop[self.tickcount])
        if self.the_player in self.current_actors:
            self.player_action = self.get_player_action()

        for actor in self.current_actors:
            try:
                self._do_actor_loop(actor)
            except SystemExit:
                self.end()

    def _do_actor_loop(self, actor):
            self.last_actions[actor] = actor.take_turn(self.player_action)
            turn_length = self.last_actions[actor].execute()
            self.advance_turn(actor, turn_length)

    def _do_decayloop(self):
        for item in self.decay_list:
            item.decayprofile.decay()



    def advance_turn(self, actor, turn_length):
        new_loc = (self.tickcount + turn_length) % self.LOOP_SIZE

        if not self.tickloop[new_loc]:
            self.tickloop[new_loc] = list()

        self.tickloop[new_loc].append(actor)
        self.tickloop[self.tickcount].remove(actor)


    def get_player_action(self):
        global player_commands

        the_char = self.the_display.wait_keypress()
        command_info = player_commands[the_char]

        return action.create_action(
            command_info[0],
            self.the_player,
            command_info[1],
            command_info[2])

    def end(self):
        self.the_display.end()
        raise SystemExit
