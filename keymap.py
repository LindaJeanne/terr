player_commands = {
    ord('8'): ('StepDirectionAction', (0, -1), None),
    ord('9'): ('StepDirectionAction', (1, -1), None),
    ord('6'): ('StepDirectionAction', (1, 0), None),
    ord('3'): ('StepDirectionAction', (1, 1), None),
    ord('2'): ('StepDirectionAction', (0, 1), None),
    ord('1'): ('StepDirectionAction', (-1, 1), None),
    ord('4'): ('StepDirectionAction', (-1, 0), None),
    ord('7'): ('StepDirectionAction', (-1, -1), None),
    ord('q'): ('QuitAction', None, None),
    ord('b'): ('BuildAction', None, None)
}


def get_dir(the_key):
    the_command = player_commands[the_key]
    the_direction = the_command[1]
    return the_direction
