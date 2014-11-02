import unittest
import templ
import arena
import gameobjects as go
import action


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
        self.assertEqual(fe.template['turn_handler'], 'DefaultTurnHandler')

        combat = fe.template['combat_info']
        self.assertEqual(
            combat['attack_handler'], 'DefaultAttackHandler')
        self.assertEqual(
            combat['defense_handler'], 'DefaultDefenseHandler')
        self.assertEqual(combat['hit'], 10)
        self.assertEqual(combat['damage'], (5, 11))
        self.assertEqual(combat['dodge'], 8)
        self.assertEqual(combat['soak'], (4, 9))

    def teardown(self):
        pass


class ArenaTileTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()
        generator = arena.UnitTestArenaGenerator()
        self.arena = generator.create((20, 20), templ.blockinfo)

        self.glassblock = templ.blockinfo['BLOCK_GLASS']
        self.stonefloor = templ.blockinfo['FLOOR_STONE']

        self.arenatile = arena.ArenaTile((0, 0), self.glassblock)
        self.floortile = arena.ArenaTile((0, 1), self.stonefloor)

    def test_create_arena_tile(self):
        self.assertEqual(
            self.arenatile.block['token'],
            'BLOCK_GLASS')
        self.assertFalse(self.arenatile.creature)
        self.assertFalse(self.arenatile.itemlist)
        self.assertFalse(self.arenatile.block['is_walkable'])
        self.assertTrue(self.arenatile.block['is_transparent'])
        self.assertEqual(
            self.arenatile.block['glyph'],
            34)
        self.assertEqual(self.arenatile._coords[0], 0)
        self.assertEqual(self.arenatile._coords[1], 0)

    def teardown(self):
        pass


class GameObjectTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates
        generator = arena.UnitTestArenaGenerator()
        self.the_arena = generator.create(
            shape=(20, 20), blockinfo=templ.blockinfo)

    def test_create_destroy_item(self):
        pickaxe = go.Item(templ.iteminfo['PICKAXE'], self.the_arena)

        self.assertTrue(pickaxe)
        self.assertEqual(pickaxe.detail.glyph, 91, self.the_arena)
        self.assertEqual(pickaxe.detail.token, 'PICKAXE')

    def test_create_destroy_creature(self):
        fire_elemental = go.Creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], self.the_arena)

        self.assertTrue(fire_elemental)
        self.assertEqual(fire_elemental.detail.glyph, 69)
        self.assertEqual(fire_elemental.detail.token, 'FIRE_ELEMENTAL')

    def test_create_player(self):
        player = go.Player(
            templ.playerclassinfo['PLAYER_DEFAULT'], self.the_arena)
        self.assertTrue(player)
        self.assertEqual(player.detail.glyph, 64)
        self.assertEqual(player.detail.token, 'PLAYER_DEFAULT')

    def teardwon(self):
        pass


