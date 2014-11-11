import unittest
import creature
import player
import item
import gamemgr
import turnmgr
import node
import gridgen
import arena
import action
import mixins

unit_test_arena = None


def setup():
    global unit_test_arena

    generator = gridgen.UnitTestGridGenerator()
    tokenarray = generator.create((40, 40))
    unit_test_arena = arena.Arena(tokenarray)


def clear_arena():

    global unit_test_arena

    itemset = set(unit_test_arena.itemset)
    for the_item in itemset:
        unit_test_arena.remove_item(the_item)

    creatureset = set(unit_test_arena.creatureset)
    for the_creature in creatureset:
        unit_test_arena.remove_creature(the_creature)

    gamemgr.turn_list = list()


setup()


class ArenaTests(unittest.TestCase):

    def setUp(self):

        gamemgr.setup(
            gridgen.UnitTestGridGenerator(),
            (20, 20))
        self.arena = gamemgr.the_arena

    def test_generate_2D_arena(self):

        wall_block = self.arena.grid[(4, 4)]
        floor_block = self.arena.grid[(5, 5)]

        self.assertEqual(wall_block.token, 'BLOCK_STONE')
        self.assertFalse(wall_block.isPassable)
        self.assertFalse(wall_block.isPassable)

        self.assertEqual(floor_block.token, 'BLOCK_AIR')
        self.assertTrue(floor_block.isPassable)
        self.assertTrue(floor_block.isTransparent)

    def teardown(self):
        pass


class TemplateTests(unittest.TestCase):

    def test_create_block(self):

        new_glass_block = node.Node('BLOCK_GLASS')

        self.assertTrue(new_glass_block)
        self.assertEqual(new_glass_block.token, 'BLOCK_GLASS')
        self.assertEqual(new_glass_block.glyph, 34)
        self.assertFalse(new_glass_block.isPassable)
        self.assertTrue(new_glass_block.isTransparent)

    def test_create_creature(self):

        the_creature = creature.create('FIRE_ELEMENTAL')

        self.assertTrue(the_creature)
        self.assertEqual(the_creature.token, 'FIRE_ELEMENTAL')
        self.assertEqual(the_creature.glyph, ord('E'))

    def test_create_player(self):

        new_player = player.create('PLAYER_DEFAULT')

        self.assertTrue(new_player)
        self.assertEqual(new_player.token, 'PLAYER_DEFAULT')
        self.assertEqual(new_player.glyph, ord('@'))

    def test_create_item(self):

        new_item = item.create('PICKAXE')

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

        wall_block = gamemgr.the_arena.grid[(4, 4)]
        floor_block = gamemgr.the_arena.grid[(5, 5)]

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

        the_tile = gamemgr.the_arena.grid[(5, 5)]
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

        the_tile = gamemgr.the_arena.grid[(5, 5)]

        pickaxe = gamemgr.new_item('PICKAXE', (5, 5))

        self.assertTrue(pickaxe)
        self.assertTrue(pickaxe in gamemgr.the_arena.itemset)
        self.assertTrue(pickaxe.contain is the_tile)
        self.assertTrue(pickaxe in the_tile.itemlist)

    def test_add_multiple_items_to_tile(self):

        pickaxe = gamemgr.new_item('PICKAXE', (5, 5))
        apple = gamemgr.new_item('APPLE', (5, 5))

        the_tile = gamemgr.the_arena.grid[(5, 5)]

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
            the_player.node is gamemgr.the_arena.grid[(13, 13)])

    def teardown(self):
        pass


