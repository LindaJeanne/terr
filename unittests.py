import unittest
import templ
import arena
import gameobjects as go
import numpy as np


class TemplBlocksTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()
        self.blocks = templ.blockinfo

    def test_blockinfo_asTuple(self):

        glassblock = self.blocks['BLOCK_GLASS']

        self.assertEqual(
            glassblock.as_tuple(),
            ('BLOCK_GLASS', False, True, 34))

    def test_blockinfo_load(self):
        glassblock = self.blocks['BLOCK_GLASS']

        self.assertEqual(glassblock.token, 'BLOCK_GLASS')
        self.assertFalse(glassblock.isPassable)
        self.assertTrue(glassblock.isTransparent)
        self.assertEqual(glassblock.char, 34)

    def teardown(self):
        pass


class TemplItemTests(unittest.TestCase):
    def setUp(self):

        templ.load_templates()
        self.pickaxe = templ.iteminfo['PICKAXE']

    def test_iteminfo_asTuple(self):
        self.assertEqual(
            self.pickaxe.as_tuple(),
            ('PICKAXE', 91))

    def test_iteminfo_load(self):
        self.assertEqual(self.pickaxe.token, 'PICKAXE')
        self.assertEqual(self.pickaxe.char, 91)

    def teardown(self):
        templ.iteminfo = self.iteminfo_state


class TemplCreatureTests(unittest.TestCase):

    def setUp(self):

        templ.load_templates()

        self.fire_elemental = templ.creatureinfo['FIRE_ELEMENTAL']

    def test_creatureinfo_asTuple(self):
        self.assertEqual(
            self.fire_elemental.as_tuple(),
            ('FIRE_ELEMENTAL', 69, 10, (5, 11), 8, (4, 9)))

    def test_creatureinfo_load(self):
        self.assertEqual(self.fire_elemental.token, 'FIRE_ELEMENTAL')
        self.assertEqual(self.fire_elemental.char, 69)
        self.assertEqual(self.fire_elemental.hit, 10)
        self.assertEqual(self.fire_elemental.damage, (5, 11))
        self.assertEqual(self.fire_elemental.dodge, 8)
        self.assertEqual(self.fire_elemental.soak, (4, 9))

    def teardown(self):
        pass


class ArenaTileTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()

        self.glassblock = templ.blockinfo['BLOCK_GLASS']
        self.stonefloor = templ.blockinfo['FLOOR_STONE']

        self.arenatile = arena.ArenaTile((0, 0), self.glassblock)
        self.floortile = arena.ArenaTile((0, 1), self.stonefloor)

    def test_create_arena_tile(self):
        self.assertEqual(
            self.arenatile.block.token,
            'BLOCK_GLASS')
        self.assertFalse(self.arenatile.creature)
        self.assertFalse(self.arenatile.itemlist)
        self.assertFalse(self.arenatile.block.isPassable)
        self.assertTrue(self.arenatile.block.isTransparent)
        self.assertEqual(
            self.arenatile.block.char,
            34)
        self.assertEqual(self.arenatile._coords[0], 0)
        self.assertEqual(self.arenatile._coords[1], 0)

    def test_add_remove_creature(self):
        fire_elemental = go.Creature(templ.creatureinfo['FIRE_ELEMENTAL'])

        self.assertTrue(self.floortile.add_creature(fire_elemental))
        self.assertEqual(self.floortile.creature, fire_elemental)
        self.assertFalse(self.floortile.add_creature(fire_elemental))

        rabbit = go.Creature(templ.creatureinfo['RABBIT'])

        self.assertFalse(self.floortile.add_creature(rabbit))
        self.assertEqual(self.floortile.creature, fire_elemental)
        self.assertTrue(self.floortile.rmv_creature())
        self.assertFalse(self.floortile.creature)
        self.assertTrue(self.floortile.add_creature(rabbit))
        self.assertEqual(self.floortile.creature, rabbit)
        self.assertTrue(self.floortile.rmv_creature())

    def test_add_remove_item(self):
        pickaxe = go.Item(templ.iteminfo['PICKAXE'])
        apple = go.Item(templ.iteminfo['APPLE'])

        self.assertFalse(self.floortile.itemlist)

        self.assertTrue(self.floortile.add_item(pickaxe))
        self.assertEqual(len(self.floortile.itemlist), 1)
        self.assertTrue(pickaxe in self.floortile.itemlist)

        self.assertTrue(self.floortile.add_item(apple))
        self.assertEqual(len(self.floortile.itemlist), 2)
        self.assertTrue(apple in self.floortile.itemlist)
        self.assertTrue(pickaxe in self.floortile.itemlist)

        self.assertTrue(self.floortile.rmv_item(pickaxe))
        self.assertEqual(len(self.floortile.itemlist), 1)
        self.assertFalse(pickaxe in self.floortile.itemlist)
        self.assertTrue(apple in self.floortile.itemlist)

        self.assertFalse(self.floortile.rmv_item(pickaxe))
        self.assertFalse(pickaxe in self.floortile.itemlist)
        self.assertTrue(apple in self.floortile.itemlist)

        self.assertTrue(self.floortile.rmv_item(apple))
        self.assertFalse(self.floortile.itemlist)

    def test_get_arena_tile_display_char(self):

        pickaxe = go.Item(templ.iteminfo['PICKAXE'])
        fire_elemental = go.Creature(templ.creatureinfo['FIRE_ELEMENTAL'])
        player = go.Player()

        self.assertEqual(self.floortile.get_display_char(), 46)

        self.assertTrue(self.floortile.add_item(pickaxe))
        self.assertEqual(self.floortile.get_display_char(), 91)

        self.assertTrue(self.floortile.add_creature(fire_elemental))
        self.assertEqual(self.floortile.get_display_char(), 69)

        self.floortile.rmv_creature()
        self.floortile.add_creature(player)
        self.assertEqual(self.floortile.get_display_char(), 64)

        self.floortile.rmv_item(pickaxe)
        self.floortile.rmv_creature()
        self.assertEqual(self.floortile.get_display_char(), 46)

    def teardown(self):
        pass


class GameObjectTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates

    def test_create_destroy_item(self):
        pickaxe = go.Item(templ.iteminfo['PICKAXE'])

        self.assertTrue(pickaxe)
        self.assertEqual(pickaxe.detail.char, 91)
        self.assertEqual(pickaxe.detail.token, 'PICKAXE')

    def test_create_destroy_creature(self):
        fire_elemental = go.Creature(templ.creatureinfo['FIRE_ELEMENTAL'])

        self.assertTrue(fire_elemental)
        self.assertEqual(fire_elemental.detail.char, 69)
        self.assertEqual(fire_elemental.detail.token, 'FIRE_ELEMENTAL')

    def test_create_player(self):
        player = go.Player()
        self.assertTrue(player)
        self.assertEqual(player.detail.char, 64)
        self.assertEqual(player.detail.token, 'PLAYER')

    def teardwon(self):
        pass


