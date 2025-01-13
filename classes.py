import multiprocessing.shared_memory
import numpy as np
from noise import pnoise2
from random import randint as random
import multiprocessing
import time
import sys
import os

seed = random(0,100)
#map region calculation functions ---------------------------------------------------------------------------------------------------------------

def noise(x, y, map):
    height, width = map.dimensions
    scale = 8
    result = pnoise2(x / scale, y / scale, octaves=1, persistence=0, lacunarity=0, repeatx=width, repeaty=height, base=seed)
    return 1 - min(round(result * 10), 1)

def convert_to_floor_tile(x, y, array):
    array[x][y] = (x - 1) % 2 == 0 and (y % 2 == 0 and 4 or 6) or (y % 2 == 0 and 6 or 4)

#variables -------------------------------------------------------------------------------------------------------------------------------------

tiles = [
    "  ",
    "██",
    "▓▓",
    "〓",#ℹ۩۞⏏〇〓
    "▒▒",
    "  ",
    "░░",
    "",
    "⚑ ",
    "⚠ ",
    "⚿ ",
    "♝ ",
    "♜ ",
    "♞ ",
    "✠ ",
    "✤ ",
    "✦ ",
    "♚ ",
    "♛ ",
    "౷",
    "⚑ ",
    "⚐ ",
    "♡",
    "♥"
]


#classes ---------------------------------------------------------------------------------------------------------------------------------------

