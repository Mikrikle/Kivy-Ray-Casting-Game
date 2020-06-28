from settings import *
from kivy.core.image import Image
from kivy.graphics import Color, Canvas, Rectangle, Line


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'barrel': Image('sprites/barrel/0.png').texture,
            'pedestal': Image('sprites/pedestal/0.png').texture,
            'devil': [Image(f'sprites/devil/{i}.png').texture for i in range(8)]
        }
        self.list_of_objects = [
            # (map pos  "column, row" ) (pos y "top") (scale)
            SpriteObject(self.sprite_types['barrel'],
                         True, (7.1, 2.1), 3.8, 0.4),
            SpriteObject(self.sprite_types['barrel'],
                         True, (5.9, 2.1), 3.8, 0.4),
            SpriteObject(
                self.sprite_types['pedestal'],
                        True, (8.8, 2.5), 3.2, 0.5),
            SpriteObject(
                self.sprite_types['pedestal'], 
                        True, (8.8, 5.6), 3.2, 0.5),
            SpriteObject(self.sprite_types['devil'], 
                        False, (7, 4), 1.5, 1),
        ]


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.object = object
        self.static = static
        self.x = pos[0] * TILE
        self.y = H - pos[1] * TILE - NULLY
        self.pos = self.x, self.y
        self.shift = shift
        self.scale = scale

        if not static:
            self.sprite_angles = [frozenset(range(i, i + 45))
                                  for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle,
                                     pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player, walls):
        fake_walls0 = [walls[0] for i in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for i in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

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
        if 0 <= fake_ray <= NUM_RAYS - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
            proj_height = min(
                int(PROJ_COEFF / distance_to_sprite * self.scale), 2 * HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if not self.static:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_pos = (current_ray * SCALE - half_proj_height + NULLX,
                          H - HALF_HEIGHT - half_proj_height + shift - TILE)  # + down / - up
            sprite = Rectangle(pos=sprite_pos, size=(
                proj_height, proj_height), texture=self.object)

            c = 1 / (1 + distance_to_sprite * distance_to_sprite * 0.00001)
            bg_color = Color(c, c, c, 1)

            return (distance_to_sprite, sprite, sprite_pos, bg_color)
        else:
            return (False,)
