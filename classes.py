import numpy as np
from noise import pnoise2



#map region calculation functions ---------------------------------------------------------------------------------------------------------------

def noise(x, y, map):
    height, width = map.dimensions
    scale = 8
    result = pnoise2(x / scale, y / scale, octaves=1, persistence=0, lacunarity=0, repeatx=width, repeaty=height, base=7)
    #print((result))
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
    "⚿ ",
    "♝ ",
    "♜ ",
    "♞ ",
    "✠ ",
    "✤ ",
    "✦ ",
    "♚ ",
    "♛ ",
    "ጨጭጮ",
    "౷",
    "⚠ ",
    "⚑ ",
    "⚐ "
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
                    case 3: #3 4 3 circle arrangement
                        #-----------------------------------------------------------------------------
                        pass
                        #-----------------------------------------------------------------------------
                map_row += [tile_color]
            map_array += [map_row]
        return map_array
    

class Player:
    def __init__(self, passed_inventory):
        self.position = (22, 30) #initial player position
        self.inventory = passed_inventory
    
    def move(self, direction, map):
        x, y = self.position #player position
        d_x, d_y = direction #direction x and y

        unit_destination = (x + d_x, y + d_y)
        destination_material = map.array[unit_destination[0]][unit_destination[1]]
        if destination_material in [4, 6]: #destination is not rock, take a single step
            self.position = unit_destination
            convert_to_floor_tile(x, y, map.array)
        elif destination_material == 1:#drill into rock until anything but tiles[1] is reached
            scale_factor = 2
            while True:
                destination = (x + (d_x * scale_factor), y + (d_y * scale_factor))
                destination_material = map.array[destination[0]][destination[1]]
                if destination_material in [4, 6]: #end of rock has been reached
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
                    #print("rock!", x, y)
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

    def generate_inventory_screen(self):
        return