class Screen:
    def __init__(self, passed_height, passed_width):
        self.dimensions = (passed_height, passed_width)
        self.grid = np.zeros((passed_height, passed_width))

    def display(self):
        screen = self.grid
        for row in screen:
            print("".join([(((i < 97) and tiles[min(int(i), len(tiles) - 1)]) or f"{chr(int(i))}") for i in row]))
            #text occupies exactly half the width of the generic pixel
    
    def add_elements_to_screen(self, elements, maps, current_map): #0 = map, 1 = player, 2 = sidescreen, 3 = enemies, 4 = npc merchants, 5 = interactable items
        screen = self.grid

        map, player, sidescreen, enemies, merchants, items = elements

        #add map
        map_height, map_width = map.dimensions
        screen[:map_height, :map_width] = map.array

        #add sidescreen
        sidescreen_height, sidescreen_width = sidescreen.dimensions
        screen[:sidescreen_height, map_width : (map_width + sidescreen_width)] = sidescreen.array

        #add player
        player_x, player_y = player.position

        #check if a kill block or exit flag is about to be stepped on
        if screen[player_x][player_y] == 8:
            #os.system('clear')
            #print("hit")
            #sys.exit()
            #increment map and reset player position
            player.position = (22, 30) #centre
            self.grid = screen
            if current_map != 4:
                current_map += 1
                return maps[current_map], current_map
            else:
                #game ends
                os.system('clear')
                print("you won")
                sys.exit()
        elif screen[player_x][player_y] == 9:
            #game ends
            os.system('clear')
            print("(you lost)\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⠤⠶⢶⠞⠿⠿⠿⡿⢿⠿⣷⢶⡶⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠖⠚⠉⡁⠡⠀⡀⠌⠐⣀⢊⡡⡙⡜⢬⢣⣛⡼⣣⢟⡵⣞⡶⣯⣟⣯⢿⡶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠚⠉⢀⠠⠐⠈⡀⡐⠀⡁⠐⢂⠱⣈⠆⡱⡑⢎⢣⠳⣌⠷⣹⢮⣝⠾⣽⣳⢟⡾⣯⡿⣿⣽⣿⣿⣯⣶⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠞⠋⠀⠀⠀⠀⡀⠠⠐⠠⠐⠀⠂⠄⠃⡈⠐⠠⢊⠱⡘⢌⢣⠹⣌⠳⡭⣞⡼⣻⠵⣯⠿⣽⣳⢿⣻⣾⢿⣽⣿⣿⣿⣮⣵⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣟⠋⠀⠀⠀⠀⠀⠀⡐⠀⡁⠄⠁⠄⠡⢈⠀⠂⠄⠉⠤⢁⠆⡩⢘⠢⡝⣌⢳⡱⢎⡷⣭⣛⢷⣻⡽⣯⣟⣯⣿⢿⣻⣿⣿⣿⣿⣿⣿⣿⣷⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠈⠑⠲⢤⣄⣀⡀⠠⠐⠀⠄⡈⠐⢈⠠⠀⠌⠐⠈⡐⠠⠈⠤⢡⢉⠖⡱⢌⡣⣝⠺⣴⢣⣏⡟⣾⢽⣳⢯⣟⣾⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠉⠀⠀⠀⠀⠀⠀⠀⠉⠛⢿⣷⣶⣥⣔⡀⠡⢀⠐⠈⠠⢈⠐⠀⠄⡉⠐⢂⢡⢊⡱⢊⠴⣊⠷⣡⢟⡼⣹⡞⣯⣟⣯⣟⣷⡿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠙⠿⣿⣿⣷⣦⣬⡀⠡⠀⠂⡁⠐⡀⠑⣈⠢⣘⠰⣉⢖⡩⢞⡱⣎⢷⣣⢟⣧⣟⡾⣽⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⠟⠁⢀⡰⠋⠀⠀⠀⠀⠀⠀⠀⠀⡀⢁⠀⠢⠤⣄⡉⠻⢿⣿⣿⠷⠈⠐⡀⢁⠐⡐⢀⠒⣄⠓⡌⢦⡙⣬⠳⡜⣧⣛⣮⣷⣾⣿⣿⣿⣿⢿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠋⢀⢐⡞⠁⠀⢀⡠⠴⠒⠋⠉⠉⠉⠉⠉⠓⠶⣤⣀⠉⠓⢦⡈⠀⠄⡈⠐⠀⠄⢂⠐⡈⢒⡠⢙⡘⢦⠱⣊⠗⣿⣿⣿⣿⣿⠿⢛⣯⣷⡾⠟⠋⠉⠉⠉⠉⠉⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⡐⢠⠎⠀⡠⠒⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣷⣄⠙⢦⡐⠀⠡⢈⠀⢂⠐⡐⢢⠐⣅⠚⡤⢛⢬⡛⣴⢫⣿⠟⣡⣾⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁⠐⠠⠏⣠⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣦⣤⣀⠀⠈⠻⣷⡄⠹⣆⠁⠠⢈⠀⢂⠔⠢⡑⢌⡚⠴⡩⢖⡹⢦⡿⢃⣾⣿⠋⠀⠀⠴⣶⣾⣷⣶⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣯⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⢀⠠⠁⢂⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠈⣹⣿⣿⣿⣿⣷⡄⠀⠹⣿⣄⠸⣆⠁⠠⢈⠄⢊⠱⣈⠲⢌⠣⣕⢫⣜⡿⣱⣿⡟⠁⠀⣤⠀⠀⣸⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣷⣃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠁⠠⢐⡠⣿⡁⣀⣀⣤⠤⠤⠤⠤⠤⠤⣤⣼⠿⠿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠈⢿⣆⠀⠠⢁⢂⠘⡄⠣⢌⠲⣉⠞⣰⢣⠾⣳⣿⠏⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣤⣤⣤⣄⣀⣀⢹⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⣌⠱⣦⠷⠟⠋⢁⠀⡀⠄⠂⡐⢀⠂⠐⠤⠤⣤⣤⣀⡀⠈⠉⠙⠻⣇⣀⠀⠀⠈⢻⣦⠁⢂⠆⡌⠰⠩⢌⡱⢸⡸⢥⣋⣾⣿⠋⠀⠀⢀⣀⣿⡿⠟⠛⣉⣩⣭⣭⣷⣶⣶⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⣁⢂⠒⠤⡁⡄⢂⡄⢢⡐⣤⢡⡄⢦⣤⣡⢤⡔⣤⢬⡭⣭⣛⣓⠶⢤⣤⣈⡛⠶⣤⣈⣿⣇⠐⡌⢰⠩⡘⠦⣑⢣⢎⡳⣼⣿⠇⣠⣴⣾⣻⣭⣶⢶⣟⣻⣿⣭⣭⣷⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡗⣌⠢⡉⢆⠴⠨⡅⢎⠵⣸⢰⢣⡝⣣⢎⡵⣋⠾⣩⢞⡱⢯⡝⣯⣟⡿⣶⣻⢿⡿⣦⢍⣛⠛⢦⠘⡤⢣⠙⢦⢩⠖⣭⢲⣛⢿⣻⣟⣷⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡜⣆⠣⡍⢆⠣⣓⠸⢌⠲⡡⠎⢦⠱⢌⠊⡔⣉⠒⣡⠊⡕⢊⠜⡰⠌⡓⠥⡋⢎⡱⢃⠞⡤⢋⠦⣙⠰⢣⢹⡘⣎⡝⢦⡻⣜⢯⡳⣟⡾⣽⣻⣟⣿⣻⢿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡼⣌⠳⡜⣌⠣⢆⠣⣌⠱⣠⠉⡔⣈⢂⠱⠐⡠⠡⢀⠒⠠⠌⡠⢁⠂⡅⢂⡑⢂⠆⡍⢲⡈⡕⢪⡔⣍⣣⢧⣙⣦⣝⣮⢳⡝⣮⢷⣹⡞⣷⡽⣞⡷⣯⣟⣿⣽⣾⢿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⢲⡭⢳⡍⢶⡹⣌⠳⣄⠳⣀⢓⡰⣀⠎⡰⢡⠐⡡⢌⠢⡑⢂⠔⡂⢅⠢⡅⠎⡆⣍⠲⣡⡶⠟⣛⣩⣭⣴⣦⣼⣤⣮⣭⣛⣻⢾⣧⣷⢻⣧⢿⣽⣻⢷⣯⣟⣾⢿⣿⣻⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⣿⢧⣛⢧⣞⡣⣗⢬⠳⣌⠳⣌⠦⡑⢆⡚⡰⣁⢚⡐⢢⡑⡘⢤⠚⣄⢋⠴⣡⢋⠔⣢⡿⢋⣴⣾⠟⠋⠉⠉⠹⣿⣟⢿⠹⡟⠻⣷⣮⢻⣟⣾⣻⢾⣽⣻⣞⣯⣿⢿⣻⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⢯⣞⣳⢎⡷⣎⣏⢷⣊⠷⣘⠶⡙⢦⡱⠱⣌⠦⡙⢦⠱⣉⢆⠳⣌⡚⢦⡃⢎⣼⢻⣴⠿⢿⡋⠀⠀⠀⠀⠀⠹⡏⠀⠀⠀⠀⠘⢿⣷⣹⣾⡽⣟⣯⣷⣻⣯⣿⡿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣟⡾⣭⣟⢾⡵⢮⡳⣭⢏⡧⣏⡝⣦⣙⠳⣌⠶⣙⢦⢛⡬⢎⡳⡬⡝⣦⢣⣾⣳⠟⠁⠀⠘⡅⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠈⣿⣷⣻⣟⡿⣿⡷⣯⢷⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣯⣟⡷⣯⣟⡾⣏⡷⡽⣎⢷⡹⣞⢦⣝⣣⡝⢮⡵⣊⠷⣼⣇⢿⣱⣹⢇⣻⣾⠋⠀⠀⠀⠀⠁⠀⠀⠀⠀⢀⠀⡁⢀⠀⡀⠀⠀⠀⢸⢻⣷⢿⣟⣿⣿⢿⣟⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣯⢿⣳⣯⢿⡽⣽⢯⣽⣫⢷⣹⡞⣼⡱⣞⢧⡳⣭⢻⣿⣾⣻⢧⡟⣼⣿⣿⣷⣾⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⢿⣽⣯⣿⣽⣻⢾⣭⣟⣧⣟⣧⣟⢮⡷⣹⢮⣿⣿⣷⣟⣾⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣷⣿⢾⣯⡿⣾⡽⣞⡾⣵⣞⣯⢷⢯⣿⣟⣾⣿⣹⣷⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣾⣿⣿⣽⣷⡿⣯⣟⣷⣻⣞⣯⣟⣾⢿⣿⡿⣿⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢏⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⢿⣽⣾⣷⣻⣾⣽⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣽⣿⣿⣿⣿⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣷⣿⣻⣾⢿⣟⣿⣿⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣯⣿⢿⣿⣻⣯⣿⢿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣹⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣟⣿⣟⣯⡿⣟⣿⣻⣽⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣷⣿⣿⣿⣿⣟⣿⣾⣻⢷⣯⢿⣽⣻⣽⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣿⣿⣿⣯⣿⣿⢯⣿⢾⣻⢾⣝⣻⢮⡟⣞⡷⣿⠿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⡿⣽⣟⡿⣽⢏⡟⡾⣜⢧⡻⣜⣯⣾⣿⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⡖⠦⢤⡀⢀⣀⡤⣶⠟⠋⣉⡹⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣻⣟⡾⣝⢧⡻⣜⣣⡝⣶⣹⡾⠿⣉⣭⣉⢹⢿⣶⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠋⠁⠀⠉⠉⠛⠻⠽⢿⣿⣶⡶⠿⠟⠔⠒⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⠿⢿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠻⢿⠛⠛⣿⣿⣿⡿⣟⣧⢻⠼⣩⢞⡱⢞⡴⣹⡾⢟⣤⣤⣄⡀⠈⠹⠦⢀⣈⡉⠛⠻⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠿⣿⣿⣿⣿⡿⣿⡀⡴⠀⠀⠀⠀⢹⠀⠀⠀⠀⠈⣅⠀⠀⠀⠀⠹⡄⠀⠀⠀⠸⠀⠀⠀⠀⠘⡆⢰⣿⢿⡿⣽⣛⢆⢫⡜⢧⡞⣭⣿⣾⠿⠗⠚⠋⠉⠉⠉⠃⠓⠲⠤⡬⢿⡷⣤⡤⠿⠿⠗⠒⠒⠠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣷⣀⠀⢀⠀⣿⠀⠀⠀⠀⠀⣱⠀⠀⠀⠀⠀⡇⠀⠀⠀⢀⣇⠀⠀⠀⣆⣿⣿⠿⢹⠛⣤⣙⢮⣧⣿⣯⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡶⣾⡿⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣛⠶⡤⣄⢀⠀⡀⠀⠀⠀⠀⢀⠺⢿⣿⣿⣿⣿⣿⣿⣿⣼⣿⠦⣤⣤⣀⣼⣿⣦⣀⣀⣄⣿⣿⣦⣤⣦⣿⣿⣷⣾⡿⢿⠫⠉⢌⣰⣻⣶⣿⣿⣿⣿⢋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⠁⠈⠙⢿⡒⠤⣤⣤⣀⣀⣰⣛⣋⣽⠷⢾⣭⣵⣊⣎⠳⣔⢢⡒⣌⠲⣌⢳⢫⣿⣿⣿⣿⣾⣽⣟⣿⣿⣿⣿⣿⣿⣿⣶⣶⣾⣾⣿⣷⣾⣶⣶⢯⠛⡉⠊⢁⢈⣠⢴⣞⣯⣿⡿⢟⢯⣱⣿⢳⢎⡲⢄⢢⡀⣄⢠⣄⠲⡜⡼⣹⢷⣻⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣌⣿⣷⣾⣷⠀⠀⢀⣽⠿⣟⣉⡡⣄⡀⠀⠀⠈⢛⣿⣷⣼⣤⡓⣌⠳⡘⢣⢋⣿⣧⢏⡟⣿⣻⢿⣾⣷⣯⣯⡽⣍⠯⡹⠉⠏⠑⠉⠌⠁⢁⣈⣠⣴⣰⣷⣾⣿⣿⡿⣟⡟⢧⡹⢎⢖⣿⡏⢓⠮⡱⢋⠖⡱⢌⣣⣎⣷⣽⠶⠷⠞⠻⢯⣛⣿⢦⡀⠀⠀⢀⣀⣀⣤⣾⣿⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡿⢻⣿⣶⣤⠋⠁⠀⠈⠉⠛⠷⣮⣄⠤⣰⠟⠁⠀⠀⠈⠻⣷⣷⠟⠛⠛⠛⢻⡎⠘⠥⠋⢯⠹⡙⢯⡛⠿⠿⢿⠿⡿⢿⡿⣿⢿⡿⢿⠿⢿⠻⣟⠻⢏⠛⠜⠣⠉⠜⠁⠈⢀⣾⠛⠛⠛⠶⣥⣯⣾⠟⠛⠛⠛⢿⡀⠀⠀⢀⡄⡲⢌⣙⢯⣟⠛⣻⣿⣿⢿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣧⣀⡁⢹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠙⡿⠋⠀⡀⡄⢤⡀⣰⣿⣧⠀⠀⠀⠀⠀⢻⡀⠀⠀⠀⠀⠁⠀⠈⠀⠉⠀⠁⠘⠀⠂⠐⠂⠈⠀⠉⠀⠁⠀⠀⠀⠈⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀⠀⠀⣸⣿⡃⢀⠀⠀⠀⠈⢷⡀⣄⡾⠾⠛⠋⠉⠀⠈⠻⣿⣿⣏⣈⣾⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣼⣁⡳⣄⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠙⠻⢶⣗⣼⣿⣿⡄⠀⢄⣢⣔⡈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣡⣆⠆⠠⠀⢠⣿⣿⡿⣌⢞⣰⣦⠀⠈⢳⡉⠀⠀⠀⠀⠀⠀⠀⠀⣹⡿⢿⣿⣿⣿⣾⣿⣯⣦⡀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⡿⢿⡋⠉⣡⣴⣾⣿⠿⠉⠉⠒⠲⢶⣾⡇⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⠁⠀⠀⠀⠈⠹⢻⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⣾⠟⠋⠀⠀⠀⠀⣸⣿⢧⡿⠚⠉⠁⠀⠀⠀⠀⠳⡄⠀⠀⠀⠀⠀⣀⣴⣿⣷⣶⣮⡄⠉⢻⣿⣿⠿⣟⣦⡄⡀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡈⠻⠐⣾⣿⣿⡃⠀⠀⠀⠀⠠⠀⠈⣷⣄⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡄⠀⠀⠀⠀⠀⣼⠇⠂⠄⣀⠀⠀⠀⠰⠖⠒⣲⣶⢾⣾⣖⣶⣿⣿⣿⣶⣞⠒⠄⠒⠂⠒⢀⣄⣰⢿⡄⠀⠀⠀⠀⠠⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⣷⣶⡶⠖⠛⠋⠁⠀⠘⣿⣿⣿⣠⢾⣩⣿⣿⣿⢯⣻⣇⠀⠀⠀⠀\n⠀⠀⠀⢀⣤⣤⣶⣿⣿⣿⣿⣿⣟⡃⠀⢿⣅⠙⠛⢷⣦⣠⣤⣤⡀⠀⢀⣀⣹⡻⣷⣦⣤⣤⣤⣾⣿⣿⣿⣿⣄⣀⣀⣠⣿⣿⠀⠀⠀⠈⠙⣦⣤⢤⡖⠺⠉⠉⣩⣧⣌⣠⣈⣏⡋⣹⣿⡗⣶⣒⣶⣿⡿⣿⣿⣾⣿⣦⣀⣀⣀⣾⣿⣿⣿⣦⣀⠀⢀⣀⣀⣠⣴⣾⡿⡁⢀⠀⠀⠀⣀⣀⣴⣾⣿⢻⣿⡟⠀⢰⣿⣿⣿⣿⣿⣿⣀⠀⠀⠀")
            sys.exit()
        else:
            screen[player_x][player_y] = 3



        self.grid = screen
        return maps[current_map], current_map


