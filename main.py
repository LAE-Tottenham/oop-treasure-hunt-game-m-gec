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

tiles = [
    "  ",#"  ",
    "██",
    "▓▓",
    "  ",
    "▒▒"
]

chars = [
    "❂"
]

'''
def generate_row(width, x):
    row = ""
    for y in range(width):
        #x = x / width_scale_factor
        y = -(y - width // 2) / (width_scale_factor - 0.25)
        block = tiles[1]
        if (x**2 + y**2) < radius**2:
            block = tiles[0]
        elif (x**2 + y**2) < (radius + 0.85)**2:
            block = tiles[2]
        else:
            block = tiles[1]
        row += (block)
    return row

grid = np.array([generate_row(int(grid_size * width_scale_factor), -(x - grid_size // 2)) for x in range(grid_size)])
'''



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