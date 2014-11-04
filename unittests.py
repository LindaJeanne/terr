import unittest
import templates.templ as templ
import arena
import objects.creature as crea
import objects.player as pl
import objects.item as it
import gamemgr
import turnmgr


class TemplBlocksTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()
        self.blocks = templ.blockinfo

    def test_blockinfo_load(self):
        glassblock = self.blocks['BLOCK_GLASS']

        self.assertEqual(glassblock.token, 'BLOCK_GLASS')
        self.assertFalse(glassblock.template['is_walkable'])
        self.assertTrue(glassblock.template['is_transparent'])
        self.assertEqual(glassblock.glyph, 34)

    def teardown(self):
        pass


class TemplItemTests(unittest.TestCase):
    def setUp(self):

        templ.load_templates()
        self.pickaxe = templ.iteminfo['PICKAXE']

    def test_iteminfo_load(self):
        self.assertEqual(self.pickaxe.token, 'PICKAXE')
        self.assertEqual(self.pickaxe.glyph, 91)

    def teardown(self):
        templ.iteminfo = self.iteminfo_state


class TemplCreatureTests(unittest.TestCase):

    def setUp(self):

        templ.load_templates()
        self.fire_elemental = templ.creatureinfo['FIRE_ELEMENTAL']

    def test_creatureinfo_load(self):

        fe = templ.creatureinfo['FIRE_ELEMENTAL']

        self.assertEqual(fe.token, 'FIRE_ELEMENTAL')
        self.assertEqual(fe.glyph, 69)

    def teardown(self):
        pass


class ArenaTests(unittest.TestCase):

    def setUp(self):

        gamemgr.setup(
            arena.UnitTestArenaGenerator(),
            (20, 20))
        self.arena = gamemgr.the_arena

    def test_generate_2D_arena(self):

        wall_block = gamemgr.get_block((4, 4))
        floor_block = gamemgr.get_block((5, 5))

        self.assertEqual(wall_block.token, 'BLOCK_STONE')
        self.assertFalse(wall_block.detail.template['is_walkable'])
        self.assertFalse(wall_block.detail.template['is_transparent'])

        self.assertEqual(floor_block.token, 'FLOOR_STONE')
        self.assertTrue(floor_block.detail.template['is_walkable'])
        self.assertTrue(floor_block.detail.template['is_transparent'])

    def teardown(self):
        pass


class TemplateTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()

    def test_create_block(self):

        new_glass_block = arena.create_block(
            'BLOCK_GLASS', arena.Arena((10, 10)), (0, 0))

        self.assertTrue(new_glass_block)
        self.assertEqual(new_glass_block.token, 'BLOCK_GLASS')
        self.assertEqual(new_glass_block.glyph, 34)
        self.assertFalse(new_glass_block.detail.template['is_walkable'])
        self.assertTrue(new_glass_block.detail.template['is_transparent'])

    def test_create_creature(self):

        new_creature = crea.create(
            templ.creatureinfo['FIRE_ELEMENTAL'])

        self.assertTrue(new_creature)
        self.assertEqual(new_creature.token, 'FIRE_ELEMENTAL')
        self.assertEqual(new_creature.glyph, ord('E'))

    def test_create_player(self):

        new_player = pl.create(
            templ.playerclassinfo['PLAYER_DEFAULT'])

        self.assertTrue(new_player)
        self.assertEqual(new_player.token, 'PLAYER_DEFAULT')
        self.assertEqual(new_player.glyph, ord('@'))

    def test_create_item(self):

        new_item = it.create(
            templ.iteminfo['PICKAXE'])

        self.assertTrue(new_item)
        self.assertEqual(new_item.token, 'PICKAXE')
        self.assertEqual(new_item.glyph, ord('['))

    def teardown(self):
        pass