class Sidescreen:
    def __init__(self, passed_inventory, passed_dimensions):
        self.dimensions = passed_dimensions
        self.lives = 3
        #self.inventory_screen = passed_inventory.inventory_screen
        self.array = self.generate_array(passed_inventory.inventory_screen)
    
    def generate_array(self, inventory_screen):
        #determine the section of screen to allocate for the inventory, paste the fetched inventory array into the allocated section
        return np.zeros(self.dimensions)



class Map:
    def __init__(self, passed_height, passed_width, passed_level):
        self.dimensions = passed_height, passed_width
        self.array = self.generate_floor(passed_level)
    
    
    def generate_section(self, start, end, floor_number, shared_map_name):
        height, width = self.dimensions
        
        existing_shared_map = multiprocessing.shared_memory.SharedMemory(name=shared_map_name)
        shared_map_array = np.ndarray((height, width), dtype='int32', buffer=existing_shared_map.buf)

        for y in range(start, end):
            section_row = []
            for x in range(width):
                tile_color = 1
                if (x - (width // 2)) ** 2 + ((y - (height // 2)) * 1.2) ** 2 <= 23 ** 2:
                    tile_color = 2
                    if (x - (width // 2)) ** 2 + ((y - (height // 2)) * 1.2) ** 2 <= 21.75 ** 2:
                        if random(1, 30) == 1 and x != 22 and y != 30:
                            tile_color = 9
                        else:
                            if noise(x, y, self) == 0:
                                dark_tile, light_tile = 4, 6
                                tile_color = (
                                    (x - 1) % 2 == 0 and
                                    (y % 2 == 0 and dark_tile or light_tile) or
                                    (y % 2 == 0 and light_tile or dark_tile)
                                )
                            else:
                                tile_color = 1
                else:
                    tile_color = 1
                #place exit flag
                if x == 30 and y == 40:
                    tile_color = 8

                section_row.append(tile_color)
            shared_map_array[y, :] = section_row

        existing_shared_map.close()

    def generate_floor(self, floor_number):
        height, width = self.dimensions

        sections = 3
        processes = []

        shared_map = multiprocessing.shared_memory.SharedMemory(create=True, size=height * width * np.dtype('int32').itemsize)
        shared_map_array = np.ndarray((height, width), dtype='int32', buffer=shared_map.buf)
        shared_map_array[:] = 1  #start with a blank array of black cells

        #divide the work into sections and spawn processes
        section_height = height // sections
        for section_index in range(sections):
            start_row = section_index * section_height
            end_row = start_row + section_height if section_index < sections - 1 else height

            p = multiprocessing.Process(
                target=self.generate_section,
                args=(start_row, end_row, floor_number, shared_map.name)
            )
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        result = shared_map_array.copy()

        shared_map.close()
        shared_map.unlink()

        return result.tolist()
    '''

    def generate_section(self, start, end, floor_number, map_array):
        height, width = self.dimensions
        #section_array = []
        for y in range(start, end):
            section_row = []
            for x in range(width):
                tile_color = 1
                match floor_number:
                    case 1: #basic circle ----------------------------------------------------------------

                        if (x-(width // 2))**2 + ((y-(height // 2)) * 1.2)**2 <= 23**2:
                            tile_color = 2
                            if (x-(width // 2))**2 + ((y-(height // 2)) * 1.2)**2 <= 21.75**2:
                                if noise(x, y, self) == 0:
                        
                                    dark_tile, light_tile = 4, 6
                                    tile_color = (x - 1) % 2 == 0 and (y % 2 == 0 and dark_tile or light_tile) or (y % 2 == 0 and light_tile or dark_tile)
                                else:
                                    tile_color = 1
                        else:
                            tile_color = 1

                    case 2: #-----------------------------------------------------------------------------
                        pass
                    case 3: #-----------------------------------------------------------------------------
                        pass
                section_row += [tile_color]
            #map_array += [section_row]
            #print(y)
            #print(map_array)
            #print(section_row)
            map_array[y] = section_row
            #sys.exit()
        #return map_array

    def generate_floor(self, floor_number):
        height, width = self.dimensions
        

        sections = 3
        processes = []

        #shared array all processes write to
        shared_map_array = np.ones(height, dtype=int).tolist()
        #map_array = np.ones(height, dtype=int).tolist()

        for i in range(0, height + 0, height // sections):
            i += height // sections
            #p = multiprocessing.Process(target=self.generate_section, args=(i - height // sections, i, floor_number, shared_map_array))
            #processes.append(p)
            #p.start()
            self.generate_section(i - height // sections, i, floor_number, shared_map_array)

        #for p in processes:
            #p.join()

        return shared_map_array
    '''

class Player:
    def __init__(self, passed_inventory):
        self.position = (22, 30) #initial player position
        self.inventory = passed_inventory
    
    def move(self, direction, map):
        x, y = self.position #player position
        d_x, d_y = direction #direction x and y

        #player class handles erasure of rock tiles
        unit_destination = (x + d_x, y + d_y)
        destination_material = map.array[unit_destination[0]][unit_destination[1]]
        if destination_material in [4, 6, 8, 9]: #destination is not rock, take a single step
            self.position = unit_destination
            convert_to_floor_tile(x, y, map.array)
        elif destination_material == 1:#drill into rock until anything but tiles[1] is reached
            scale_factor = 2
            while True:
                destination = (x + (d_x * scale_factor), y + (d_y * scale_factor))
                destination_material = map.array[destination[0]][destination[1]]
                if destination_material in [4, 6, 8, 9]: #end of rock has been reached
                    self.position = destination
                    #convert the final rock cell into a floor cell
                    tunnel_x, tunnel_y = (x + (d_x * (scale_factor - 1)), y + (d_y * (scale_factor - 1)))
                    convert_to_floor_tile(tunnel_x, tunnel_y, map.array)
                    break
                elif destination_material != 1: #non rock entity reached, stop one block before it
                    destination_x, destination_y = (x + (d_x * (scale_factor - 1)), y + (d_y * (scale_factor - 1)))
                    self.position = (destination_x, destination_y)
                    convert_to_floor_tile(destination_x, destination_y, map.array)
                    break
                else:
                    #still drilling through rock, replace rock with ground
                    tunnel_x, tunnel_y = (x + (d_x * (scale_factor - 1)), y + (d_y * (scale_factor - 1)))
                    convert_to_floor_tile(tunnel_x, tunnel_y, map.array)
                
                scale_factor += 1
            
        else: #map border, do not drill
            pass
        #either move until an obstruction is reached, or move a set unit


class Inventory:
    def __init__(self):
        self.items = []
        self.inventory_screen = self.generate_inventory_screen()

    def generate_inventory_screen(self): #generate the inventory part of the sidescreen
        return


class NPC: #enemies & merchants
    def __init__(self, passed_type):
        self.type = passed_type