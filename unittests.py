import unittest
import templates.templ as templ
import objects.creature as crea
import objects.player as pl
import objects.item as it
import gamemgr
import turnmgr
import node
import gridgen
import arena


unit_test_arena = None


def setup():
    global unit_test_arena

    generator = gridgen.UnitTestGridGenerator()
    tokenarray = generator.create((40, 40))
    unit_test_arena = arena.Arena(tokenarray)


def clear_arena():

    global unit_test_arena

    itemset = set(unit_test_arena.itemset)
    for item in itemset:
        unit_test_arena.remove_item(item)

    creatureset = set(unit_test_arena.creatureset)
    for creature in creatureset:
        unit_test_arena.remove_creature(creature)


setup()


class ArenaTests(unittest.TestCase):

    def setUp(self):

        gamemgr.setup(
            gridgen.UnitTestGridGenerator(),
            (20, 20))
        self.arena = gamemgr.the_arena

    def test_generate_2D_arena(self):

        wall_block = gamemgr.get_block((4, 4))
        floor_block = gamemgr.get_block((5, 5))

        self.assertEqual(wall_block.token, 'BLOCK_STONE')
        self.assertFalse(wall_block.isPassable)
        self.assertFalse(wall_block.isPassable)

        self.assertEqual(floor_block.token, 'BLOCK_AIR')
        self.assertTrue(floor_block.isPassable)
        self.assertTrue(floor_block.isTransparent)

    def teardown(self):
        pass


class TemplateTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()

    def test_create_block(self):

        new_glass_block = node.Node('BLOCK_GLASS')

        self.assertTrue(new_glass_block)
        self.assertEqual(new_glass_block.token, 'BLOCK_GLASS')
        self.assertEqual(new_glass_block.glyph, 34)
        self.assertFalse(new_glass_block.isPassable)
        self.assertTrue(new_glass_block.isTransparent)

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
            gridgen.UnitTestGridGenerator(),
            (40, 40))

    def test_createArena(self):
        the_arena = gamemgr.the_arena

        wall_block = gamemgr.get_block((4, 4))
        floor_block = gamemgr.get_block((5, 5))

        self.assertTrue(the_arena)

        self.assertEqual(wall_block.token, 'BLOCK_STONE')
        self.assertFalse(wall_block.isPassable)
        self.assertFalse(wall_block.isTransparent)

        self.assertEqual(floor_block.token, 'BLOCK_AIR')
        self.assertTrue(floor_block.isPassable)
        self.assertTrue(floor_block.isTransparent)

    def test_not_adding_creature_to_invalide_location(self):

        # non-walkable tile
        self.assertRaises(
            Exception,
            gamemgr.new_creature,
            ('FIRE_ELEMENTAL', (4, 4)))

        # out-of-bounds tile
        self.assertRaises(
            Exception,
            gamemgr.new_creature,
            ('FIRE_ELEMENTAL', (85, 85)))

        # creature already present
        gamemgr.new_creature('RABBIT', (7, 7))
        self.assertRaises(
            Exception,
            gamemgr.new_creature,
            ('FIRE_ELEMENTAL', (4, 4)))

    def test_add_creature(self):

        fire_elemental = gamemgr.new_creature('FIRE_ELEMENTAL', (5, 5))
        self.assertTrue(fire_elemental)

        the_tile = gamemgr.get_block((5, 5))
        self.assertTrue(the_tile.creature is fire_elemental)
        self.assertTrue(fire_elemental.node is the_tile)
        self.assertTrue(
            fire_elemental in gamemgr.the_arena.creatureset)

    def test_not_adding_item_to_invalide_location(self):

        # non-walkable tile
        self.assertRaises(
            Exception,
            gamemgr.new_item,
            ('PICKAXE', (4, 4)))

        # out-of-bounds tile
        self.assertRaises(
            Exception,
            gamemgr.new_item,
            ('PICKAXE', (85, 85)))

    def test_add_single_item_to_tile(self):

        the_tile = gamemgr.get_block((5, 5))

        pickaxe = gamemgr.new_item('PICKAXE', (5, 5))

        self.assertTrue(pickaxe)
        self.assertTrue(pickaxe in gamemgr.the_arena.itemset)
        self.assertTrue(pickaxe.contain is the_tile)
        self.assertTrue(pickaxe in the_tile.itemlist)

    def test_add_multiple_items_to_tile(self):

        pickaxe = gamemgr.new_item('PICKAXE', (5, 5))
        apple = gamemgr.new_item('APPLE', (5, 5))

        the_tile = gamemgr.get_block((5, 5))

        self.assertTrue(pickaxe)
        self.assertTrue(pickaxe.contain is the_tile)
        self.assertTrue(pickaxe in the_tile.itemlist)

        self.assertTrue(apple)
        self.assertTrue(apple.contain is the_tile)
        self.assertTrue(apple in the_tile.itemlist)

        self.assertTrue(apple.contain is pickaxe.contain)

    def test_add_player(self):

        the_player = gamemgr.new_player('PLAYER_DEFAULT', (13, 13))

        self.assertTrue(the_player)
        self.assertTrue(
            gamemgr.the_arena.player is the_player)
        self.assertTrue(
            the_player.node is gamemgr.get_block((13, 13)))

    def teardown(self):
        pass


