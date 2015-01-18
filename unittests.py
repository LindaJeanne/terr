import unittest
import item
import gameobj
import arena
import actor
import gameloop
import action
import logger


def standard_gameloop():

    return gameloop.GameLoop(
        (20, 20),
        'GenUnitTestArena',
        'PopUnitTestArena',
        'TerrUnitTestDisplay',
        'UNIT_TEST_PLAYER')


class ItemTests(unittest.TestCase):

    def setUp(self):
        self.test_item = item.create_item('GENERIC_ITEM')

    def test_throw(self):

        self.assertIsInstance(
            self.test_item.throw_profile, item.ThrowableProfile)

    def test_decay(self):

        self.assertIsInstance(
            self.test_item.decay_profile, item.DecayableProfile)

    def test_damage(self):

        self.assertIsInstance(
            self.test_item.damage_profile, item.DamagableProfile)

    def test_treasure(self):

        self.assertIsInstance(
            self.test_item.treasure_profile, item.TreasureProfile)


class BlockTests(unittest.TestCase):

    def setUp(self):
        self.solid_block = gameobj.create_block('GENERIC_SOLID_BLOCK')
        self.air_block = gameobj.create_block('GENERIC_AIR_BLOCK')
        self.floor_block = gameobj.create_block('GENERIC_FLOOR_BLOCK')
        self.liquid_block = gameobj.create_block('GENERIC_LIQUID_BLOCK')

    def test_solid_block(self):

        self.assertIsInstance(self.solid_block, gameobj.SolidBlock)
        self.assertEqual(self.solid_block.token, 'GENERIC_SOLID_BLOCK')

    def test_air_block(self):

        self.assertIsInstance(self.air_block, gameobj.AirBlock)
        self.assertEqual(self.air_block.token, 'GENERIC_AIR_BLOCK')

    def test_floor_block(self):

        self.assertIsInstance(self.floor_block, gameobj.FloorBlock)
        self.assertEqual(self.floor_block.token, 'GENERIC_FLOOR_BLOCK')
        self.assertEqual(self.floor_block.item_list, list())
        self.assertEqual(self.floor_block.actor_list, list())
        self.assertIs(self.floor_block.structure, None)

    def test_liquid_block(self):

        self.assertIsInstance(self.liquid_block, gameobj.LiquidBlock)
        self.assertEqual(self.liquid_block.token, 'GENERIC_LIQUID_BLOCK')


class ArenaGeneratorTests(unittest.TestCase):

    def setUp(self):

        the_generator = arena.GenUnitTestArena()
        self.gridarray = the_generator.generate((10, 10))

    def test_gridarray_values(self):

        self.assertEqual(self.gridarray[(5, 5)], 'GENERIC_FLOOR_BLOCK')
        self.assertEqual(self.gridarray[(5, 8)], 'GENERIC_FLOOR_BLOCK')
        self.assertEqual(self.gridarray[(8, 8)], 'GENERIC_SOLID_BLOCK')


class CreateArenaTests(unittest.TestCase):

    def setUp(self):

        self.the_arena = arena.generate_arena('GenUnitTestArena', (10, 10))
        arena.populate_arena(
            'PopUnitTestArena', self.the_arena, 'UNIT_TEST_PLAYER')

        # TODO: if a pickle file of the test arena does not already
        # exist, create it.

    def test_grid_creation(self):

        block_grid = self.the_arena.grid

        self.assertIsInstance(block_grid[(4, 4)], gameobj.SolidBlock)
        self.assertIsInstance(block_grid[(5, 5)], gameobj.FloorBlock)

    def test_item_population(self):
        block_grid = self.the_arena.grid
        self.assertTrue(block_grid[(5, 5)].item_list)
        self.assertFalse(block_grid[(5, 6)].item_list)
        self.assertIsInstance(block_grid[(5, 5)].item_list[0], item.Item)

    def test_actor_population(self):
        block_grid = self.the_arena.grid

        self.assertTrue(block_grid[(7, 7)].actor_list)
        self.assertFalse(block_grid[(7, 8)].actor_list)
        self.assertIsInstance(
            block_grid[(7, 7)].actor_list[0], actor.AiCreature)


