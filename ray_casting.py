from settings import *
from worldmap import world_map, WORLD_WIDTH, WORLD_HEIGHT
from kivy.graphics import Color, Canvas, Rectangle


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(player, textures):
    walls = []
    ox, oy = player.pos
    xm, ym = mapping(ox, oy)
    cur_angle = player.angle - HALF_FOV
    texture_v, texture_h = 1, 1
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
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (
            depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= math.cos(player.angle - cur_angle)
        depth = max(depth, 0.00001)

        proj_height = min(int(PROJ_COEFF / depth), PENTA_HEIGHT)

        c = 1 / (1 + depth * depth * DIST_COLOR * 0.000001)
        bg_color = Color(c, c, c, 1)
        

        wall_pos = [(ray * SCALE) + NULLX,
                    H-(HALF_HEIGHT - proj_height // 2)-TILE]
        try:
            t = textures[texture].get_region(
                offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        except KeyError:
            t = None

        wall_column = Rectangle(
            pos=wall_pos, size=[SCALE, proj_height], texture=t)
        walls.append((depth, wall_column, wall_pos, bg_color))
        cur_angle += DELTA_ANGLE

    return walls