class TestTeleportItem(unittest.TestCase):

    def setUp(self):

        clear_arena()
        global unit_test_arena

        self.arena = unit_test_arena

        pickaxe = it.create(templ.iteminfo['PICKAXE'])
        self.arena.place_item(pickaxe, (3, 3))
        pickaxeblock = self.arena.grid[(3, 3)]

        self.assertTrue(pickaxe)
        self.assertTrue(pickaxeblock)
        self.assertTrue(pickaxe in pickaxeblock.itemlist)
        self.assertTrue(pickaxe.contain is pickaxeblock)

        self.pa = pickaxe

        apple = it.create(templ.iteminfo['APPLE'])
        self.arena.place_item(apple, (5, 5))
        appleblock = self.arena.grid[(5, 5)]

        self.assertTrue(apple)
        self.assertTrue(appleblock)
        self.assertTrue(apple in appleblock.itemlist)
        self.assertTrue(apple.contain is appleblock)

        self.ap = apple

    def test_no_teleport_out_of_arena_bounds(self):

        self.assertRaises(
            Exception,
            self.arena.place_item,
            (self.pa, (80, 80)))

    def test_no_teleport_inside_of_walls(self):

        self.assertRaises(
            Exception,
            self.arena.place_item,
            (self.pa, (4, 4)))

    def test_teleport_item_to_empty_square(self):

        self.arena.place_item(self.pa, (9, 9))
        self._validate_item(self.pa, (3, 3), (9, 9))

    def test_teleport_item_to_another_item(self):

        self.arena.place_item(self.pa, (5, 5))
        self._validate_item(self.pa, (3, 3), (5, 5))
        self._validate_item(self.ap, (3, 3), (5, 5))

    def _validate_item(self, item, old_loc, new_loc):

        old_tile = self.arena.grid[old_loc]
        new_tile = self.arena.grid[new_loc]

        self.assertTrue(item.contain is new_tile)
        self.assertTrue(item in new_tile.itemlist)
        self.assertFalse(item in old_tile.itemlist)


class TestTeleportCreature(unittest.TestCase):

    def setUp(self):

        clear_arena()
        global unit_test_arena

        self.arena = unit_test_arena
        self.fe = crea.create(templ.creatureinfo['FIRE_ELEMENTAL'])
        self.arena.place_creature(self.fe, (9, 9))
        self.assertTrue(self.fe)

    def test_no_teleport_to_non_walkable_tile(self):

        self.assertRaises(
            Exception,
            self.arena.place_creature,
            (self.fe, (4, 4)))

    def test_no_teleport_to_outside_arena(self):

        self.assertRaises(
            Exception,
            self.arena.place_creature,
            (self.fe, (80, 80)))

    def test_no_teleport_onto_other_creature(self):

        # teleporting on top of another creature should not work
        rabbit = crea.create(templ.creatureinfo['RABBIT'])
        self.arena.place_creature(rabbit, (11, 11))

        self.assertRaises(
            Exception,
            self.arena.place_creature,
            (self.fe, (11, 11)))

    def test_valid_creature_teleportation(self):

        # now to a teleport that should work
        self.arena.place_creature(self.fe, (15, 15))
        self.assertTrue(
            self.arena.grid[(15, 15)].creature is self.fe)

        self.assertFalse(self.arena.grid[(9, 9)].creature)

        self.assertTrue(
            self.fe.node is self.arena.grid[(15, 15)])


