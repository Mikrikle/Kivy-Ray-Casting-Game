from settings import *
from ray_casting import ray_casting
from kivy.graphics import Color, Canvas, Rectangle, Line
from kivy.core.image import Image
from worldmap import world_map, mini_map


class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.textures = {1: Image('texture/wall3.png').texture,
                         2: Image('texture/wall4.png').texture,
                         3: Image('texture/wall5.png').texture,
                         4: Image('texture/wall6.png').texture,
                         # 1200X600
                         'S': Image('texture/sky1.png').texture,
                         'G': Image('texture/ground.jpg').texture,
                         }

    def field(self, player):
        self.sc.add(Color(0, 0, 1, .5))
        p = Rectangle(pos=(NULLX + int(player.x)-6, H -
                           int(player.y)-6), size=(12, 12))
        l = Line(points=[
            NULLX+player.pos[0], H - player.pos[1],
            NULLX + (player.x + WIDTH*math.cos(player.angle)), H -
            (player.y + WIDTH*math.sin(player.angle))
        ])

        self.sc.add(p)
        self.sc.add(l)
        for x, y in world_map:
            r = Rectangle(pos=(x+NULLX,  H - y - TILE), size=(TILE, TILE))
            self.sc.add(r)

    def background(self, angle):
        # 0 - 1200 -> 0 - 120
        angdeg = math.degrees(angle)
        d = 0
        if angdeg > 0:
            r_angdeg = angdeg % 360
            if r_angdeg > 180:
                d = 180-r_angdeg % 180
            else:
                d = r_angdeg
        else:
            r_angdeg = angdeg % -360
            if r_angdeg < -180:
                d = -180-r_angdeg % -180
            else:
                d = r_angdeg

        texture_x1 = int(300+d)
        texture_x2 = int(600+d)

        # ground
        bg_color = Color(.1, .1, .1, 1)
        rectangle = Rectangle(pos=[NULLX, NULLY], size=[
                              WIDTH, HALF_HEIGHT], texture=self.textures['G'])
        self.sc.add(bg_color)
        self.sc.add(rectangle)

        # sky
        bg_color2 = Color(.3, .3, .6, .8)
        rectangle2 = Rectangle(
            pos=[NULLX, HALF_HEIGHT+NULLY], size=[WIDTH, HALF_HEIGHT],
            texture=self.textures['S'].get_region(texture_x1, 0, texture_x2, 400))
        self.sc.add(bg_color2)
        self.sc.add(rectangle2)

    def world(self, world_objects):
        #self.sc.add(Color(.5, .5, .5, 1))
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos, color = obj
                object.pos = (object_pos[0], H-object_pos[1])
                self.sc.add(color)
                self.sc.add(object)

    def mini_map(self, player):
        # 75 50
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        self.sc.add(Color(.5, .8, .5, .8))

        self.sc.add(Line(
            points=[
                NULLX+map_x, H - map_y,
                    NULLX + (map_x + 10 * math.cos(player.angle)), H - (map_y + 10 * math.sin(player.angle))]
        ))
        self.sc.add(
            Rectangle(pos=[NULLX+int(map_x)-3, H - int(map_y)-3], size=[6, 6]))

        self.sc.add(Color(.2, .3, .2, .6))
        for x, y in mini_map:
            self.sc.add(
                Rectangle(pos=[NULLX+x,  HEIGHT-y+NULLY-MAP_SCALE], size=[MAP_TILE, MAP_TILE]))

    def sight(self):
        self.sc.add(Color(1, 0, 0, .5))
        self.sc.add(
            Rectangle(pos=[NULLX+HALF_WIDTH-5, NULLY+HALF_HEIGHT-5], size=(10, 10)))
