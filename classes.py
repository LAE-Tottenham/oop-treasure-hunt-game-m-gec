import numpy as np

'''
screen = np.zeros((5, 5))
array = np.array([[23, 46, 85],
    [43, 56, 99],
    [11, 34, 55]])
screen[:3, :3] = array
print(screen)'''

tiles = [
    "  ",
    "██",
    "▓▓",
    "▒▒"
]

class Screen:
    def __init__(self, passed_height, passed_width):
        self.dimensions = (passed_height, passed_width)
        self.grid = np.zeros((passed_height, passed_width))
    
    def add_map_to_screen(self, map):
        screen = self.grid

        map_array = map.array
        map_width, map_height = map.dimensions

        screen[:map_width, :map_height] = map_array
        self.grid = screen

    def display(self):
        screen = self.grid
        for row in screen:
            print(row)


class Map:
    def __init__(self, passed_height, passed_width, passed_level):
        self.dimensions = passed_height, passed_width
        self.array = self.generate_floor(passed_level)
    
    def generate_floor(self, floor_number):
        height, width = self.dimensions
        map_array = np.array([])

        for y in range(height):
            map_row = np.array([])
            #for x in range(width):
            match floor_number:
                case 1:
                    #-----------------------------------------------------------------------------
                    map_row = [tiles[1] * width]
                    print(map_row[0])
                    #-----------------------------------------------------------------------------
                case 2:
                    #-----------------------------------------------------------------------------
                    pass
                    #-----------------------------------------------------------------------------
                case 3:
                    #-----------------------------------------------------------------------------
                    pass
                    #-----------------------------------------------------------------------------

            #map_array += [map_row]
        return map_array