class BlockGetGlyphTests(unittest.TestCase):

    def setUp(self):

        clear_arena()
        global unit_test_arena
        self.arena = unit_test_arena

        self.pl = pl.create(templ.playerclassinfo['PLAYER_DEFAULT'])
        self.arena.place_creature(self.pl, (5, 5))

        self.pa = it.create(templ.iteminfo['PICKAXE'])
        self.arena.place_item(self.pa, (7, 7))

        self.ap = it.create(templ.iteminfo['APPLE'])
        self.arena.place_item(self.ap, (7, 7))

        self.fe = crea.create(templ.creatureinfo['FIRE_ELEMENTAL'])
        self.arena.place_creature(self.fe, (7, 7))

        self.assertTrue(self.pl)
        self.assertTrue(self.pa)
        self.assertTrue(self.ap)
        self.assertTrue(self.fe)

    def test_empty_tile_gets_block_glyph(self):

        self.assertEqual(
            self.arena.grid[(9, 9)].get_glyph(),
            ord('.'))

        self.assertEqual(
            self.arena.grid[(10, 10)].get_glyph(),
            ord('#'))

    def test_items_no_creatre_gets_last_item_glyph(self):

        self.arena.place_item(self.pa, (11, 11))
        self.arena.place_item(self.ap, (11, 11))

        self.assertEqual(
            self.arena.grid[(11, 11)].get_glyph(),
            ord('%'))

    def test_creature_and_items_gets_creature_glyph(self):

        self.arena.place_item(self.pa, (13, 13))
        self.arena.place_item(self.ap, (13, 13))
        self.arena.place_creature(self.fe, (13, 13))

        self.assertEqual(
            self.arena.grid[(13, 13)].get_glyph(),
            ord('E'))

    def test_player_and_items_gets_player_glyph(self):

        self.arena.place_item(self.pa, (15, 15))
        self.arena.place_item(self.ap, (15, 15))
        self.arena.place_creature(self.pl, (15, 15))

        self.assertEqual(
            self.arena.grid[(15, 15)].get_glyph(),
            ord('@'))


class TurnManagerTests(unittest.TestCase):

    def setUp(self):

        clear_arena()
        global unit_test_arena
        self.arena = unit_test_arena

        self.ngz = crea.create(templ.creatureinfo['NORTH_GOING_ZAX'])
        self.arena.place_creature(self.ngz, (35, 35))

        self.other_ngz = crea.create(templ.creatureinfo['NORTH_GOING_ZAX'])
        self.arena.place_creature(self.other_ngz, (37, 37))

        self.assertTrue(self.ngz)
        self.assertTrue(self.other_ngz)

        self.zaxlist = list()
        self.zaxlist.append(self.ngz)
        self.zaxlist.append(self.other_ngz)
        turnmgr.setup(self.zaxlist)

    def test_setup(self):

        self.assertTrue(self.arena)
        self.assertTrue(self.ngz)
        self.assertEqual(turnmgr._counter, 0)
        self.assertTrue(turnmgr._tickloop[turnmgr._counter] is self.zaxlist)

    def test_tick_loop(self):

        turnmgr.tick(gamemgr)
        self.assertEqual(self.ngz.node.location, (35, 34))
        self.assertEqual(self.other_ngz.node.location, (37, 36))

        self.assertEqual(turnmgr._counter, 1)
        self.assertEqual(turnmgr._tickloop[0], list())

        self.assertTrue(self.ngz in turnmgr._tickloop[10])
        self.assertTrue(self.other_ngz in turnmgr._tickloop[10])

        for i in range(0, 9):
            turnmgr.tick(gamemgr)

        self.assertEqual(turnmgr._counter, 10)
        self.assertEqual(self.ngz.node.location, (35, 34))
        self.assertEqual(self.other_ngz.node.location, (37, 36))

        turnmgr.tick(gamemgr)

        self.assertEqual(self.ngz.node.location, (35, 33))
        self.assertEqual(self.other_ngz.node.location, (37, 35))

        for i in range(0, 999):
            turnmgr.tick(gamemgr)

        self.assertEqual(turnmgr._counter, 10)
        self.assertEqual(self.ngz.node.location, (25, 12))
        self.assertEqual(self.other_ngz.node.location, (25, 14))

        turnmgr.tick(gamemgr)

        self.assertEqual(turnmgr._counter, 11)
        self.assertEqual(self.ngz.node.location, (25, 11))
        self.assertEqual(self.other_ngz.node.location, (25, 13))


if __name__ == '__main__':
    unittest.main()