class CreateActorTests(unittest.TestCase):

    def setUp(self):
        self.null_creature = actor.create_actor('NULL_CREATURE')

    def test_actor_creation(self):
        self.assertIsInstance(self.null_creature, actor.Actor)
        self.assertIsInstance(self.null_creature, actor.AiCreature)

    def test_actor_movement(self):
        self.assertIsInstance(
            self.null_creature.movement_profile, actor.NullActorProfile)

    def test_actor_attack(self):
        self.assertIsInstance(
            self.null_creature.attack_profile, actor.NullActorProfile)

    def test_actor_defense(self):
        self.assertIsInstance(
            self.null_creature.defense_profile, actor.NullActorProfile)

    def test_actor_magic(self):
        self.assertIsInstance(
            self.null_creature.magic_profile, actor.NullActorProfile)

    def test_actor_equip(self):
        self.assertIsInstance(
            self.null_creature.equip_profile, actor.NullActorProfile)


class CreateGameLoopTests(unittest.TestCase):

    def setUp(self):

        self.game_loop = standard_gameloop()
        self.other_creatures = list(self.game_loop.actor_list)
        self.other_creatures.remove(self.game_loop.the_player)
        self.other_a = self.other_creatures[0]

    def test_gameloop_setup(self):

        gl = self.game_loop

        self.assertTrue(gl.the_player)
        self.assertTrue(gl.the_player in gl.actor_list)
        self.assertTrue(self.other_a)
        self.assertTrue(self.other_a in gl.actor_list)

        self.assertEqual(gl.tickcount, 0)
        self.assertEqual(gl.decaycount, 0)
        self.assertTrue(gl.the_display)
        self.assertTrue(gl.the_arena)
        self.assertTrue(gl.the_player)

        self.assertIs(gl.actor_list, gl.tickloop[1])

    def test_first_tick(self):
        gl = self.game_loop
        gl.tick()

        self.assertEqual(gl.tickcount, 1)
        self.assertEqual(gl.decaycount, 1)
        self.assertTrue(gl.tickloop[11])
        self.assertTrue(gl.the_player in gl.tickloop[11])
        self.assertTrue(self.other_a in gl.tickloop[11])
        self.assertIsInstance(gl.last_actions[self.other_a], action.NullAction)
        self.assertIsInstance(
            gl.last_actions[gl.the_player], action.StepDirectionAction)
        self.assertEqual(gl.the_player.container, gl.the_arena.grid[(9, 10)])

    def test_second_tick(self):
        gl = self.game_loop
        gl.tick()
        gl.tick()

        self.assertEqual(gl.tickcount, 2)
        self.assertEqual(gl.decaycount, 2)
        self.assertTrue(gl.tickloop[11])
        self.assertTrue(gl.the_player in gl.tickloop[11])
        self.assertTrue(self.other_a in gl.tickloop[11])
        self.assertIsInstance(gl.last_actions[self.other_a], action.NullAction)
        self.assertIsInstance(
            gl.last_actions[gl.the_player], action.StepDirectionAction)
        self.assertEqual(gl.the_player.container, gl.the_arena.grid[(9, 10)])

    def test_eleventh_tick(self):
        gl = self.game_loop

        for _ in range(11):
            gl.tick()

        self.assertEqual(gl.tickcount, 11)
        self.assertEqual(gl.decaycount, 11)
        self.assertTrue(gl.tickloop[21])
        self.assertTrue(gl.the_player in gl.tickloop[21])
        self.assertTrue(self.other_a in gl.tickloop[21])
        self.assertIsInstance(gl.last_actions[self.other_a], action.NullAction)
        self.assertIsInstance(
            gl.last_actions[gl.the_player], action.StepDirectionAction)
        self.assertEqual(gl.the_player.container, gl.the_arena.grid[(9, 11)])


