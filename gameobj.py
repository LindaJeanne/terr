class GameObj(object):

    def __init__(self, token, template, the_arena=None):
        self.token = token
        self.template = template
        self.tileinfo = template['tileinfo']
        self.container = None
        self.arena = the_arena
