import pygame
from settings import *
from worldmap import world_map
from kivy.graphics import  Color, Canvas, Rectangle


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(sc, player_pos, player_angle):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        # verticals
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in world_map:
                break
            x += dx * TILE

        # horizontals
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if mapping(x, y + dy) in world_map:
                break
            y += dy * TILE

        # projection
        depth = depth_v if depth_v < depth_h else depth_h
        depth *= math.cos(player_angle - cur_angle)
        proj_height = PROJ_COEFF / depth
        c = 1 / (1 + depth * depth * 0.00002)
        
        bg_color = Color(c, c // 2, c // 3,1)
        pos = [ray * SCALE,HALF_HEIGHT - proj_height // 2]
        rectangle = Rectangle(pos = pos, size = [SCALE, proj_height])
        sc.add(bg_color)
        sc.add(rectangle)
        cur_angle += DELTA_ANGLE
