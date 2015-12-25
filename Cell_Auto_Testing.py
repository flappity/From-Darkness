import libtcodpy as libtcod
import random
import copy

initial_chance = .4

# Chance for a wall to remain a wall.
# If there's between min_to_stay_alive and max_to_stay_alive walls around it, it stays alive. Otherwise it becomes a floor.
min_to_stay_alive = 5
max_to_stay_alive = 9

# Chance for a floor to become a wall.
# If there is between min_to_come_alive and max_to_come_alive walls around it, it turns into a wall.
min_to_come_alive = 3
max_to_come_alive = 8

# Alternate method of birth/death rates
# If a floor has this many walls touching it, it becomes a wall.
birth_limit = 4

# If a wall doesn't have this many walls touching it, it becomes a floor
death_limit = 3

num_iterations = 3

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

def generate_cave(map_obj):
    # First, add two invisible maps to the Map object.
    # ref_map is the map that all the checking is done on,
    # grown_map is the map that is written to.
    map_obj.ref_map = [[cell_init() for y in range(map_obj.height)] for x in range(map_obj.width)]
    map_obj.grown_map = copy.deepcopy(map_obj.ref_map)

    for iteration in range(num_iterations):
        process_cell_cycle(map_obj)

    for x in range(map_obj.width):
        for y in range(map_obj.height):
            if not map_obj.grown_map[x][y]:
                map_obj.array[x][y].blocked = False
                map_obj.array[x][y].block_sight = False

# Returns true or false based on initial_chance
def cell_init():
    if random.random() <= initial_chance:
        return True
    else:
        return False

# Returns True if a cell is born/stays alive, false if it dies/stays dead.
# Checks starting state of the cell, and its neighbors (3x3 square around the initial cell)
# If it is alive:
#   If neighbors is outside the range of min_to_stay_alive to max_to_stay_alive, it dies.
#   Otherwise it lives.
# If it is dead:
#   If neighbors is between min_to_come_alive and max_to_come_alive, it comes to life.
#   If not, it's deader than dead still.
# This function returns the cell's new status: True if it ends alive, False if it ends dead.
def cell_process(map_obj, x, y):
    neighbors = cell_get_neighbors(map_obj, x, y)
    #print str(neighbors) + " = " + str(x) + ", " + str(y)
    cell_alive = map_obj.ref_map[x][y]

    # Cell starts alive
    if cell_alive:

        # # death_limit method
        if neighbors <= death_limit:
            return False
        else:
            return True

        # min_to_stay_alive and max_to_stay_alive method
        # if neighbors < min_to_stay_alive or neighbors > max_to_stay_alive:
        #     return False
        # elif neighbors >= min_to_stay_alive and neighbors <= max_to_stay_alive:
        #     return True

    # Cell starts dead (floor)
    else:

        # # birth_limit method
        if neighbors >= birth_limit:
            return True
        else:
            return False

        # # min_to_come_alive and max_to_come_alive method
        # if neighbors >= min_to_come_alive and neighbors <= max_to_come_alive:
        #     return True
        # elif neighbors < min_to_come_alive or neighbors > max_to_come_alive:
        #     return False

# This function counts live cells in a 3x3 area centered on x, y.
# It checks ref_map, since grown_map is going to be updated with each process_cell_cycle step.
def cell_get_neighbors(map_obj, x, y):
    count = 0
    for test_x in range(x-1, x+2):
        for test_y in range(y-1, y+2):
            if test_x < 0 or test_x >= map_obj.width or test_y < 0 or test_y >= map_obj.height:
                count += 1
            elif test_x == x and test_y == y:
                continue
            else:
                if map_obj.ref_map[test_x][test_y]:
                    count += 1
    return count

# This runs cell_process on each cell in the map, starting at 0,0 and ending at map.width, map.height.
# It writes the new cell states to grown_map, and then copies grown_map over to ref_map in preparation of a new cycle.
def process_cell_cycle(map_obj):
    for x in range(map_obj.width):
        for y in range(map_obj.height):
            map_obj.grown_map[x][y] = cell_process(map_obj, x, y)
    map_obj.ref_map = copy.deepcopy(map_obj.grown_map)

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
                libtcod.console_put_char(0, x, y, '#')
            elif not cave_map.array[x][y].blocked:
                libtcod.console_put_char(0, x, y, '.')

    libtcod.console_flush()

    key = libtcod.console_wait_for_keypress(False)

    if key.vk == libtcod.KEY_ESCAPE:
        break


