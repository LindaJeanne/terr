import numpy as np
import networkx as nx
import gameobj as ob
import actor
import item


class Arena(object):

    def __init__(self, mapgrid):

        self.grid = np.empty(mapgrid.shape, ob.Block)
        self.player = None

        for i, block_token in np.ndenumerate(mapgrid):
            self.grid[i] = ob.create_block(block_token, self)
            self.grid[i].location = i

        self.navgraph = self.build_master_navgraph()

    def build_master_navgraph(self):
        pass

    def add_player_from_token(self, token, coords):
        self.player = self.add_actor_from_token(token, coords)
        self.grid[coords].add_player(self.player)
        return self.player

    def add_actor_from_token(self, token, coords):
        new_actor = actor.create_actor(token)
        self.grid[coords].add_actor(new_actor)
        return new_actor

    def add_item_from_token(self, token, coords):
        new_item = item.create_item(token)
        self.grid[coords].add_item(new_item)
        return new_item

    def change_block(self, coords, new_block_token):

        old_block = self.grid[coords]
        if any(
                old_block.item_list,
                old_block.actor_list,
                old_block.the_player):
            return False

        self.grid[coords] = ob.create_block(new_block_token, self)

        # TODO: call to update master nav-graph, once such a call exists.


class NavGraph(nx.Graph):
    pass


class ArenaGenerator(object):

    def generate(self, shape):
        ''' returns an array of block tokens'''
        return np.full(shape, 'GENERIC_FLOOR_BLOCK', object)


class GenUnitTestArena(ArenaGenerator):

    def generate(self, shape):

        new_grid = super().generate(shape)

        for i, v in np.ndenumerate(new_grid):
            x_even = ((i[0] % 2) == 0)
            y_even = ((i[1] % 2) == 0)
            if x_even and y_even:
                new_grid[i] = 'GENERIC_SOLID_BLOCK'

        return new_grid


class ArenaPopulator(object):

    def populate(self, the_arena, player_token):
        return {'actor_list': list(), 'decay_list': list()}


class PopUnitTestArena(ArenaPopulator):

    def populate(self, the_arena, player_token):

        actor_list = list()
        decay_list = list()

        the_arena.add_item_from_token('GENERIC_ITEM', (5, 5))
        actor_list.append(the_arena.add_actor_from_token(
            'NULL_CREATURE', (7, 7)))
        actor_list.append(the_arena.add_player_from_token(
            player_token, (9, 9)))

        return {'actor_list': actor_list, 'decay_list': decay_list}


def generate_arena(generator_class, shape):
    the_generator_class = globals()[generator_class]
    the_generator = the_generator_class()
    return Arena(the_generator.generate(shape))


def populate_arena(populator_class, the_arena, player_token):
    the_populator_class = globals()[populator_class]
    the_populator = the_populator_class()
    return the_populator.populate(the_arena, player_token)