class GameManagerTests(unittest.TestCase):

    def setUp(self):

        gamemgr.setup(
            arena.UnitTestArenaGenerator(),
            (40, 40))

    def test_createArena(self):
        the_arena = gamemgr.the_arena

        wall_block = gamemgr.get_block((4, 4))
        floor_block = gamemgr.get_block((5, 5))

        self.assertTrue(the_arena)

        self.assertEqual(wall_block.token, 'BLOCK_STONE')
        self.assertFalse(wall_block.detail.template['is_walkable'])
        self.assertFalse(wall_block.detail.template['is_transparent'])

        self.assertEqual(floor_block.token, 'FLOOR_STONE')
        self.assertTrue(floor_block.detail.template['is_walkable'])
        self.assertTrue(floor_block.detail.template['is_transparent'])

    def test_not_adding_creature_to_invalide_location(self):

        #non-walkable tile
        self.assertFalse(gamemgr.new_creature('FIRE_ELEMENTAL', (4, 4)))

        #out-of-bounds tile
        self.assertFalse(gamemgr.new_creature('FIRE_ELEMENTAL', (85, 85)))

        #creature_already_present
        self.assertTrue(gamemgr.new_creature('RABBIT', (7, 7)))
        self.assertFalse(gamemgr.new_creature('FIRE_ELEMENTAL', (7, 7)))

    def test_add_creature(self):

        fire_elemental = gamemgr.new_creature('FIRE_ELEMENTAL', (5, 5))
        self.assertTrue(fire_elemental)

        the_tile = gamemgr.get_block((5, 5))
        self.assertTrue(the_tile.creature is fire_elemental)
        self.assertTrue(fire_elemental.block is the_tile)
        self.assertEqual(fire_elemental.location, (5, 5))
        self.assertEqual(fire_elemental.location, the_tile.location)
        self.assertTrue(
            fire_elemental in gamemgr.the_arena.creatureset)

    def test_not_adding_item_to_invalide_location(self):

        #non-walkable tile
        self.assertFalse(gamemgr.new_item('PICKAXE', (4, 4)))

        #out-of-bounds tile
        self.assertFalse(gamemgr.new_item('PICKAXE', (85, 85)))

    def test_add_single_item_to_tile(self):

        the_tile = gamemgr.get_block((5, 5))

        pickaxe = gamemgr.new_item('PICKAXE', (5, 5))

        self.assertTrue(pickaxe)
        self.assertTrue(pickaxe in gamemgr.the_arena.itemset)
        self.assertTrue(pickaxe.block is the_tile)
        self.assertTrue(pickaxe in the_tile.itemlist)
        self.assertEqual(pickaxe.location, (5, 5))
        self.assertEqual(pickaxe.location, the_tile.location)

    def test_add_multiple_items_to_tile(self):

        pickaxe = gamemgr.new_item('PICKAXE', (5, 5))
        apple = gamemgr.new_item('APPLE', (5, 5))

        the_tile = gamemgr.get_block((5, 5))

        self.assertTrue(pickaxe)
        self.assertTrue(pickaxe.block is the_tile)
        self.assertEqual(pickaxe.location, (5, 5))
        self.assertTrue(pickaxe in the_tile.itemlist)

        self.assertTrue(apple)
        self.assertTrue(apple.block is the_tile)
        self.assertEqual(apple.location, (5, 5))
        self.assertTrue(apple in the_tile.itemlist)

        self.assertEqual(apple.location, pickaxe.location)
        self.assertEqual(apple.location, the_tile.location)
        self.assertTrue(apple.block is pickaxe.block)

    def test_add_player(self):

        the_player = gamemgr.new_player('PLAYER_DEFAULT', (13, 13))

        self.assertTrue(the_player)
        self.assertTrue(
            gamemgr.the_arena.player is the_player)
        self.assertTrue(
            the_player.block is gamemgr.get_block((13, 13)))

    def teardown(self):
        pass


