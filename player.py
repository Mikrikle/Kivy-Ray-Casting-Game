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

    
    
    def lookbehind(self, key):
        if key == 'left':
            self.angle -= 0.02
        if key == 'right':
            self.angle += 0.02

        self.angle %= DOUBLE_PI
    
    def movement(self, joystick):

        def sign(num):
            return -1 if num < 0 else 1

        pad = joystick.pad
        padx = pad[0]
        pady = pad[1]
        if abs(padx) + abs(pady) > 1.01:
            s = (1 - (abs(padx) + abs(pady)))//2
            if padx < 0:
                padx = padx + s
                padx = padx % sign(padx)
            else:
                padx = padx - s
                padx = padx % sign(padx)
            if pady < 0:
                pady = pady + s
                pady = pady % sign(pady)
            else:
                pady = pady - s
                pady = pady % sign(pady)

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        if pady >= 0.1:
            self.x += player_speed * cos_a * pady
            self.y += player_speed * sin_a * pady
        if pady <= -0.1:
            self.x += -player_speed * cos_a * abs(pady)
            self.y += -player_speed * sin_a * abs(pady)
        if padx <= -0.1:
            self.x += player_speed * sin_a * abs(padx)
            self.y += -player_speed * cos_a * abs(padx)
        if padx >= 0.1:
            self.x += -player_speed * sin_a * padx
            self.y += player_speed * cos_a * padx

