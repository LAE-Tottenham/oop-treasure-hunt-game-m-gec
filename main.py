from classes import *
import numpy as np
from random import randint as random
import os
import time
import shutil #for terminal size check


#inital terminal sizing configuration -----------------------------------------------------------------------------------------------------------------------------------

accepted_columns, accepted_lines = 160, 35
def validate_terminal_dimensions(accepted_columns, accepted_lines):
    columns, lines = shutil.get_terminal_size()
    if (columns < accepted_columns) or (lines < accepted_lines):
        print((columns < accepted_columns) and f"terminal width is too narrow ({columns}/{accepted_columns}), make it wider" or f"terminal height is too low ({lines}/{accepted_lines}), make it taller")
        time.sleep(0.5)
        #os.system('clear')
        return False
    else:
        os.system('clear')
        return True

while True:
    os.system('clear')
    if validate_terminal_dimensions(accepted_columns, accepted_lines): break


#settings -------------------------------------------------------------------------------------------------------------------------------------------------------------

#height and width of the screen
height, width = 45, 80

#height and width of the map
map_height = 45
map_width = 60

fps = 5

#instance configuration ------------------------------------------------------------------------------------------------------------------------------------------------
inventory = Inventory()
player = Player(inventory)
map_one = Map(map_height, map_width, 1)

#main loop -------------------------------------------------------------------------------------------------------------------------------------------------------------

while True:
    #clear the last screen
    os.system('clear')

    #validate terminal dimensions (disabled for performance)
    #if not validate_terminal_dimensions(accepted_columns, accepted_lines): continue

    #generate instances -------------------------------------------------------------------------

    screen = Screen(height, width)
    map = map_one

    #display elements ---------------------------------------------------------------------------

    screen.add_elements_to_screen([map, player, 1, 1, 1, 1])#error origin
    screen.display()

    #break

    #keybinds -----------------------------------------------------------------------------------

    pressed_key = input()
    match pressed_key.lower():
        #movement keybinds-----------------------------
        #top left is (0, 0)
        case "w":
            player.move(np.array([-1, 0]), map)
        case "a":
            player.move(np.array([0, -1]), map)
        case "s":
            player.move(np.array([1, 0]), map)
        case "d":
            player.move(np.array([0, 1]), map)

        #action keybinds-------------------------------
        
        case "e": #interacting with items
            pass
        case "y": #"yes" response to npcs
            pass
        case "n": #"no" response to npcs
            pass
        case " ": #attack
            pass

        #end the program-------------------------------

        case "q":
            break

    #wait the refresh period
    time.sleep(fps**-1)














