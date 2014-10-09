#import numpy as np
import maplayer as ml
#import cursesdisplay as cd


width = 40
height = 40

worldmap = ml.WorldMap((width, height))

for i in range(1, 9):
    worldmap += worldmap.gen_perlin(octaves=i)

#for i in range(1, 5):
#    worldmap.apply_automata()

worldmap.display_rougelike_map()
