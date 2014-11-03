import unittest
import templ
import arena
import gameobjects as go
import action
import gamemgr


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


#class ArenaTileTests(unittest.TestCase):

#    def setUp(self):
#        templ.load_templates()
#        generator = arena.UnitTestArenaGenerator()
#        self.arena = generator.create((20, 20), templ.blockinfo)

#        self.glassblock = templ.blockinfo['BLOCK_GLASS']
#        self.stonefloor = templ.blockinfo['FLOOR_STONE']

#        self.arenatile = arena.ArenaTile((0, 0), self.glassblock)
#        self.floortile = arena.ArenaTile((0, 1), self.stonefloor)

#    def test_create_arena_tile(self):
#        self.assertEqual(
#            self.arenatile.block['token'],
#            'BLOCK_GLASS')
#        self.assertFalse(self.arenatile.creature)
#        self.assertFalse(self.arenatile.itemlist)
#        self.assertFalse(self.arenatile.block['is_walkable'])
#        self.assertTrue(self.arenatile.block['is_transparent'])
#        self.assertEqual(
#            self.arenatile.block['glyph'],
#            34)
#        self.assertEqual(self.arenatile._coords[0], 0)
#        self.assertEqual(self.arenatile._coords[1], 0)

#    def teardown(self):
#        pass


class GameObjectTests(unittest.TestCase):

    def setUp(self):
        templ.load_templates
        generator = arena.UnitTestArenaGenerator()
        self.the_arena = generator.create(
            shape=(20, 20), blockinfo=templ.blockinfo)

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

    #def test_step_creature(self):

    #    the_tile = gamemgr.get_block(5, 19)

    #    fire_elemental = templ.creatureinfo['FIRE_ELEMENTAL'].create()
    #    gamemgr.add_creature(fire_elemental, (5, 19))
    #    self.assertTrue(fire_elemental)

    #    #south: out-of-range, shouldn't move.
    #    self.assertFalse(self.arena.step_creature(
    #        fire_elemental, arena.dir_south))
    #    self.assertTrue(
    #        self.arena._tileArray[(5, 19)].creature is fire_elemental)
    #    self.assertEqual(fire_elemental.tile._coords, (5, 19))

    #    #this move should be legal.
    #    self.assertTrue(self.arena.step_creature(
    #        fire_elemental, arena.dir_north))
    #    self.assertTrue(
    #        self.arena._tileArray[(5, 18)].creature is fire_elemental)
    #    self.assertFalse(self.arena._tileArray[(5, 19)].creature)
    #    self.assertEqual(fire_elemental.tile._coords, (5, 18))

    #    #walking into a wall shouldn't work.
    #    self.assertFalse(
    #        self.arena.step_creature(fire_elemental, arena.dir_east))
    #    self.assertEqual(fire_elemental.tile._coords, (5, 18))
    #    self.assertTrue(
    #        self.arena._tileArray[(5, 18)].creature is fire_elemental)

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

        gamemgr.setup(
            arena.UnitTestArenaGenerator(),
            (20, 20))

        self.arena = gamemgr.the_arena

        self.fe = templ.creatureinfo['FIRE_ELEMENTAL'].create()
        gamemgr.add_creature(self.fe, (5, 5))

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

    def test_add_creature(self):

        fire_elemental = templ.creatureinfo['FIRE_ELEMENTAL'].create()

        #adding to non-walkable tile should fail
        was_successful = gamemgr.add_creature(fire_elemental, (4, 4))
        self.assertFalse(was_successful)

        #adding to an out-of-bounds tile should fail
        self.assertFalse(gamemgr.add_creature(fire_elemental, (85, 85)))

        #adding to a valid tile should succeed
        self.assertTrue(gamemgr.add_creature(fire_elemental, (5, 5)))

        valid_tile = gamemgr.get_block((5, 5))

        self.assertTrue(valid_tile.creature is fire_elemental)
        self.assertEqual(fire_elemental.location, valid_tile.location)
        self.assertTrue(fire_elemental.block is valid_tile)

        #adding a creature that's already been added should fail
        self.assertFalse(gamemgr.add_creature(fire_elemental, (7, 7)))

        #adding a creature to a tile that already has a creature
        # shoudl fail
        rabbit = templ.creatureinfo['RABBIT'].create()
        self.assertFalse(gamemgr.add_creature(rabbit, (5, 5)))

    def test_not_adding_item_to_invalide_location(self):

        pickaxe = templ.iteminfo['PICKAXE'].create()

        #adding to non-walkable tile should fail
        self.assertFalse(gamemgr.add_item(pickaxe, (4, 4)))

        #adding to an out-of-bounds tile should fail
        self.assertFalse(gamemgr.add_item(pickaxe, (85, 85)))

    def test_add_item(self):

        pickaxe = templ.iteminfo['PICKAXE'].create()

        the_tile = gamemgr.get_block((5, 5))

        #adding to a valid tile should succeed
        self.assertTrue(gamemgr.add_item(pickaxe, (5, 5)))

        self.assertTrue(pickaxe in gamemgr.the_arena.itemset)
        self.assertEqual(pickaxe.location, the_tile.location)
        self.assertTrue(pickaxe.block is the_tile)
        self.assertEqual(pickaxe.location, (5, 5))
        self.assertTrue(pickaxe in the_tile.itemlist)

        #adding an item that's already been added should fail
        self.assertFalse(gamemgr.add_item(pickaxe, (7, 7)))

        #should be able to have more than one item on a tile
        apple = templ.iteminfo['APPLE'].create()
        self.assertTrue(gamemgr.add_item(apple, (5, 5)))

        self.assertTrue(apple in the_tile.itemlist)
        self.assertTrue(pickaxe in the_tile.itemlist)
        self.assertTrue(apple in gamemgr.the_arena.itemset)
        self.assertTrue(apple.block is pickaxe.block)
        self.assertTrue(apple.block is the_tile)
        self.assertEqual(apple.location, pickaxe.location)

    def test_add_player(self):

        the_player = templ.playerclassinfo['PLAYER_DEFAULT'].create()

        self.assertTrue(gamemgr.add_player(the_player, (13, 13)))

        self.assertTrue(gamemgr.the_arena.player is the_player)
        self.assertTrue(the_player.arena is gamemgr.the_arena)

    def teardown(self):
        pass


