import templ


def load_playerclasses():

    playerclassinfo = {
        'PLAYER_DEFAULT': templ.Template({
            'token': 'PLAYER_DEFAULT',
            'glyph': ord('@'),
            'objclass': 'Player'})}

    return playerclassinfo
