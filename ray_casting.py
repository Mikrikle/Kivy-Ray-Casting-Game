import pygame
from settings import *
from worldmap import world_map
from kivy.graphics import Color, Canvas, Rectangle


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(sc, player_pos, player_angle, textures):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - HALF_FOV
    texture_v = 0
    texture_h = 0
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        # verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        # projection
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        try:
            proj_height = PROJ_COEFF / depth
        except ZeroDivisionError:
            proj_height = 360
        c = 1 / (1 + depth * depth * 0.00002)

        bg_color = Color(c-0.1, c-0.1, c-0.1, 1)
        pos = [(ray * SCALE) + NULLX, (HALF_HEIGHT - proj_height // 2) + NULLY]
        try:
            t = textures[texture].get_region(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        except KeyError:
            t = None
        rectangle = Rectangle(pos=pos, size=[SCALE, proj_height], texture=t)
        sc.add(bg_color)
        sc.add(rectangle)
        cur_angle += DELTA_ANGLE