class TestTeleportItem(unittest.TestCase):

    def setUp(self):

        gamemgr.setup(
            arena.UnitTestArenaGenerator(),
            (40, 40))

        pickaxe = gamemgr.new_item('PICKAXE', (3, 3))
        pickaxeblock = gamemgr.get_block((3, 3))

        self.assertTrue(pickaxe)
        self.assertTrue(pickaxeblock)
        self.assertTrue(pickaxe in pickaxeblock.itemlist)
        self.assertTrue(pickaxe.block is pickaxeblock)

        self.pa = pickaxe

        apple = gamemgr.new_item('APPLE', (5, 5))
        appleblock = gamemgr.get_block((5, 5))

        self.assertTrue(apple)
        self.assertTrue(appleblock)
        self.assertTrue(apple in appleblock.itemlist)
        self.assertTrue(apple.block is appleblock)

        self.ap = apple

    def test_no_teleport_out_of_arena_bounds(self):
        self.assertFalse(self.pa.teleport((80, 80)))

    def test_no_teleport_inside_of_walls(self):
        self.assertFalse(self.pa.teleport((4, 4)))

    def test_teleport_item_to_empty_square(self):
        self.assertTrue(self.pa.teleport((9, 9)))
        self._validate_item(self.pa, (3, 3), (9, 9))

    def test_teleport_item_to_another_item(self):
        self.assertTrue(self.pa.teleport((5, 5)))
        self._validate_item(self.pa, (3, 3), (5, 5))
        self._validate_item(self.ap, (3, 3), (5, 5))

    def _validate_item(self, item, old_loc, new_loc):

        old_tile = gamemgr.get_block(old_loc)
        new_tile = gamemgr.get_block(new_loc)

        self.assertTrue(item.block is new_tile)
        self.assertTrue(item in new_tile.itemlist)
        self.assertFalse(item in old_tile.itemlist)
        self.assertEqual(item.location, new_loc)


class TestTeleportCreature(unittest.TestCase):

    def setUp(self):

        gamemgr.setup(
            arena.UnitTestArenaGenerator(),
            (40, 40))

        self.fe = gamemgr.new_creature('FIRE_ELEMENTAL', (9, 9))
        self.assertTrue(self.fe)

    def test_no_teleport_to_non_walkable_tile(self):
        self.assertFalse(self.fe.teleport((4, 4)))

    def test_no_teleport_to_outside_arena(self):
        self.assertFalse(self.fe.teleport((80, 80)))

    def test_no_teleport_onto_other_creature(self):

        #teleporting on top of another creature should not work
        rabbit = gamemgr.new_creature('RABBIT', (11, 11))
        self.assertTrue(rabbit)

        self.assertFalse(self.fe.teleport((11, 11)))

    def test_no_teleport_creature_that_wasnt_added(self):

        rabbit = crea.create(templ.creatureinfo['RABBIT'])
        self.assertTrue(rabbit)

        self.assertFalse(rabbit.teleport((19, 19)))

    def test_valid_creature_teleportation(self):

        #double-checking that the fire elemental is where we first put him
        self.assertTrue(
            gamemgr.the_arena.blockArray[(9, 9)].creature is self.fe)
        self.assertEqual(self.fe.location, (9, 9))

        #now to a teleport that should work
        self.assertTrue(self.fe.teleport((15, 15)))

        self.assertTrue(
            gamemgr.the_arena.blockArray[(15, 15)].creature is self.fe)

        self.assertFalse(gamemgr.the_arena.blockArray[(9, 9)].creature)

        self.assertEqual(self.fe.location, (15, 15))
        self.assertTrue(
            self.fe.block is gamemgr.the_arena.blockArray[(15, 15)])


