from csv import reader

# Local function
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        csv_reader = reader(map)
        for row in csv_reader:
            row = [' ' if cell == '-1' else 'X' if cell == '0' else cell for cell in row]
            terrain_map.append(''.join(row))
    return terrain_map
    

level_map1 = import_csv_layout(r"src\graphics\backgrounds\level_1\school_map.csv")

level_map2 = [
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
    {'text': 'Calculate 2 + 5?', 'answers': ['8', '7', '10', 1]},
    {'text': 'What is the square root of 169?', 'answers': ['13', '17', '19', 0]},
    {'text': 'Calculate the sum of the first 5 even numbers?', 'answers': ['10', '20', '22', 1]},
    {'text': 'Is zero a integer number?', 'answers': ['Yes', 'No', 'Zero is not a number', 0]},
    {'text': 'Calculate the expression ((1 + 2)/3) + 1', 'answers': ['1', '2', '4', 1]},
    {'text': "What is the fifth Fibonacci number? (Remember that Fibonacci's sequence begins with 0 and 1)", 'answers': ['2', '3', '5', 1]},
    {'text': 'Every square is a rectangle?', 'answers': ['Yes', 'No', 0]},
    {'text': 'What is the shape of xy = 1 in the cartesian plane?', 'answers': ['Elipse', 'Parabola', 'Hyperbole', 2]},
    {'text': 'Limit of x tending to zero of sinx / x', 'answers': ['Infinity', '0', '1', 2]},
    {'text': '(Piano Question) How many movies are in The Twilight Saga?', 'answers': ['3', '4', '5', 2]}
]


level_list = [level_map1, level_map2]

# Constants
FPS = 60
VERTICAL_TILE_NUMBER = 45
TILE_SIZE = 16
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = len(level_map1) * TILE_SIZE
