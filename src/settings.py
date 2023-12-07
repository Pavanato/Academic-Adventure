level_map1 = [
'                              ',
'                              ',
'        x                     ',
' XX   XXX              XX     ',
' XX E         P           F   ',
' XXXX  N      XX      N   XX  ',
' XXXX  E    XX                ',
' XX    X  XXXX  N XXXNXXX     ',
'       X  XEXX    XXXXXXX     ',
'    XXXX  X N  X  XX   XXXX   ',
'XXXXXXXX  XXXXXX  XX   XXXX   ']

level_map2 = [
        "XXXXXXXXXXXXXXXXXXXX",
        "X                  X",
        "X                  X",
        "X      F   X       X",
        "X      X     X     X",
        "X                  X",
        "X     N    X    x  X",
        "X     XX           X",
        "X  X           X   X",
        "X           P      X",
        "XXXXXXXXXXXXXXXXXXXX",
    ]

level_list = [level_map1, level_map2]

tile_size = 64
screen_width = 1280
screen_height = len(level_map1) * tile_size
