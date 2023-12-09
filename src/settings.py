# level_map1 = [
# '                              ',
# '                              ',
# '        x                     ',
# ' XX   XXX              XX     ',
# ' XX E        P CC C CCCCC F   ',
# ' XXXX  N CCCCCCXX     N   XX  ',
# ' XXXX  E    XX                ',
# ' XX    X  XXXX  N XXXNXXX  C  ',
# '       X  XEXX    XXXXXXX     ',
# '    XXXX  X N  X  XX   XXXX   ',
# 'XXXXXXXX  XXXXXX  XX   XXXX   ']


from csv import reader

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        csv_reader = reader(map)
        for row in csv_reader:
            row = [' ' if cell == '-1' else 'X' if cell == '0' else cell for cell in row]
            terrain_map.append(''.join(row))
    return terrain_map
    


level_map2 = import_csv_layout(r"src\graphics\backgrounds\level_1\map_2.csv")

level_map1 = [
        "XXXXXXXXXXXXXXXXXXXX",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                  X",
        "X       C          X",
        "X                  X",
        "X              C   X",
        "X  C               X",
        "X          N       X",        
        "X      N   X       X",
        "X      X     X     X",
        "X         C     N  X",
        "X     F    X    x  X",
        "X   N XX           X",
        "X  X           X   X",
        "X         P        X",
        "XXXXXXXXXXXXXXXXXXXX",
    ]

list_of_questions = [
    {'text': 'What is the capital of France?', 'answers': ['Paris', 'London', 'Berlin', 0]},
    {'text': 'What is the square root of 16?', 'answers': ['4', '8', '2', 0]},
    {'text': 'Who wrote "To Kill a Mockingbird"?', 'answers': ['Harper Lee', 'George Orwell', 'J.K. Rowling', 0]},
    {'text': 'What is the chemical symbol for Hydrogen?', 'answers': ['H', 'He', 'Hy', 0]},
    {'text': 'Who painted the Mona Lisa?', 'answers': ['Leonardo da Vinci', 'Vincent van Gogh', 'Pablo Picasso', 0]},
    {'text': 'What is the largest planet in our solar system?', 'answers': ['Jupiter', 'Earth', 'Mars', 0]},
    {'text': 'What is the capital of Australia?', 'answers': ['Canberra', 'Sydney', 'Melbourne', 0]},
    {'text': 'Who discovered penicillin?', 'answers': ['Alexander Fleming', 'Marie Curie', 'Louis Pasteur', 0]},
    {'text': 'What is the tallest mountain in the world?', 'answers': ['Mount Everest', 'K2', 'Kilimanjaro', 0]},
    {'text': 'Who is the author of "1984"?', 'answers': ['George Orwell', 'Aldous Huxley', 'Ray Bradbury', 0]}
]


level_list = [level_map1, level_map2]

# Constants
FPS = 60
VERTICAL_TILE_NUMBER = 45
TILE_SIZE = 16
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = len(level_map1) * TILE_SIZE
