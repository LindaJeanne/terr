import collections as cn

blocks = dict()
floor_tiles = dict()

BlockInfo = cn.namedtuple('BlockInfo', 'token isPassable isTransparent char')
FloorInfo = cn.namedtuple('FloorInfo', 'token char')


def load_all():

    blocks['BLOCK_STONE'] = BlockInfo('BLOCK_STONE', False, False, ord("#"))
    blocks['BLOCK_AIR'] = BlockInfo('BLOCK_AIR', True, True, ord(' '))
    blocks['BLOCK_DUMMY'] = BlockInfo('BLOCK_DUMMY', True, True, ord('x'))

    floor_tiles['FLOOR_STONE'] = FloorInfo('FLOOR_STONE', ord('.'))
    floor_tiles['FLOOR_AIR'] = FloorInfo('FLOOR_AIR', ord(' '))
    floor_tiles['FLOOR_DUMMY'] = FloorInfo('FLOOR_DUMMY', ord('x'))
