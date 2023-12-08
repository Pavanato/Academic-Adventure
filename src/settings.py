level_map1 = [
'                              ',
'                              ',
'        x                     ',
' XX   XXX              XX     ',
' XX E        P CC C       F   ',
' XXXX  N CC    XX     N   XX  ',
' XXXX  E    XX                ',
' XX    X  XXXX  N XXXNXXX  C  ',
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

tile_size = 64
screen_width = 1280
screen_height = len(level_map1) * tile_size
