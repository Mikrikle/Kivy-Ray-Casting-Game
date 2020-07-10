from settings import *
from kivy.core.image import Image
from kivy.graphics import Color, Canvas, Rectangle, Line
from collections import deque


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'sprite_barrel': {
                'sprite': Image('sprites/barrel/base/0.png').texture,
                'viewing_angles': None,
                'shift': 1.8 + POS_DOWN,
                'scale': 0.4,
                'animation': deque(
                    [Image(f'sprites/barrel/anim/{i}.png').texture for i in range(12)]),
                'animation_dist': 800,
                'animation_speed': 10,
            },
            'sprite_pin': {
                'sprite': Image('sprites/pin/base/0.png').texture,
                'viewing_angles': None,
                'shift': 0.6 + POS_DOWN,
                'scale': 0.6,
                'animation': deque([Image(f'sprites/pin/anim/{i}.png').texture for i in range(8)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'sprite_devil': {
                'sprite': [Image(f'sprites/devil/base/{i}.png').texture for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2 + POS_DOWN,
                'scale': 1.1,
                'animation': deque(
                    [Image(f'sprites/devil/anim/{i}.png').texture for i in range(9)]),
                'animation_dist': 200,
                'animation_speed': 10,
                'blocked': True,
            },
            'sprite_flame': {
                'sprite': Image('sprites/flame/base/0.png').texture,
                'viewing_angles': None,
                'shift': 0.7 + POS_DOWN,
                'scale': 0.6,
                'animation': deque(
                    [Image(f'sprites/flame/anim/{i}.png').texture for i in range(16)]),
                'animation_dist': 800,
                'animation_speed': 5,
                'blocked': None,
            },
        }

        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['sprite_barrel'], (7.1, 2.1)),
            SpriteObject(self.sprite_parameters['sprite_barrel'], (5.9, 2.1)),
            SpriteObject(self.sprite_parameters['sprite_pin'], (8.7, 2.5)),
            SpriteObject(self.sprite_parameters['sprite_devil'], (7, 4)),
            SpriteObject(self.sprite_parameters['sprite_flame'], (8.6, 5.6))
        ]


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation']
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.x = pos[0] * TILE
        self.y = H - pos[1] * TILE - NULLY
        self.pos = self.x, self.y

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45))
                                  for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle,
                                     pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(
                int(PROJ_COEFF / distance_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            # choosing sprite for angle
            if self.viewing_angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            # sprite animation
            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            # sprite scale and pos
            sprite_pos = (current_ray * SCALE - half_proj_height + NULLX,
                          H - HALF_HEIGHT - half_proj_height + shift - TILE)  # + down / - up
            sprite = Rectangle(pos=sprite_pos, size=(
                proj_height, proj_height), texture=sprite_object)

            c = 1 / (1 + distance_to_sprite * distance_to_sprite * 0.00001)
            bg_color = Color(c, c, c, 1)

            return (distance_to_sprite, sprite, sprite_pos, bg_color)
        else:
            return (False,)
