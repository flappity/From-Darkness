import libtcodpy as libtcod

initial_chance = 40
survival_min = 3
survival_max = 8
birth_min = 6
birth_max = 8
num_iterations = 1

class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        if block_sight is None:
            block_sight = blocked


class Map:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.array = [[ Tile(True)
                        for y in range(self.height)]
                        for x in range(self.width)]
        self.ref_map = [[False for y in range(height)] for x in range(width)]
        self.grown_map = [[False for y in range(height)] for x in range(width)]

def generate_cave(map):
    # Fill the tempmap with 'wall' or 'floor'
    # The number after random_get_float is the probability that a tile is a wall.
    for x in range(map.width):
        for y in range(map.height):
            if libtcod.random_get_int(0,0,100) >= initial_chance:
                map.grown_map[x][y] = True
                map.ref_map[x][y] = True

    run_iterations(map)

    for x in range(map.width):
        for y in range(map.height):
            if not map.grown_map[x][y]:
                map.array[x][y].blocked = False
                map.array[x][y].block_sight = False

#def cell_grow(ref, grown, x, y, width, height):
def cell_grow(map, x, y):
    live_count = 0
    # Sees if the cells in a 3x3 square are alive or dead. True is alive (wall)
    # sets live_count to a running total of living adjacent cells.
    for check_x in range(x-1, x+2):
        for check_y in range(y-1, y+2):
            if check_x < 0 or check_x >= map.width or check_y < 0 or check_y >= map.height:
                live_count += 1
            elif check_x != x and check_y != y:
                if map.ref_map[check_x][check_y]:
                    live_count += 1
    # If the cell is alive - Does it have the right number of neighbors to stay alive?
    if map.ref_map[x][y] == True:
        if live_count < survival_min or live_count > survival_max:
            map.grown_map[x][y] = False
        elif live_count >= survival_min and live_count <= survival_max:
            map.grown_map[x][y] = True

    # If the cell is dead, does it have the right number of neighbors to come alive?
    elif map.ref_map[x][y] == False:
        if live_count >= birth_min and live_count <= birth_max:
            map.grown_map[x][y] = True
        else:
            map.grown_map[x][y] = False

def run_iterations(map):
    # Run this code block num_iterations times
    for iter in range(num_iterations):

        # We run cell_grow on each individual cell in order.
        # This will check the cell on ref[x][y], and put the result on grown[x][y]
        for x in range(map.width):
            for y in range(map.height):
                cell_grow(map, x, y)

        # Now that each cell has been "grown", we copy the grown map over to the ref map.
        map.ref_map = map.grown_map


cave_map = Map(75,75)
generate_cave(cave_map)

libtcod.console_set_custom_font('meiryu_11.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
libtcod.console_init_root(75, 75, 'Roguelike Thing', False)
libtcod.console_set_default_background(0, libtcod.black)
libtcod.console_set_default_foreground(0, libtcod.white)



while not libtcod.console_is_window_closed():
    for x in range(cave_map.width):
        for y in range(cave_map.height):
            if cave_map.array[x][y].blocked:
                libtcod.console_put_char(0, x, y, '.')
            elif not cave_map.array[x][y].blocked:
                libtcod.console_put_char(0, x, y, '#')

    libtcod.console_flush()

    key = libtcod.console_wait_for_keypress(False)

    if key.vk == libtcod.KEY_ESCAPE:
        break