class ArenaTests(unittest.TestCase):

    def setUp(self):

        templ.load_templates()

        generator = arena.UnitTestArenaGenerator()
        self.arena = generator.create((20, 20), templ.blockinfo)

        self.pickaxe = go.Item(templ.iteminfo['PICKAXE'], self.arena)
        self.fire_elemental = go.Creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], self.arena)

    def test_generate_2D_arena(self):

        self.assertEqual(
            self.arena._tileArray[(4, 4)].block['token'],
            'BLOCK_STONE')

        self.assertFalse(self.arena._tileArray[(4, 4)].block['is_walkable'])
        self.assertFalse(self.arena._tileArray[(4, 4)].block['is_transparent'])

        self.assertEqual(
            self.arena._tileArray[(5, 5)].block['token'],
            'FLOOR_STONE')

        self.assertTrue(self.arena._tileArray[(5, 5)].block['is_walkable'])
        self.assertTrue(self.arena._tileArray[(5, 5)].block['is_transparent'])

    def test_add_item(self):

        valid_pickaxe = self.arena.create_item(
            templ.iteminfo['PICKAXE'], (7, 7))
        pickaxe_in_solid_wall = self.arena.create_item(
            templ.iteminfo['PICKAXE'], (6, 6))
        pickaxe_out_of_bounds = self.arena.create_item(
            templ.iteminfo['PICKAXE'], (22, 22))

        self.assertTrue(valid_pickaxe)
        self.assertFalse(pickaxe_in_solid_wall)
        self.assertFalse(pickaxe_out_of_bounds)

        self.assertTrue(valid_pickaxe in self.arena._itemSet)
        self.assertFalse(pickaxe_in_solid_wall in self.arena._itemSet)
        self.assertFalse(pickaxe_out_of_bounds in self.arena._itemSet)

        self.assertTrue(
            valid_pickaxe in self.arena._tileArray[(7, 7)].itemlist)

        self.assertEqual(len(self.arena._tileArray[(6, 6)].itemlist), 0)

        self.assertTrue(self.arena.destroy_item(valid_pickaxe))
        self.assertFalse(self.arena.destroy_item(pickaxe_in_solid_wall))
        self.assertFalse(self.arena.destroy_item(pickaxe_out_of_bounds))

    def test_teleport_item(self):

        teleporting_pickaxe = self.arena.create_item(
            templ.iteminfo['PICKAXE'], (9, 9))
        teleporting_apple = self.arena.create_item(
            templ.iteminfo['APPLE'], (9, 9))

        self.assertTrue(teleporting_pickaxe)
        self.assertTrue(teleporting_apple)

        self.assertTrue(self.arena.teleport_item(
            teleporting_pickaxe, (11, 11)))
        self.assertFalse(
            teleporting_pickaxe in self.arena._tileArray[(9, 9)].itemlist)
        self.assertTrue(
            teleporting_apple in self.arena._tileArray[(9, 9)].itemlist)

        self.assertTrue(
            teleporting_pickaxe in self.arena._tileArray[(11, 11)].itemlist)

        self.assertFalse(self.arena.teleport_item(
            teleporting_pickaxe, (23, 23)))

        self.assertFalse(self.arena.teleport_item(
            teleporting_pickaxe, (12, 12)))
        self.assertTrue(
            teleporting_pickaxe in self.arena._tileArray[(11, 11)].itemlist)
        self.assertFalse(
            teleporting_pickaxe in self.arena._tileArray[(12, 12)].itemlist)

        self.arena.destroy_item(teleporting_pickaxe)
        self.arena.destroy_item(teleporting_apple)

    def test_destroy_item(self):

        disappearing_pickaxe = self.arena.create_item(
            templ.iteminfo['PICKAXE'], (11, 11))

        self.assertTrue(disappearing_pickaxe in self.arena._itemSet)
        self.assertTrue(
            disappearing_pickaxe in self.arena._tileArray[(11, 11)].itemlist)

        self.assertTrue(self.arena.destroy_item(disappearing_pickaxe))
        self.assertFalse(disappearing_pickaxe in self.arena._itemSet)
        self.assertFalse(
            disappearing_pickaxe in self.arena._tileArray[(11, 11)].itemlist)

    def test_create_creature(self):

        valid_fire_elemental = self.arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (5, 5))
        fire_elemental_in_wall = self.arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (6, 6))
        fire_elemental_out_of_bounds = self.arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (23, 23))

        self.assertTrue(valid_fire_elemental)
        self.assertFalse(fire_elemental_in_wall)
        self.assertFalse(fire_elemental_out_of_bounds)

        self.assertTrue(valid_fire_elemental in self.arena._creatureSet)
        self.assertTrue(
            valid_fire_elemental is self.arena._tileArray[5, 5].creature)
        self.assertFalse(self.arena._tileArray[6, 6].creature)
        self.assertFalse(
            self.arena.create_creature('FIRE_ELEMENTAL', (5, 5)))

        self.arena.destroy_creature(valid_fire_elemental)

    def test_teleport_creature(self):

        fire_elemental = self.arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (3, 3))
        rabbit = self.arena.create_creature(
            templ.creatureinfo['RABBIT'], (5, 5))

        self.assertFalse(
            self.arena.teleport_creature(fire_elemental, (5, 5)))
        self.assertTrue(
            self.arena._tileArray[(5, 5)].creature is rabbit)
        self.assertTrue(
            self.arena._tileArray[(3, 3)].creature is fire_elemental)

        self.assertTrue(
            self.arena.teleport_creature(fire_elemental, (7, 7)))
        self.assertFalse(
            self.arena._tileArray[(3, 3)].creature)
        self.assertTrue(
            self.arena._tileArray[(7, 7)].creature is fire_elemental)

        self.arena.destroy_creature(fire_elemental)
        self.arena.destroy_creature(rabbit)

    def test_destroy_creature(self):
        fire_elemental = self.arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (5, 5))

        self.assertTrue(fire_elemental)
        self.assertTrue(fire_elemental in self.arena._creatureSet)
        self.assertTrue(
            fire_elemental is self.arena._tileArray[(5, 5)].creature)

        self.arena.destroy_creature(fire_elemental)
        self.assertFalse(fire_elemental in self.arena._creatureSet)
        self.assertFalse(self.arena._tileArray[(5, 5)].creature)

    def test_step_creature(self):

        fire_elemental = self.arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (5, 19))
        self.assertTrue(fire_elemental)

        #south: out-of-range, shouldn't move.
        self.assertFalse(self.arena.step_creature(
            fire_elemental, arena.dir_south))
        self.assertTrue(
            self.arena._tileArray[(5, 19)].creature is fire_elemental)
        self.assertEqual(fire_elemental.location._coords, (5, 19))

        #this move should be legal.
        self.assertTrue(self.arena.step_creature(
            fire_elemental, arena.dir_north))
        self.assertTrue(
            self.arena._tileArray[(5, 18)].creature is fire_elemental)
        self.assertFalse(self.arena._tileArray[(5, 19)].creature)
        self.assertEqual(fire_elemental.location._coords, (5, 18))

        #walking into a wall shouldn't work.
        self.assertFalse(
            self.arena.step_creature(fire_elemental, arena.dir_east))
        self.assertEqual(fire_elemental.location._coords, (5, 18))
        self.assertTrue(
            self.arena._tileArray[(5, 18)].creature is fire_elemental)

        self.arena.destroy_creature(fire_elemental)

    def teardown(self):
        pass


class TurnHandlerTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_turn_handler_slow(self):

        turn_handler = action.DefaultTurnHandler(None)
        self.assertFalse(turn_handler._skip)
        self.assertFalse(turn_handler._extra)
        self.assertEqual(turn_handler._mode, 'NORMAL')

        for i in range(0, 10):
            turn_handler.next()
            self.assertFalse(turn_handler._skip)
            self.assertFalse(turn_handler._extra)

        turn_handler.slow(4, 20)

        for i in range(0, 5):
            self.assertTrue(turn_handler._skip)
            self.assertFalse(turn_handler._extra)
            self.assertEqual(turn_handler._mode, 'SLOW')
            turn_handler.next()

            for j in range(0, 3):
                self.assertFalse(turn_handler._skip)
                self.assertFalse(turn_handler._extra)
                self.assertEqual(turn_handler._mode, 'SLOW')
                turn_handler.next()

        turn_handler.slow(3, 20)
        self.assertEqual(turn_handler._mode, 'SLOW')
        turn_handler.fast(5, 30)
        self.assertEqual(turn_handler._mode, 'NORMAL')

    def test_turn_handler_fast(self):

        turn_handler = action.DefaultTurnHandler(None)
        self.assertFalse(turn_handler._skip)
        self.assertFalse(turn_handler._extra)
        self.assertEqual(turn_handler._mode, 'NORMAL')

        for i in range(0, 10):
            turn_handler.next()
            self.assertFalse(turn_handler._skip)
            self.assertFalse(turn_handler._extra)

        turn_handler.fast(4, 20)

        for i in range(0, 5):

            self.assertFalse(turn_handler._skip)
            self.assertTrue(turn_handler._extra)
            self.assertEqual(turn_handler._mode, 'FAST')
            turn_handler.next()

            for j in range(0, 3):
                self.assertFalse(turn_handler._skip)
                self.assertFalse(turn_handler._extra)
                self.assertEqual(turn_handler._mode, 'FAST')
                turn_handler.next()

        turn_handler.fast(3, 20)
        self.assertEqual(turn_handler._mode, 'FAST')
        turn_handler.slow(5, 30)
        self.assertEqual(turn_handler._mode, 'NORMAL')

    def teardown(self):
        pass


class ActionHandlerTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()
        generator = arena.UnitTestArenaGenerator()
        self.arena = generator.create((20, 20), templ.blockinfo)

        self.fe = self.arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'],
            (5, 5))

    def test_turn_handler(self):

        turn_handler = self.fe.turn_handler

        self.assertTrue(isinstance(
            turn_handler, action.TurnHandler))
        self.assertTrue(isinstance(
            turn_handler, action.DefaultTurnHandler))

    def test_attack_handler(self):

        attack_handler = self.fe.attack_handler

        self.assertTrue(isinstance(
            attack_handler, action.AttackHandler))
        self.assertTrue(isinstance(
            attack_handler, action.DefaultAttackHandler))
        self.assertEqual(
            attack_handler.hit, 10)
        self.assertEqual(
            attack_handler.damage, (5, 11))

    def test_defence_handler(self):

        defense_handler = self.fe.defense_handler

        self.assertTrue(isinstance(
            defense_handler, action.DefenseHandler))
        self.assertTrue(isinstance(
            defense_handler, action.DefaultDefenseHandler))
        self.assertEqual(
            defense_handler.dodge, 8)
        self.assertEqual(
            defense_handler.soak, (4, 9))

    def teardown(self):
        self.arena.destroy_creature(self.fe)

#=========================================================================
# new tests begin here
#=========================================================================


class TemplateTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()

    def test_create_block(self):

        new_glass_block = templ.blockinfo['BLOCK_GLASS'].create()

        self.assertTrue(new_glass_block)
        self.assertEqual(new_glass_block.token, 'BLOCK_GLASS')
        self.assertEqual(new_glass_block.glyph, 34)
        self.assertFalse(new_glass_block.detail.template['is_walkable'])
        self.assertTrue(new_glass_block.detail.template['is_transparent'])

    def test_create_creature(self):

        new_creature = templ.creatureinfo['FIRE_ELEMENTAL'].create()

        self.assertTrue(new_creature)
        self.assertEqual(new_creature.token, 'FIRE_ELEMENTAL')
        self.assertEqual(new_creature.glyph, ord('E'))
        self.assertTrue(new_creature.attack_handler)
        self.assertTrue(new_creature.defense_handler)
        self.assertTrue(new_creature.turn_handler)

    def test_create_player(self):

        new_player = templ.playerclassinfo['PLAYER_DEFAULT'].create()

        self.assertTrue(new_player)
        self.assertEqual(new_player.token, 'PLAYER_DEFAULT')
        self.assertEqual(new_player.glyph, ord('@'))
        self.assertTrue(new_player.turn_handler)
        self.assertTrue(new_player.attack_handler)
        self.assertTrue(new_player.defense_handler)

    def test_create_item(self):

        new_item = templ.iteminfo['PICKAXE'].create()

        self.assertTrue(new_item)
        self.assertEqual(new_item.token, 'PICKAXE')
        self.assertEqual(new_item.glyph, ord('['))

    def teardown(self):
        pass

if __name__ == '__main__':
    unittest.main()
