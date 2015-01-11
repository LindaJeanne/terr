tmpl = {
    'NULL_CREATURE': {
        'classname': 'AiCreature',
        'displayname': 'Null creature',
        'description': 'For testing purposes; a creature that doesnt do anything.',
        'tileinfo':
            {
                'ascii_code': 78,
                'utf8_code': 'TODO',
                'image16': 'TODO',
                'image32': 'TODO',
                'image64': 'TODO',
                'image_vector': 'TODO',
                'curses_colorpair': 1,
                'foreground_color': 'TODO',
                'background_color': 'TODO'
            },
        'movement_profile':
            {
                'classname': 'NullActorProfile',
                'args': None
            },
        'attack_profile':
            {
                'classname': 'NullActorProfile',
                'args': None
            },
        'defense_profile':
            {
                'classname': 'NullActorProfile',
                'args': None
            },
        'magic_profile':
            {
                'classname': 'NullActorProfile',
                'args': None
            },
        'equip_profile':
            {
                'classname': 'NullActorProfile',
                'args': None
            }
    },
    'UNIT_TEST_PLAYER': {
        'classname': 'Player',
        'displayname': 'The Player',
        'description': 'A computer controlled player to use in unit tests.',
        'tileinfo':
            {
                'ascii_code': 64,
                'utf8_code': 'TODO',
                'image16': 'TODO',
                'image32': 'TODO',
                'image64': 'TODO',
                'image_vector': 'TODO',
                'curses_colorpair': 1,
                'foreground_color': 'TODO',
                'background_color': 'TODO'
            },
        'movement_profile':
            {
                'classname': 'WalkerProfile',
                'args': None
            },
        'attack_profile':
            {
                'classname': 'NullActorProfile',
                'args': None
            },
        'defense_profile':
            {
                'classname': 'NullActorProfile',
                'args': None
            },
        'magic_profile':
            {
                'classname': 'NullActorProfile',
                'args': None
            },
        'equip_profile':
            {
                'classname': 'NullActorProfile',
                'args': None
            }
    }
}