class TestTeleportItem(unittest.TestCase):

    def setUp(self):

        clear_arena()
        global unit_test_arena

        self.arena = unit_test_arena

        pickaxe = item.create('PICKAXE')
        self.arena.place_item(pickaxe, (3, 3))
        pickaxeblock = self.arena.grid[(3, 3)]

        self.assertTrue(pickaxe)
        self.assertTrue(pickaxeblock)
        self.assertTrue(pickaxe in pickaxeblock.itemlist)
        self.assertTrue(pickaxe.contain is pickaxeblock)

        self.pa = pickaxe

        apple = item.create('APPLE')
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

        global unit_test_arena
        clear_arena()

        self.arena = unit_test_arena
        self.fe = creature.create('FIRE_ELEMENTAL')
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
        rabbit = creature.create('RABBIT')
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

        self.pl = player.create('PLAYER_DEFAULT')
        self.arena.place_creature(self.pl, (5, 5))

        self.pa = item.create('PICKAXE')
        self.arena.place_item(self.pa, (7, 7))

        self.ap = item.create('APPLE')
        self.arena.place_item(self.ap, (7, 7))

        self.fe = creature.create('FIRE_ELEMENTAL')
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

        self.ngz = creature.create('NORTH_GOING_ZAX')
        self.arena.place_creature(self.ngz, (35, 35))

        self.other_ngz = creature.create('NORTH_GOING_ZAX')
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

        turnmgr.tick()
        self.assertEqual(self.ngz.node.location, (35, 34))
        self.assertEqual(self.other_ngz.node.location, (37, 36))

        self.assertEqual(turnmgr._counter, 1)
        self.assertEqual(turnmgr._tickloop[0], list())

        self.assertTrue(self.ngz in turnmgr._tickloop[10])
        self.assertTrue(self.other_ngz in turnmgr._tickloop[10])

        for i in range(0, 9):
            turnmgr.tick()

        self.assertEqual(turnmgr._counter, 10)
        self.assertEqual(self.ngz.node.location, (35, 34))
        self.assertEqual(self.other_ngz.node.location, (37, 36))

        turnmgr.tick()

        self.assertEqual(self.ngz.node.location, (35, 33))
        self.assertEqual(self.other_ngz.node.location, (37, 35))

        for i in range(0, 999):
            turnmgr.tick()

        self.assertEqual(turnmgr._counter, 10)
        self.assertEqual(self.ngz.node.location, (35, 14))
        self.assertEqual(self.other_ngz.node.location, (37, 16))

        turnmgr.tick()

        self.assertEqual(turnmgr._counter, 11)
        self.assertEqual(self.ngz.node.location, (35, 13))
        self.assertEqual(self.other_ngz.node.location, (37, 15))


class PickupDropTest(unittest.TestCase):

    def setUp(self):

        global unit_test_arena
        clear_arena()
        self.arena = None
        self.arena = unit_test_arena

        self.pd_one = creature.create('PICKUP_DROPPER')
        self.arena.place_creature(self.pd_one, (15, 15))

        self.pd_two = creature.create('PICKUP_DROPPER')
        self.arena.place_creature(self.pd_two, (5, 5))

        self.apple_one = item.create('APPLE')
        self.arena.place_item(self.apple_one, (15, 15))

        self.apple_two = item.create('APPLE')
        self.arena.place_item(self.apple_two, (25, 25))

        self.pickaxe_one = item.create('PICKAXE')
        self.arena.place_item(self.pickaxe_one, (15, 15))

        self.pickaxe_two = item.create('PICKAXE')
        self.arena.place_item(self.pickaxe_two, (31, 31))

    def test_pick_up_drop_items_on_same_square(self):

        # Starting conditions
        self.assertTrue(self.pd_one.inv_empty())
        self.assertFalse(self.pd_one.node.inv_empty())
        self.assertFalse(self.pd_one.inv_full())
        self.assertFalse(self.pd_one.node.inv_full())
        self.assertTrue(self.pd_one.node.in_inv(self.apple_one))
        self.assertTrue(self.pd_one.node.in_inv(self.pickaxe_one))

        # Pick up the apple
        self.assertTrue(self.pd_one.pickup_item(self.apple_one))

        self.assertFalse(self.pd_one.inv_empty())
        self.assertFalse(self.pd_one.node.inv_empty())

        self.assertTrue(self.apple_one.contain is self.pd_one)
        self.assertTrue(self.pd_one.in_inv(self.apple_one))
        self.assertFalse(self.pd_one.node.in_inv(self.apple_one))

        self.assertTrue(self.pickaxe_one.contain is self.pd_one.node)
        self.assertTrue(self.pd_one.node.in_inv(self.pickaxe_one))
        self.assertFalse(self.pd_one.in_inv(self.pickaxe_one))

        # Pick up the pickaxe
        self.assertTrue(self.pd_one.pickup_item(self.pickaxe_one))

        self.assertTrue(self.pd_one.node.inv_empty())
        self.assertTrue(self.pd_one.in_inv(self.pickaxe_one))
        self.assertTrue(self.pd_one.in_inv(self.apple_one))
        self.assertFalse(self.pd_one.node.in_inv(self.apple_one))
        self.assertFalse(self.pd_one.node.in_inv(self.pickaxe_one))

        # Drop the apple
        self.assertTrue(self.pd_one.drop_item(self.apple_one))

        self.assertFalse(self.pd_one.inv_empty())
        self.assertFalse(self.pd_one.node.inv_empty())

        self.assertTrue(self.pd_one.in_inv(self.pickaxe_one))
        self.assertTrue(self.pd_one.node.in_inv(self.apple_one))

        self.assertFalse(self.pd_one.in_inv(self.apple_one))
        self.assertFalse(self.pd_one.node.in_inv(self.pickaxe_one))

    def test_no_pick_up_items_on_other_square(self):

        self.assertFalse(self.pd_two.pickup_item(self.apple_two))
        self.assertFalse(self.pd_two.in_inv(self.apple_two))
        self.assertTrue(self.arena.grid[(25, 25)].in_inv(self.apple_two))
        self.assertTrue(self.pd_two.inv_empty())
        self.assertTrue(self.pd_two.node.inv_empty())

    def test_no_drop_items_not_in_inventory(self):

        self.assertFalse(self.pd_two.drop_item(self.pickaxe_two))
        self.assertFalse(self.pd_two.in_inv(self.pickaxe_two))
        self.assertFalse(self.pd_two.node.in_inv(self.pickaxe_two))
        self.assertTrue(self.arena.grid[(31, 31)].in_inv(self.pickaxe_two))