class TestTeleportItem(unittest.TestCase):

    def setUp(self):

        gamemgr.setup(
            arena.UnitTestArenaGenerator(),
            (40, 40))

        pickaxe = templ.iteminfo['PICKAXE'].create()
        gamemgr.add_item(pickaxe, (3, 3))
        pickaxeblock = gamemgr.get_block((3, 3))

        self.assertTrue(pickaxe in pickaxeblock.itemlist)
        self.pa = pickaxe

        apple = templ.iteminfo['APPLE'].create()
        gamemgr.add_item(apple, (5, 5))
        appleblock = gamemgr.get_block((5, 5))
        self.assertTrue(apple in appleblock.itemlist)
        self.ap = apple

    def test_no_teleport_out_of_arena_bounds(self):
        self.assertFalse(gamemgr.teleport_item(self.pa, (80, 80)))

    def test_no_teleport_inside_of_walls(self):
        self.assertFalse(gamemgr.teleport_item(self.pa, (4, 4)))

    def test_no_teleport_items_not_added_to_arena(self):
        another_pickaxe = templ.iteminfo['PICKAXE'].create()
        self.assertFalse(
            gamemgr.teleport_item(another_pickaxe, (7, 7)))

    def test_teleport_item_to_empty_square(self):
        self.assertTrue(gamemgr.teleport_item(self.pa, (9, 9)))
        self._validate_item(self.pa, (3, 3), (9, 9))

    def test_teleport_item_to_another_item(self):
        self.assertTrue(gamemgr.teleport_item(self.pa, (5, 5)))
        self._validate_item(self.pa, (9, 9), (5, 5))
        self._validate_item(self.pa, (3, 3), (5, 5))

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

        fire_elemental = templ.creatureinfo['FIRE_ELEMENTAL'].create()
        gamemgr.add_creature(fire_elemental, (9, 9))
        self.assertTrue(
            gamemgr.the_arena.blockArray[(9, 9)].creature is fire_elemental)

        self.fe = fire_elemental

    def test_no_teleport_to_non_walkable_tile(self):
        self.assertFalse(gamemgr.teleport_creature(self.fe, (4, 4)))

    def test_no_teleport_to_outside_arena(self):
        self.assertFalse(gamemgr.teleport_creature(self.fe, (80, 80)))

    def test_no_teleport_onto_other_creature(self):

        #teleporting on top of another creature should not work
        rabbit = templ.creatureinfo['RABBIT'].create()
        gamemgr.add_creature(rabbit, (11, 11))
        self.assertTrue(
            gamemgr.the_arena.blockArray[(11, 11)].creature is rabbit)
        self.assertFalse(gamemgr.teleport_creature(self.fe, (11, 11)))

    def test_no_teleport_creature_that_wasnt_added(self):

        another_rabbit = templ.creatureinfo['RABBIT'].create()
        self.assertFalse(gamemgr.teleport_creature(another_rabbit, (19, 19)))

    def test_valid_creature_teleportation(self):

        #double-checking that the fire elemental is where we first put him
        self.assertTrue(
            gamemgr.the_arena.blockArray[(9, 9)].creature is self.fe)
        self.assertEqual(self.fe.location, (9, 9))

        #now to a teleport that should work
        self.assertTrue(gamemgr.teleport_creature(self.fe, (15, 15)))

        self.assertTrue(
            gamemgr.the_arena.blockArray[(15, 15)].creature is self.fe)

        self.assertFalse(gamemgr.the_arena.blockArray[(9, 9)].creature)

        self.assertEqual(self.fe.location, (15, 15))
        self.assertTrue(
            self.fe.block is gamemgr.the_arena.blockArray[(15, 15)])

