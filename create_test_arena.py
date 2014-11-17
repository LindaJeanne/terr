import pickle
import arena
import gridgen

utgg = gridgen.UnitTestGridGenerator()

the_arena = arena.Arena(utgg.create((40, 40)))

f = open('test_arena.pickle', 'wb')
pickle.dump(the_arena, f)