class TrivialPathingTest(unittest.TestCase):

    def setUp(self):
        clear_arena()
        global unit_test_arena
        self.arena = unit_test_arena
        has_turn = list()

        self.fe = creature.create('FIRE_ELEMENTAL')
        self.arena.place_creature(self.fe, (25, 25))
        has_turn.append(self.fe)

        self.pc = creature.create('PLAYER_CHASER')
        self.arena.place_creature(self.pc, (15, 15))
        has_turn.append(self.pc)

        self.pl = player.create('PLAYER_DEFAULT')
        self.arena.place_creature(self.pl, (15, 10))
        self.arena.player = self.pl

        turnmgr.setup(has_turn)

    def test_path_towards_easy_node(self):

        path_action = action.PathTowardsAction(self.arena.grid[(25, 20)])
        path_action.execute(self.fe)

        self.assertEqual(self.fe.node.location, (25, 24))

    def test_player_chaser(self):

        turnmgr.tick()

        self.assertEqual(self.pc.node.location, (15, 14))


class TestTickReturnValue(unittest.TestCase):

    def setUp(self):

        clear_arena()
        global unit_test_arena
        self.arena = unit_test_arena
        has_turn = list()

        self.zax = creature.create('NORTH_GOING_ZAX')
        self.arena.place_creature(self.zax, (25, 25))
        has_turn.append(self.zax)

        self.rabbit = creature.create('RABBIT')
        self.arena.place_creature(self.rabbit, (15, 15))
        has_turn.append(self.rabbit)

        turnmgr.setup(has_turn)

    def test_tick_return_dict(self):

        self.assertTrue(self.zax)
        self.assertTrue(self.rabbit)

        result = dict()

        while not result:
            result = turnmgr.tick()

        self.assertTrue(isinstance(result[self.zax], action.StepAction))
        self.assertTrue(isinstance(result[self.rabbit], action.NullAction))


class TestNewUtilityFunctions(unittest.TestCase):

    def setUp(self):

        clear_arena()
        global unit_test_arena
        self.arena = unit_test_arena

        self.fe = creature.create('FIRE_ELEMENTAL')
        self.arena.place_creature(self.fe, (25, 25))

        self.rb = creature.create('RABBIT')
        self.arena.place_creature(self.rb, (25, 26))

        self.ap = item.create('APPLE')
        self.arena.place_item(self.ap, (25, 27))

        self.pi = item.create('PICKAXE')
        self.arena.place_item(self.pi, (11, 11))

        self.zx = creature.create('NORTH_GOING_ZAX')
        self.arena.place_creature(self.zx, (15, 15))

    def test_findAdjacent(self):

        result = self.fe.node.find_adj_creature()
        self.assertTrue(result is self.rb)

        result = self.fe.node.find_adj_item()
        self.assertFalse(result)

        result = self.rb.node.find_adj_creature()
        self.assertTrue(result is self.fe)

        result = self.rb.node.find_adj_item()
        self.assertTrue(result is self.ap)

        result = self.ap.contain.find_adj_creature()
        self.assertTrue(result is self.rb)

        result = self.ap.contain.find_adj_item()
        self.assertFalse(result)

    def test_find_creatures_in_radius(self):

        self.assertTrue(self.zx in self.arena.creatureset)

        result = self.arena.find_creatures_in_radius(
            self.arena.grid[(5, 5)], 4)
        self.assertFalse(result)

        result = self.arena.find_creatures_in_radius(
            self.zx.node, 3)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.zx in result)

        result = self.arena.find_creatures_in_radius(
            self.zx.node, 20)

        self.assertEqual(len(result), 3)
        self.assertTrue(self.rb in result)
        self.assertTrue(self.fe in result)
        self.assertTrue(self.zx in result)

    def test_find_items_in_radius(self):

        result = self.arena.find_items_in_radius(
            self.zx.node, 3)
        self.assertFalse(result)

        result = self.arena.find_items_in_radius(
            self.zx.node, 7)
        self.assertEqual(len(result), 1)
        self.assertTrue(self.pi in result)

        result = self.arena.find_items_in_radius(
            self.zx.node, 30)
        self.assertEqual(len(result), 2)
        self.assertTrue(self.pi in result)
        self.assertTrue(self.ap in result)

    def test_find_closest_creature_in_radius(self):

        result = self.arena.get_closest_creature(
            self.zx.node, 30)

        self.assertTrue(result is self.fe)

        result = self.arena.get_closest_creature(
            self.zx.node, 3)
        self.assertFalse(result)


