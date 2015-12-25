import libtcodpy as libtcod
import math
import textwrap
import shelve

# This class replaces globals. All the variables here are the CURRENT ones.
# Example:
# self.map will load the array from the proper Level object (the one the player is exploring).
# self.objects will be the list of objects for the level the player's on
# and so on. Essentially we're "saving" and "loading" levels by pulling the data from the proper Level
# object, and when we're done we update the Level object again.
class Game:
    def __init__(self):
        self.map = []
        self.maplist = {}
        self.objects = []

        self.FONT = 'meiryu_11.png'
        self.WINDOW_WIDTH = 110
        self.WINDOW_HEIGHT = 58
        self.VIEWPORT_WIDTH = 80
        self.VIEWPORT_HEIGHT = 45
        self.MAP_WIDTH = 100
        self.MAP_HEIGHT = 100

        self.player = None

    def create_game_window(self):
        libtcod.console_set_custom_font(self.FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, 'Roguelike Thing', False)
        libtcod.console_set_default_background(0, libtcod.black)
        libtcod.console_set_default_foreground(0, libtcod.white)
        self.viewport = libtcod.console_new(self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT)

    def blit_consoles_to_main(self):
        libtcod.console_blit(self.viewport, self.player.x - 40, self.player.y - 23, self.VIEWPORT_WIDTH, self.VIEWPORT_HEIGHT, 0, 20, 5)

    def spawn_player(self):
        self.player = Entity(int(self.VIEWPORT_WIDTH / 2), int(self.VIEWPORT_HEIGHT / 2), '@', 'You', libtcod.light_crimson)

    def spawn_entity(self, x, y, type):
        if type == 'passive':
            entity = Entity(x, y, '@', 'npc', libtcod.blue)


    def turn_loop(self):
        self.player_action = None
        self.key = libtcod.Key()
        self.mouse = libtcod.Mouse()
        while not libtcod.console_is_window_closed():
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, self.key, self.mouse)
            self.draw_objects()
            self.blit_consoles_to_main()
            libtcod.console_flush()
            self.clear_objects()
            self.input_action = self.handle_controls()
            if self.input_action == 'exit':
                break

    def handle_controls(self):
        #if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        if self.key.vk == libtcod.KEY_UP or self.key.vk == libtcod.KEY_KP8:
            self.player.move_or_attack(0,-1)
        elif self.key.vk == libtcod.KEY_RIGHT or self.key.vk == libtcod.KEY_KP6:
            self.player.move_or_attack(1,0)
        elif self.key.vk == libtcod.KEY_DOWN or self.key.vk == libtcod.KEY_KP2:
            self.player.move_or_attack(0,1)
        elif self.key.vk == libtcod.KEY_LEFT or self.key.vk == libtcod.KEY_KP4:
            self.player.move_or_attack(-1,0)
        elif self.key.vk == libtcod.KEY_KP7:
            self.player.move_or_attack(-1,-1)
        elif self.key.vk == libtcod.KEY_KP9:
            self.player.move_or_attack(1,-1)
        elif self.key.vk == libtcod.KEY_KP1:
            self.player.move_or_attack(-1,1)
        elif self.key.vk == libtcod.KEY_KP3:
            self.player.move_or_attack(1,1)
        elif self.key.vk == libtcod.KEY_ESCAPE:
            return 'exit'

    def draw_objects(self):
        for object in self.objects:
            object.draw()
            #libtcod.console_put_char(self.viewport, object.x, object.y, object.char)

    def clear_objects(self):
        for object in self.objects:
            object.clear()
            #libtcod.console_put_char(self.viewport, object.x, object.y, ' ')

class Level:
    def __init__(self, w, h, name):
        self.map = []
        for x in range(w):
            for y in range(h):
                map[x][y] = Tile(False)
        game_object.maplist[name] = self


class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        if block_sight is None:
            block_sight = blocked




class Entity:
    def __init__(self, x, y, char, name, fore_color=libtcod.white, back_color=libtcod.black):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.fore_color = fore_color
        self.back_color = back_color
        game_object.objects.append(self)

    def move_or_attack(self, x, y):
        self.x += x
        self.y += y

    def draw(self):
        libtcod.console_put_char_ex(game_object.viewport, self.x, self.y, self.char, self.fore_color, self.back_color)

    def clear(self):
        libtcod.console_put_char(game_object.viewport, self.x, self.y, ' ')

game_object = Game()
game_object.create_game_window()
game_object.spawn_player()
game_object.spawn_entity(libtcod.random_get_int(0, 1, game_object.VIEWPORT_WIDTH), libtcod.random_get_int(0, 1, game_object.VIEWPORT_HEIGHT), 'passive')
game_object.turn_loop()



#class Level:


#class Entity:


