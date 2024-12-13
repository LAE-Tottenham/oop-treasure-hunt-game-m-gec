from classes import *
import numpy as np
from random import randint as random
import os
import time
os.system('clear')

#height and width of the screen
height, width = 45, 60

#height and width of the map
map_height = 30
map_width = 30#np.floor(map_height * np.pi * 0.5)

chars = [
    "❂"
]



#main loop ------------------------------------------------------------------------------------

while True:
    #clear the last screen
    os.system('clear')

    screen = Screen(height, width)
    map = Map(height, width, 1)

    #screen.add_map_to_screen(map)
    #screen.display()

    pressed_key = input()

    #wait the refresh period
    time.sleep(60**-1)
    break