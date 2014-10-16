import unittest
import templ
import arena
import gameobjects as go
import numpy as np


class TemplModuleTests(unittest.TestCase):

    def setUp(self):
        self.blockinfo_state = templ.blockinfo
        self.iteminfo_state = templ.iteminfo
        self.creatureinfo_state = templ.creatureinfo

        templ.blockinfo = dict()
        templ.iteminfo = dict()
        templ.creatreinfo = dict()

        templ.loadBlockXML('blocks.xml')
        templ.loadItemXML('items.xml')
        templ.loadCreatureXML('creatures.xml')

        assert(templ.blockinfo)
        assert(templ.iteminfo)
        assert(templ.creatureinfo)

        self.glassblock = templ.blockinfo['BLOCK_GLASS']
        self.pickaxe = templ.iteminfo['PICKAXE']
        self.fire_elemental = templ.creatureinfo['FIRE_ELEMENTAL']

    def test_blockinfo_asTuple(self):

        self.assertEqual(
            self.glassblock.as_tuple(),
            ('BLOCK_GLASS', False, True, 34))

    def test_blockinfo_load(self):

        self.assertEqual(self.glassblock.token, 'BLOCK_GLASS')
        self.assertFalse(self.glassblock.isPassable)
        self.assertTrue(self.glassblock.isTransparent)
        self.assertEqual(self.glassblock.char, 34)

    def test_iteminfo_asTuple(self):
        self.assertEqual(
            self.pickaxe.as_tuple(),
            ('PICKAXE', 91))

    def test_iteminfo_load(self):
        self.assertEqual(self.pickaxe.token, 'PICKAXE')
        self.assertEqual(self.pickaxe.char, 91)

    def test_creatureinfo_asTuple(self):
        self.assertEqual(
            self.fire_elemental.as_tuple(),
            ('FIRE_ELEMENTAL', 69))

    def test_creatureinfo_load(self):
        self.assertEqual(self.fire_elemental.token, 'FIRE_ELEMENTAL')
        self.assertEqual(self.fire_elemental.char, 69)

    def teardown(self):
        templ.blockinfo = self.blockinfo_state
        templ.iteminfo = self.iteminfo_state
        templ.creatureinfo = self.creatureinfo_state


class ArenaTileTests(unittest.TestCase):

    def setUp(self):
        glassblock = templ.BlockDetails('BLOCK_GLASS', False, True, 34)
        stonefloor = templ.BlockDetails('STONE_FLOOR', True, True, 46)
        self.arenatile = arena.ArenaTile((0, 0), glassblock)
        self.floortile = arena.ArenaTile((0, 1), stonefloor)

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
        fire_elemental = go.Creature(
            templ.CreatureDetails('FIRE_ELEMENTAL', 69))

        self.assertTrue(self.floortile.add_creature(fire_elemental))
        self.assertEqual(self.floortile.creature, fire_elemental)
        self.assertFalse(self.floortile.add_creature(fire_elemental))

        rabbit = go.Creature(
            templ.CreatureDetails('RABBIT', 114))

        self.assertFalse(self.floortile.add_creature(rabbit))
        self.assertEqual(self.floortile.creature, fire_elemental)
        self.assertTrue(self.floortile.rmv_creature())
        self.assertFalse(self.floortile.creature)
        self.assertTrue(self.floortile.add_creature(rabbit))
        self.assertEqual(self.floortile.creature, rabbit)
        self.assertTrue(self.floortile.rmv_creature())

    def test_add_remove_item(self):
        pickaxe = go.Item(
            templ.ItemDetails('PICKAXE', 91))
        apple = go.Item(
            templ.ItemDetails('APPLE', 37))

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

        pickaxe = go.Item(templ.ItemDetails('PICKAXE', 91))
        fire_elemental = go.Creature(
            templ.CreatureDetails('FIRE_ELEMENTAL', 69))
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
        pass

    def test_create_destroy_item(self):
        pickaxe = go.Item(templ.ItemDetails('PICKAXE', 91))

        self.assertTrue(pickaxe)
        self.assertEqual(pickaxe.detail.char, 91)
        self.assertEqual(pickaxe.detail.token, 'PICKAXE')
        self.assertTrue(pickaxe in go.Item.index)
        pickaxe.destroy()
        self.assertFalse(pickaxe in go.Item.index)

    def test_create_destroy_creature(self):
        fire_elemental = go.Creature(
            templ.CreatureDetails('FIRE_ELEMENTAL', 69))

        self.assertTrue(fire_elemental)
        self.assertEqual(fire_elemental.detail.char, 69)
        self.assertEqual(fire_elemental.detail.token, 'FIRE_ELEMENTAL')
        self.assertTrue(fire_elemental in go.Creature.index)
        fire_elemental.destroy()
        self.assertFalse(fire_elemental in go.Creature.index)

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

    def test_generate_2D_arena(self):
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
        blockinfo_dict = dict([
            ('FLOOR_STONE',
                templ.BlockDetails(
                    'FLOOR_STONE', True, True, 46)),
            ('BLOCK_STONE',
                templ.BlockDetails(
                    'BLOCK_STONE', False, False, 35))])

        newarena = arena.Arena(template_array, blockinfo_dict)
        chararray = np.empty_like(newarena.tile_array)
        for i, v in np.ndenumerate(newarena.tile_array):
            chararray[i] = v.block.char
        self.assertTrue(np.equal(chararray, self.testarray).all())

    def teardown(self):
        pass


if __name__ == '__main__':
    unittest.main()