class GetDisplayCharacterTests(unittest.TestCase):

    def setUp(self):
        self.the_arena = arena.generate_arena('GenUnitTestArena', (10, 10))
        arena.populate_arena(
            'PopUnitTestArena', self.the_arena, 'UNIT_TEST_PLAYER')

    def _display(self, x, y):
        return self.the_arena.grid[(x, y)].get_display_tile()['ascii_code']

    def test_display_empty_blocks(self):
        # floor block
        self.assertEqual(self._display(1, 1), 46)
        # wall block
        self.assertEqual(self._display(2, 2), 35)

    def test_display_item_blocks(self):
        # single item on block, 'G' for generic object
        self.assertEqual(self._display(5, 5), 71)

    def test_display_creature_blocks(self):
        # single creature on block, 'N' for NullCreature
        self.assertEqual(self._display(7, 7), 78)

    def test_display_player_blocks(self):
        # player is only thing on block
        self.assertEqual(self._display(9, 9), 64)


class CreateActionTests(unittest.TestCase):

    def setUp(self):
        self.the_arena = arena.generate_arena('GenUnitTestArena', (10, 10))
        the_lists = arena.populate_arena(
            'PopUnitTestArena', self.the_arena, 'UNIT_TEST_PLAYER')
        self.turn_list = the_lists['actor_list']

    def test_create_movement_action(self):

        the_action = action.create_action(
            'StepDirectionAction', self.turn_list[0], (0, 1))
        self.assertIsInstance(the_action, action.Action)
        self.assertIsInstance(the_action, action.MovementAction)
        self.assertIsInstance(the_action, action.StepDirectionAction)
        self.assertIs(the_action.actor, self.turn_list[0])
        self.assertEqual(tuple(the_action.target), (7, 8))
        self.assertFalse(the_action.item)


class LoggerTests(unittest.TestCase):

    def setUp(self):
        self.logname = 'unittest.log'
        with open(self.logname, 'w') as f:
            f.write('')
        self.logger = logger.Logger('unittest.log', 3, False)

    def _print_all_lines(self):
        self.logger.log_error("This is an error.")
        self.logger.log_warning("This is a warning")
        self.logger.log_info("This is informational.")
        self.logger.log_debug("This is extended info for debugging.")

    def test_log_level_three(self):
        self.logger.log_level = 3
        self._print_all_lines()

        with open(self.logname) as f:
            result = f.readlines()

        self.assertEqual(len(result), 4)
        self.assertTrue("[ERROR] This is an error." in result[0])
        self.assertTrue("[WARNING] This is a warning" in result[1])
        self.assertTrue("[INFO] This is informational." in result[2])
        self.assertTrue(
            "[DEBUG] This is extended info for debugging." in result[3])

    def test_log_level_two(self):
        self.logger.log_level = 2
        self._print_all_lines()

        with open(self.logname) as f:
            result = f.readlines()

        self.assertEqual(len(result), 3)
        self.assertTrue("[ERROR] This is an error." in result[0])
        self.assertTrue("[WARNING] This is a warning" in result[1])
        self.assertTrue("[INFO] This is informational." in result[2])

    def test_log_level_one(self):
        self.logger.log_level = 1
        self._print_all_lines()

        with open(self.logname) as f:
            result = f.readlines()

        self.assertEqual(len(result), 2)
        self.assertTrue("[ERROR] This is an error." in result[0])
        self.assertTrue("[WARNING] This is a warning" in result[1])

    def test_log_level_zero(self):
        self.logger.log_level = 0
        self._print_all_lines()

        with open(self.logname) as f:
            result = f.readlines()

        self.assertEqual(len(result), 1)
        self.assertTrue("[ERROR] This is an error." in result[0])

if __name__ == '__main__':
    unittest.main()
