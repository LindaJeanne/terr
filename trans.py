ENGLISH_MSGS = {
    'CHOOSE_DIRECTION': "Pick a direction:",
    'TRY_AGAIN': "I didn't understand that response.",
    'CHOOSE_TARGET': "Move the cursor to choose a target:",
    'INVALID_TARGET': "That was not a valid target.",
    'A_WALL': "a wall"
}

ENGLISH_FORMATTED = {
    'YOU_BUMP_INTO': "Ouch! You bump into {var_one}."}


class Messages(object):

    def __init__(self, msgs, formatted):
        self.msgs = msgs
        self.formatted = formatted

    def get(self, key, var_one=None, var_two=None, var_three=None):

        if self._get_msgs(key):
            return self._get_msgs(key)
        else:
            return self._get_formatted(key, var_one, var_two, var_three)

    def _get_msgs(self, key):
        try:
            result = self.msgs[key]
        except Exception:
            result = None
        finally:
            return result

    def _get_formatted(self, key, var_one, var_two=None, var_three=None):

        try:
            result = self.formatted[key].format(
                var_one=var_one, var_two=var_two, var_three=var_three)
        except Exception:
            result = None
        finally:
            return result


msgs = Messages(ENGLISH_MSGS, ENGLISH_FORMATTED)
