from settings import *

text_map_old = [
    'WWWWWWWWWWWWWW',
    'W......W.....W',
    'W..WW.W..W.W.W',
    'W.......WW.W.W',
    'W..W....W..W.W',
    'W..W...WWW.W.W',
    'W............W',
    'WWWWWWWWWWWWWW'
]

# 20x16
text_map = [
    'WWWWWWWWWWWWWWWWWWWW', #1
    'W............W.....W', #2
    'WWW..WWWW....W.....W', #3
    'W............W...WWW', #4
    'W............W.....W', #5
    'W......WW..........W', #6
    'WWW..WWWW....W....WW', #7
    'W......W.....W.....W', #8
    'W......W.....WWW...W', #9
    'W....W.....W.......W', #10
    'W..................W', #11
    'W..WWW.....WWW.....W', #12
    'W..................W', #13
    'W.......WWW......W.W', #14
    'W..................W', #15
    'WWWWWWWWWWWWWWWWWWWW', #16
]

world_map = set()
mini_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == 'W':
            world_map.add((i * TILE, j * TILE))
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
