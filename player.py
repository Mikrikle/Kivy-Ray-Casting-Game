from settings import *
import math
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout


class Player():
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.x, self.y = player_pos
        self.angle = player_angle

    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self, key):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        if key == 'w':
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
        if key == 's':
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
        if key == 'a':
            self.x += player_speed * sin_a
            self.y += -player_speed * cos_a
        if key == 'd':
            self.x += -player_speed * sin_a
            self.y += player_speed * cos_a
        if key == 'left':
            self.angle -= 0.02
        if key == 'right':
            self.angle += 0.02
