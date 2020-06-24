from settings import *
from ray_casting import ray_casting
from kivy.graphics import Color, Canvas, Rectangle, Line
from worldmap import mini_map
from kivy.core.image import Image
#from map import mini_map


class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.textures = {'1': Image('texture/1.png').texture,
                         '2': Image('texture/2.jpg').texture,
                         # 1200X400
                         'S': Image('texture/sky.png').texture
                         }

    def background(self, angle):
        # 0 - 1200 -> 0 - 120
        angdeg = math.degrees(angle)
        d = 0
        if angdeg > 0:
            r_angdeg = angdeg%360
            if r_angdeg > 180:
                d = 180-r_angdeg%180
            else:
                d = r_angdeg
        else:
            r_angdeg = angdeg%-360
            if r_angdeg < -180:
                d = -180-r_angdeg%-180
            else:
                d = r_angdeg
            
        texture_x1 = int(400+d*2)
        texture_x2 = int(800+d*2)

        # ground
        bg_color = Color(.1, .1, .1, 1)
        rectangle = Rectangle(pos=[NULLX, NULLY], size=[WIDTH, HALF_HEIGHT])
        self.sc.add(bg_color)
        self.sc.add(rectangle)

        # sky
        bg_color2 = Color(.3, .3, .6, .8)
        rectangle2 = Rectangle(
            pos=[NULLX, HALF_HEIGHT+NULLY], size=[WIDTH, HALF_HEIGHT],
            texture=self.textures['S'].get_region(texture_x1, 0, texture_x2, 400))
        self.sc.add(bg_color2)
        self.sc.add(rectangle2)

    def world(self, player_pos, player_angle):
        ray_casting(self.sc, player_pos, player_angle, self.textures)

    def mini_map(self, player):

        map_x, map_y =  player.x // MAP_SCALE, player.y // MAP_SCALE

        self.sc.add(Color(.8, 0, 0, 1))
        self.sc.add(Line( points=[NULLX+map_x, NULLY+map_y, NULLX+map_x + 12 * math.cos(player.angle), NULLY+map_y + 12 * math.sin(player.angle)] ))
        self.sc.add(
            Rectangle(pos=[NULLX+int(map_x)-3, NULLY+int(map_y)-3], size=[6, 6]))

        self.sc.add(Color(0, .8, 0, .5))
        for x, y in mini_map:
            self.sc.add(
                Rectangle(pos=[NULLX+x, NULLY+y], size=[MAP_TILE, MAP_TILE]))

    def sight(self):
        self.sc.add(Color(1, 0, 0, .5))
        self.sc.add(
            Rectangle(pos=[NULLX+HALF_WIDTH-5, NULLY+HALF_HEIGHT-5], size=(10, 10)))
