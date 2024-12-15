import numpy as np
from noise import pnoise2 #noise must be installed via pip3

'''
screen = np.zeros((5, 5))
array = np.array([[23, 46, 85],
    [43, 56, 99],
    [11, 34, 55]])
screen[:3, :3] = array
print(screen)'''


#map region calculation functions ---------------------------------------------------------------------------------------------------------------

def noise(x, y, map):
    height, width = map.dimensions
    scale = 8
    result = pnoise2(x / scale, y / scale, octaves=1, persistence=0, lacunarity=0, repeatx=width, repeaty=height, base=7)
    #print((result))
    return 1 - min(round(result * 10), 1)


def within_castle(x, y, y_sf, a, b, r, depth): # (x-a)**2 + ((y-b) * y_sf)**2 <= r**2        checks for main body, then each tower
    
    if depth == 0:#only apply on the first iteration of the function
        #get x and y relative to the centre (int of y for unique curvature)
        x, y = x - a, int((y-b) * y_sf)
    depth += 1

     #do not go any deeper for the towers
    if depth == 2: return ((x)**2 + (y)**2 <= r**2) #tower shape calculation

    #lies_within_main_body = False#((x)**2 + (y)**2 <= r**2) #main body shape calculation
    path_thickness = 4.5
    gradient = 0.8

    #check for inner body & 4 connecting paths clamped at map edges
    #((x)**2 + (y)**2 <= (r / 1.5)**2) or ---- former circle

    path_one = ((-gradient * x + path_thickness >= y and -gradient * x - path_thickness <= y) and x > -20 and x < 20 and y > -20 and y < 20)
    path_two = ((gradient * x + path_thickness >= y and gradient * x - path_thickness <= y) and x > -20 and x < 20 and y > -20 and y < 20)
    lies_within_main_body = path_one or path_two
    if lies_within_main_body: return True

    #adjust variables for the smaller towers
    dist_sf = 2
    radial_sf = 2.4
    r /= radial_sf

    within_north_towers = within_castle(x - (dist_sf * r), y + (dist_sf * (r / y_sf)), y_sf, a, b, r, depth) or within_castle(x + (dist_sf * r), y + (dist_sf * (r / y_sf)), y_sf, a, b, r, depth)
    within_south_towers = within_castle(x - (dist_sf * r), y - (dist_sf * (r / y_sf)), y_sf, a, b, r, depth) or within_castle(x + (dist_sf * r), y - (dist_sf * (r / y_sf)), y_sf, a, b, r, depth)

    return within_north_towers or within_south_towers


#variables -------------------------------------------------------------------------------------------------------------------------------------

tiles = [
    "  ",
    "██",
    "▓▓",
    "⏏ ",#ℹ۩۞
    "▒▒",
    "  ",
    "░░",
    "",
    "⌺ ",
    "♝ ",
    "♜ ",
    "♞ ",
    "✠ ",
    "✤ ",
    "✦ ",
    "ጨጭጮ",
    "౷"
]




#classes ---------------------------------------------------------------------------------------------------------------------------------------

class Screen:
    def __init__(self, passed_height, passed_width):
        self.dimensions = (passed_height, passed_width)
        self.grid = np.zeros((passed_height, passed_width))
    
    def add_elements_to_screen(self, elements): #0 = map, 1 = player, 2 = inventory, 3 = enemies, 4 = npc merchants, 5 = interactable items
        screen = self.grid

        map, player, inventory, enemies, merchants, items = elements

        #add map
        map_height, map_width = map.dimensions
        screen[:map_height, :map_width] = map.array

        #add player
        player_x, player_y = player.position
        screen[player_x][player_y] = 3



        self.grid = screen

    def display(self):
        screen = self.grid
        for row in screen:
            print("".join([(((i < 97) and tiles[min(int(i), len(tiles) - 1)]) or f"{chr(int(i))}") for i in row]))
            #text occupies exactly half the width of the generic pixel


class Map:
    def __init__(self, passed_height, passed_width, passed_level):
        self.dimensions = passed_height, passed_width
        self.array = self.generate_floor(passed_level)
    
    def generate_floor(self, floor_number):
        height, width = self.dimensions

        map_array = []
        for y in range(height):
            map_row = []
            for x in range(width):
                tile_color = 1
                match floor_number:
                    case 1: #
                        #basic circle ----------------------------------------------------------------
                        
                        if (x-(width // 2))**2 + ((y-(height // 2)) * 1.2)**2 <= 23**2:
                            tile_color = 2
                            if (x-(width // 2))**2 + ((y-(height // 2)) * 1.2)**2 <= 21.75**2:
                                if noise(x, y, self) == 0:
                                    #additional obstacles
                        
                                    dark_tile, light_tile = 4, 6
                                    tile_color = (x - 1) % 2 == 0 and (y % 2 == 0 and dark_tile or light_tile) or (y % 2 == 0 and light_tile or dark_tile)
                                else:
                                    tile_color = 1
                        else:
                            tile_color = 1
                        #-----------------------------------------------------------------------------
                    case 2: #castle
                        #-----------------------------------------------------------------------------
                        if within_castle(x, y, 1.2, width // 2, height // 2, 22, 0): 
                            #check for static objects (interior walls, doors)

                            #render a checkerboard floor pattern
                            tile_color = (x - 1) % 2 == 0 and (y % 2 == 0 and 2 or 5) or (y % 2 == 0 and 5 or 2)
                        else:
                            tile_color = 1 #black tile
                        
                        #-----------------------------------------------------------------------------
                    case 3:
                        #-----------------------------------------------------------------------------
                        pass
                        #-----------------------------------------------------------------------------
                map_row += [tile_color]
            map_array += [map_row]
        return map_array
    

class Player:
    def __init__(self):
        self.position = (22, 30) #initial player position
        self.inventory = Inventory()
    
    def move(self, direction, map):
        pass
        #either move until an obstruction is reached, or move a set unit


class Inventory:
    def __init__(self):
        self.items = []
        self.inventory_screen = self.generate_inventory_screen()

    def generate_inventory_screen(self):
        return