class ArenaTests(unittest.TestCase):

    def setUp(self):
        self.testarray = np.asanyarray(
            ((46, 46, 46, 46, 46),
             (46, 35, 35, 35, 46),
             (46, 46, 46, 46, 46),
             (46, 35, 35, 35, 46),
             (46, 46, 46, 46, 46)))

        template_array = np.asanyarray(
            (('FLOOR_STONE', 'FLOOR_STONE', 'FLOOR_STONE',
                'FLOOR_STONE', 'FLOOR_STONE'),
                ('FLOOR_STONE', 'BLOCK_STONE', 'BLOCK_STONE',
                    'BLOCK_STONE', 'FLOOR_STONE'),
                ('FLOOR_STONE', 'FLOOR_STONE', 'FLOOR_STONE',
                    'FLOOR_STONE', 'FLOOR_STONE'),
                ('FLOOR_STONE', 'BLOCK_STONE', 'BLOCK_STONE',
                    'BLOCK_STONE', 'FLOOR_STONE'),
                ('FLOOR_STONE', 'FLOOR_STONE', 'FLOOR_STONE',
                    'FLOOR_STONE', 'FLOOR_STONE')))

        templ.load_templates()
        blockinfo_dict = templ.blockinfo

        self.newarena = arena.Arena(template_array, blockinfo_dict)

        self.pickaxe = go.Item(templ.iteminfo['PICKAXE'])
        self.fire_elemental = go.Creature(templ.creatureinfo['FIRE_ELEMENTAL'])

    def test_generate_2D_arena(self):

        chararray = np.empty_like(self.newarena.tile_array)
        for i, v in np.ndenumerate(self.newarena.tile_array):
            chararray[i] = v.block.char
        self.assertTrue(np.equal(chararray, self.testarray).all())

    def test_add_teleport_destroy_item(self):

        self.newarena.add_item(self.pickaxe, (4, 4))
        self.assertTrue(
            self.pickaxe in self.newarena.tile_array[(4, 4)].itemlist)
        self.assertTrue(
            self.pickaxe.location is self.newarena.tile_array[(4, 4)])
        self.assertTrue(
            self.pickaxe in self.newarena.itemset)

        self.newarena.teleport_item(self.pickaxe, (2, 2))
        self.assertFalse(
            self.pickaxe in self.newarena.tile_array[(4, 4)].itemlist)
        self.assertTrue(
            self.pickaxe in self.newarena.tile_array[(2, 2)].itemlist)
        self.assertTrue(
            self.pickaxe.location is self.newarena.tile_array[(2, 2)])
        self.assertTrue(
            self.pickaxe in self.newarena.itemset)

        self.newarena.destroy_item(self.pickaxe)
        self.assertFalse(
            self.pickaxe in self.newarena.itemset)
        self.assertFalse(self.pickaxe.location)
        self.assertFalse(
            self.pickaxe in self.newarena.tile_array[(2, 2)].itemlist)
        self.assertFalse(
            self.pickaxe in self.newarena.tile_array[(4, 4)].itemlist)

    def test_add_teleport_destroy_creature(self):

        self.newarena.add_creature(self.fire_elemental, (4, 4))
        self.assertTrue(
            self.fire_elemental in self.newarena.creatureset)

        self.assertTrue(
            self.newarena.tile_array[(4, 4)].creature is self.fire_elemental)

        self.assertTrue(
            self.fire_elemental.location is self.newarena.tile_array[(4, 4)])

        self.newarena.teleport_creature(self.fire_elemental, (2, 2))
        self.assertTrue(
            self.fire_elemental in self.newarena.creatureset)
        self.assertFalse(
            self.newarena.tile_array[(4, 4)].creature is self.fire_elemental)
        self.assertTrue(
            self.newarena.tile_array[(2, 2)].creature is self.fire_elemental)
        self.assertTrue(
            self.fire_elemental.location is self.newarena.tile_array[(2, 2)])

        self.newarena.destroy_creature(self.fire_elemental)
        self.assertFalse(
            self.fire_elemental in self.newarena.creatureset)
        self.assertFalse(self.newarena.tile_array[(2, 2)].creature)
        self.assertFalse(self.fire_elemental.location)

    def test_step_creature(self):

        self.newarena.add_creature(self.fire_elemental, (4, 4))

        #out-of-range, shouldn't move
        self.assertFalse(
            self.newarena.step_creature(self.fire_elemental, arena.dir_south))
        self.assertEqual(self.fire_elemental.location._coords[0], 4)
        self.assertEqual(self.fire_elemental.location._coords[1], 4)

        #this move should be legal
        self.assertTrue(
            self.newarena.step_creature(self.fire_elemental, arena.dir_north))
        self.assertEqual(self.fire_elemental.location._coords[0], 4)
        self.assertEqual(self.fire_elemental.location._coords[1], 3)

        #This hits a wall, and therefore should not work.
        self.assertFalse(
            self.newarena.step_creature(self.fire_elemental, arena.dir_nw))
        self.assertEqual(self.fire_elemental.location._coords[0], 4)
        self.assertEqual(self.fire_elemental.location._coords[1], 3)

    def teardown(self):
        pass


class MainLoopTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_creature_speed_obj(self):
        pass

    def teardown(self):
        pass


if __name__ == '__main__':
    unittest.main()