#    def test_find_nearest_creature(self):
#
#        result = self.zx.arena.find_nearest_creature(self.node, 20)
#
#        self.assertTrue(result is self.fe)
#
#        self.assertFalse(self.zx.arena.find_nearest_crature(self.node, 5))
#
#        clear_arena()
#        rabbit = creature.create('RABBIT')
#        self.arena.place_creature(rabbit, (23, 23))
#
#        self.assertTrue(False)


class TrivialCombatTest(unittest.TestCase):

    def setUp(self):

        clear_arena()
        global unit_test_arena
        self.arena = unit_test_arena
        has_turn = list()

        self.ta_one = creature.create('TRACK_AND_ATTACK')
        self.arena.place_creature(self.ta_one, (25, 25))
        has_turn.append(self.ta_one)

        self.ta_two = creature.create('TRACK_AND_ATTACK')
        self.arena.place_creature(self.ta_two, (25, 28))
        has_turn.append(self.ta_two)

        turnmgr.setup(has_turn)

    def test_basic_combat(self):

        # Verify Setup
        self.assertTrue(self.ta_one)
        self.assertEqual(self.ta_one.node.location, (25, 25))
        self.assertTrue(self.ta_two)
        self.assertEqual(self.ta_two.node.location, (25, 28))

        # First tick they should approack each other.
        result = {}
        while not result:
            result = turnmgr.tick()

        self.assertTrue(isinstance(
            result[self.ta_one], action.PathTowardsAction))
        self.assertTrue(isinstance(
            result[self.ta_two], action.PathTowardsAction))
        self.assertEqual(self.ta_one.node.location, (25, 26))
        self.assertEqual(self.ta_two.node.location, (25, 27))

        # Next action should be for them to attack each other.
        result = {}
        while not result:
            result = turnmgr.tick()

        ta_one_action = result[self.ta_one]
        ta_two_action = result[self.ta_two]

        self.assertTrue(isinstance(ta_one_action, action.MeleeAction))
        self.assertTrue(isinstance(ta_two_action, action.MeleeAction))


class LoadingCombatAttackDefenseProfiles(unittest.TestCase):

    def setUp(self):
        pass

    def test_load_attack_profile(self):

        ap = mixins.attack_profile_create(
            'BASIC_ATTACK_PROFILE')

        self.assertTrue(isinstance(ap, mixins.BasicAttackProfile))
        self.assertEqual(ap.token, 'BASIC_ATTACK_PROFILE')

        self.assertEqual(ap.attacks['TEETH']['hit_chance'], 90)
        self.assertEqual(ap.attacks['TEETH']['speed'], 10)
        self.assertEqual(ap.attacks['TEETH']['damage_type'], 'TEARING')
        self.assertEqual(ap.attacks['TEETH']['damage_range'], (20, 40))

        self.assertEqual(ap.attacks['CLAWS']['hit_chance'], 90)

    def test_load_defense_profile(self):

        the_defense_profile = mixins.defense_profile_create(
            'BASIC_DEFENSE_PROFILE')

        self.assertTrue(isinstance(
            the_defense_profile, mixins.BasicDefenseProfile))
        self.assertEqual(the_defense_profile.token, 'BASIC_DEFENSE_PROFILE')
        self.assertEqual(the_defense_profile.dodge_chance, 20)
        self.assertEqual(the_defense_profile.soak_range, (5, 15))


if __name__ == '__main__':
    unittest.main()