class BlockGetGlyphTests(unittest.TestCase):

    def setUp(self):

        gamemgr.setup(
            arena.UnitTestArenaGenerator(),
            (40, 40))

        self.pl = gamemgr.new_player('PLAYER_DEFAULT', (5, 5))

        self.pa = gamemgr.new_item('PICKAXE', (7, 7))
        self.ap = gamemgr.new_item('APPLE', (7, 7))
        self.fe = gamemgr.new_creature('FIRE_ELEMENTAL', (7, 7))

        self.assertTrue(self.pl)
        self.assertTrue(self.pa)
        self.assertTrue(self.ap)
        self.assertTrue(self.fe)

    def test_empty_tile_gets_block_glyph(self):

        self.assertEqual(
            gamemgr.get_block((9, 9)).get_glyph(),
            ord('.'))

        self.assertEqual(
            gamemgr.get_block((10, 10)).get_glyph(),
            ord('#'))

    def test_items_no_creatre_gets_last_item_glyph(self):

        self.assertTrue(self.pa.teleport((11, 11)))
        self.assertTrue(self.ap.teleport((11, 11)))

        self.assertEqual(
            gamemgr.get_block((11, 11)).get_glyph(),
            ord('%'))

    def test_creature_and_items_gets_creature_glyph(self):

        self.assertTrue(self.pa.teleport((13, 13)))
        self.assertTrue(self.ap.teleport((13, 13)))

        self.assertTrue(self.fe.teleport((13, 13)))

        self.assertEqual(
            gamemgr.get_block((13, 13)).get_glyph(),
            ord('E'))

    def test_player_and_items_gets_player_glyph(self):

        self.assertTrue(self.pa.teleport((15, 15)))
        self.assertTrue(self.ap.teleport((15, 15)))
        self.assertTrue(self.pl.teleport((15, 15)))

        self.assertEqual(
            gamemgr.get_block((15, 15)).get_glyph(),
            ord('@'))


class TurnManagerTests(unittest.TestCase):

    def setUp(self):
        gamemgr.setup(
            arena.UnitTestArenaGenerator(),
            (40, 40))

        self.ngz = gamemgr.new_creature('NORTH_GOING_ZAX', (35, 35))
        self.other_ngz = gamemgr.new_creature('NORTH_GOING_ZAX', (37, 37))

        self.assertTrue(self.ngz)
        self.assertTrue(self.other_ngz)

        self.zaxlist = list()
        self.zaxlist.append(self.ngz)
        self.zaxlist.append(self.other_ngz)
        turnmgr.setup(self.zaxlist)

    def test_setup(self):

        self.assertTrue(gamemgr.the_arena)
        self.assertTrue(self.ngz)
        self.assertEqual(turnmgr._counter, 0)
        self.assertTrue(turnmgr._tickloop[turnmgr._counter] is self.zaxlist)

    def test_tick_loop(self):

        turnmgr.tick(gamemgr)
        self.assertEqual(self.ngz.location, (35, 34))
        self.assertEqual(self.other_ngz.location, (37, 36))

        self.assertEqual(turnmgr._counter, 1)
        self.assertEqual(turnmgr._tickloop[0], list())

        self.assertTrue(self.ngz in turnmgr._tickloop[10])
        self.assertTrue(self.other_ngz in turnmgr._tickloop[10])

        for i in range(0, 9):
            turnmgr.tick(gamemgr)

        self.assertEqual(turnmgr._counter, 10)
        self.assertEqual(self.ngz.location, (35, 34))
        self.assertEqual(self.other_ngz.location, (37, 36))

        turnmgr.tick(gamemgr)

        self.assertEqual(self.ngz.location, (35, 33))
        self.assertEqual(self.other_ngz.location, (37, 35))

        for i in range(0, 999):
            turnmgr.tick(gamemgr)

        self.assertEqual(turnmgr._counter, 10)
        self.assertEqual(self.ngz.location, (25, 12))
        self.assertEqual(self.other_ngz.location, (25, 14))

        turnmgr.tick(gamemgr)

        self.assertEqual(turnmgr._counter, 11)
        self.assertEqual(self.ngz.location, (25, 11))
        self.assertEqual(self.other_ngz.location, (25, 13))


if __name__ == '__main__':
    unittest.main()