#==============================================================================
# replace/merge ArenaTile with Block
#==============================================================================


class BlockGetGlyphTests(unittest.TestCase):

    def setUp(self):

        gamemgr.setup(
            arena.UnitTestArenaGenerator(),
            (40, 40))

        self.pl = templ.playerclassinfo['PLAYER_DEFAULT'].create()
        self.pa = templ.iteminfo['PICKAXE'].create()
        self.ap = templ.iteminfo['APPLE'].create()
        self.fe = templ.creatureinfo['FIRE_ELEMENTAL'].create()

        self.assertTrue(gamemgr.add_player(self.pl, (5, 5)))
        self.assertTrue(gamemgr.add_creature(self.fe, (7, 7)))
        self.assertTrue(gamemgr.add_item(self.pa, (7, 7)))
        self.assertTrue(gamemgr.add_item(self.ap, (7, 7)))

    def test_empty_tile_gets_block_glyph(self):

        self.assertEqual(
            gamemgr.get_block((9, 9)).get_glyph(),
            ord('.'))

        self.assertEqual(
            gamemgr.get_block((10, 10)).get_glyph(),
            ord('#'))

    def test_items_no_creatre_gets_last_item_glyph(self):

        assert(gamemgr.teleport_item(self.pa, (11, 11)))
        assert(gamemgr.teleport_item(self.ap, (11, 11)))

        self.assertEqual(
            gamemgr.get_block((11, 11)).get_glyph(),
            ord('%'))

    def test_creature_and_items_gets_creature_glyph(self):

        assert(gamemgr.teleport_item(self.pa, (13, 13)))
        assert(gamemgr.teleport_item(self.ap, (13, 13)))
        assert(gamemgr.teleport_creature(self.fe, (13, 13)))

        self.assertEqual(
            gamemgr.get_block((13, 13)).get_glyph(),
            ord('E'))

    def test_player_and_items_gets_player_glyph(self):

        assert(gamemgr.teleport_item(self.pa, (15, 15)))
        assert(gamemgr.teleport_item(self.ap, (15, 15)))
        assert(gamemgr.teleport_creature(self.pl, (15, 15)))

        self.assertEqual(
            gamemgr.get_block((15, 15)).get_glyph(),
            ord('@'))


if __name__ == '__main__':
    unittest.main()
