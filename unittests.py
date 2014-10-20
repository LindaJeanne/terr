import unittest
import templ
import arena
import gameobjects as go
import action


class TemplBlocksTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()
        generator = arena.UnitTestArenaGenerator()
        arena.setup(generator, (20, 20))
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
        generator = arena.UnitTestArenaGenerator()
        arena.setup(generator, (20, 20))
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
        generator = arena.UnitTestArenaGenerator()
        arena.setup(generator, (20, 20))

        self.fire_elemental = templ.creatureinfo['FIRE_ELEMENTAL']

    def test_creatureinfo_asTuple(self):
        self.assertEqual(
            self.fire_elemental.as_tuple(), (
                'FIRE_ELEMENTAL',
                69,
                'DefaultTurnHandler',
                {
                    'attack_handler': 'DefaultAttackHandler',
                    'defense_handler': 'DefaultDefenseHandler',
                    'hit': 10,
                    'damage': (5, 11),
                    'dodge': 8,
                    'soak': (4, 9)}))

    def test_creatureinfo_load(self):

        fe = templ.creatureinfo['FIRE_ELEMENTAL']

        self.assertEqual(fe.token, 'FIRE_ELEMENTAL')
        self.assertEqual(fe.char, 69)
        self.assertEqual(fe.turn_handler, 'DefaultTurnHandler')
        self.assertEqual(
            fe.combat_info['attack_handler'], 'DefaultAttackHandler')
        self.assertEqual(
            fe.combat_info['defense_handler'], 'DefaultDefenseHandler')
        self.assertEqual(fe.combat_info['hit'], 10)
        self.assertEqual(fe.combat_info['damage'], (5, 11))
        self.assertEqual(fe.combat_info['dodge'], 8)
        self.assertEqual(fe.combat_info['soak'], (4, 9))

    def teardown(self):
        pass


class ArenaTileTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates()
        generator = arena.UnitTestArenaGenerator()
        arena.setup(generator, (20, 20))

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

    def teardown(self):
        pass


class GameObjectTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates
        generator = arena.UnitTestArenaGenerator()
        arena.setup(generator, (20, 20))

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

        templ.load_templates()

        generator = arena.UnitTestArenaGenerator()
        arena.setup(generator, (20, 20))

        self.pickaxe = go.Item(templ.iteminfo['PICKAXE'])
        self.fire_elemental = go.Creature(templ.creatureinfo['FIRE_ELEMENTAL'])

    def test_generate_2D_arena(self):

        self.assertEqual(
            arena._tileArray[(4, 4)].block.token,
            'BLOCK_STONE')

        self.assertFalse(arena._tileArray[(4, 4)].block.isPassable)
        self.assertFalse(arena._tileArray[(4, 4)].block.isTransparent)

        self.assertEqual(
            arena._tileArray[(5, 5)].block.token,
            'FLOOR_STONE')

        self.assertTrue(arena._tileArray[(5, 5)].block.isPassable)
        self.assertTrue(arena._tileArray[(5, 5)].block.isTransparent)

    def test_add_item(self):

        valid_pickaxe = arena.create_item(
            templ.iteminfo['PICKAXE'], (7, 7))
        pickaxe_in_solid_wall = arena.create_item(
            templ.iteminfo['PICKAXE'], (6, 6))
        pickaxe_out_of_bounds = arena.create_item(
            templ.iteminfo['PICKAXE'], (22, 22))

        self.assertTrue(valid_pickaxe)
        self.assertFalse(pickaxe_in_solid_wall)
        self.assertFalse(pickaxe_out_of_bounds)

        self.assertTrue(valid_pickaxe in arena._itemSet)
        self.assertFalse(pickaxe_in_solid_wall in arena._itemSet)
        self.assertFalse(pickaxe_out_of_bounds in arena._itemSet)

        self.assertTrue(
            valid_pickaxe in arena._tileArray[(7, 7)].itemlist)

        self.assertEqual(len(arena._tileArray[(6, 6)].itemlist), 0)

        self.assertTrue(arena.destroy_item(valid_pickaxe))
        self.assertFalse(arena.destroy_item(pickaxe_in_solid_wall))
        self.assertFalse(arena.destroy_item(pickaxe_out_of_bounds))

    def test_teleport_item(self):

        teleporting_pickaxe = arena.create_item(
            templ.iteminfo['PICKAXE'], (9, 9))
        teleporting_apple = arena.create_item(
            templ.iteminfo['APPLE'], (9, 9))

        self.assertTrue(teleporting_pickaxe)
        self.assertTrue(teleporting_apple)

        self.assertTrue(arena.teleport_item(teleporting_pickaxe, (11, 11)))
        self.assertFalse(
            teleporting_pickaxe in arena._tileArray[(9, 9)].itemlist)
        self.assertTrue(
            teleporting_apple in arena._tileArray[(9, 9)].itemlist)

        self.assertTrue(
            teleporting_pickaxe in arena._tileArray[(11, 11)].itemlist)

        self.assertFalse(arena.teleport_item(teleporting_pickaxe, (23, 23)))

        self.assertFalse(arena.teleport_item(teleporting_pickaxe, (12, 12)))
        self.assertTrue(
            teleporting_pickaxe in arena._tileArray[(11, 11)].itemlist)
        self.assertFalse(
            teleporting_pickaxe in arena._tileArray[(12, 12)].itemlist)

        arena.destroy_item(teleporting_pickaxe)
        arena.destroy_item(teleporting_apple)

    def test_destroy_item(self):

        disappearing_pickaxe = arena.create_item(
            templ.iteminfo['PICKAXE'], (11, 11))

        self.assertTrue(disappearing_pickaxe in arena._itemSet)
        self.assertTrue(
            disappearing_pickaxe in arena._tileArray[(11, 11)].itemlist)

        self.assertTrue(arena.destroy_item(disappearing_pickaxe))
        self.assertFalse(disappearing_pickaxe in arena._itemSet)
        self.assertFalse(
            disappearing_pickaxe in arena._tileArray[(11, 11)].itemlist)

    def test_create_creature(self):

        valid_fire_elemental = arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (5, 5))
        fire_elemental_in_wall = arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (6, 6))
        fire_elemental_out_of_bounds = arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (23, 23))

        self.assertTrue(valid_fire_elemental)
        self.assertFalse(fire_elemental_in_wall)
        self.assertFalse(fire_elemental_out_of_bounds)

        self.assertTrue(valid_fire_elemental in arena._creatureSet)
        self.assertTrue(
            valid_fire_elemental is arena._tileArray[5, 5].creature)
        self.assertFalse(arena._tileArray[6, 6].creature)
        self.assertFalse(
            arena.create_creature('FIRE_ELEMENTAL', (5, 5)))

        arena.destroy_creature(valid_fire_elemental)

    def test_teleport_creature(self):

        fire_elemental = arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (3, 3))
        rabbit = arena.create_creature(
            templ.creatureinfo['RABBIT'], (5, 5))

        self.assertFalse(
            arena.teleport_creature(fire_elemental, (5, 5)))
        self.assertTrue(
            arena._tileArray[(5, 5)].creature is rabbit)
        self.assertTrue(
            arena._tileArray[(3, 3)].creature is fire_elemental)

        self.assertTrue(
            arena.teleport_creature(fire_elemental, (7, 7)))
        self.assertFalse(
            arena._tileArray[(3, 3)].creature)
        self.assertTrue(
            arena._tileArray[(7, 7)].creature is fire_elemental)

        arena.destroy_creature(fire_elemental)
        arena.destroy_creature(rabbit)

    def test_destroy_creature(self):
        fire_elemental = arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (5, 5))

        self.assertTrue(fire_elemental)
        self.assertTrue(fire_elemental in arena._creatureSet)
        self.assertTrue(
            fire_elemental is arena._tileArray[(5, 5)].creature)

        arena.destroy_creature(fire_elemental)
        self.assertFalse(fire_elemental in arena._creatureSet)
        self.assertFalse(arena._tileArray[(5, 5)].creature)

    def test_step_creature(self):

        fire_elemental = arena.create_creature(
            templ.creatureinfo['FIRE_ELEMENTAL'], (5, 19))
        self.assertTrue(fire_elemental)

        #south: out-of-range, shouldn't move.
        self.assertFalse(arena.step_creature(fire_elemental, arena.dir_south))
        self.assertTrue(arena._tileArray[(5, 19)].creature is fire_elemental)
        self.assertEqual(fire_elemental.location._coords, (5, 19))

        #this move should be legal.
        self.assertTrue(arena.step_creature(fire_elemental, arena.dir_north))
        self.assertTrue(arena._tileArray[(5, 18)].creature is fire_elemental)
        self.assertFalse(arena._tileArray[(5, 19)].creature)
        self.assertEqual(fire_elemental.location._coords, (5, 18))

        #walking into a wall shouldn't work.
        self.assertFalse(arena.step_creature(fire_elemental, arena.dir_east))
        self.assertEqual(fire_elemental.location._coords, (5, 18))
        self.assertTrue(arena._tileArray[(5, 18)].creature is fire_elemental)

        arena.destroy_creature(fire_elemental)

    def teardown(self):
        pass


class TurnHandlerTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_turn_handler_slow(self):

        turn_handler = action.DefaultTurnHandler()
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

        turn_handler = action.DefaultTurnHandler()
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
        arena.setup(generator, (20, 20))

        self.fe = arena.create_creature(
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
        arena.destroy_creature(self.fe)

if __name__ == '__main__':
    unittest.main()
