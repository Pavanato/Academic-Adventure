"""
This module contains all the game settings.
"""

from csv import reader

def import_csv_layout(path):
    """
    Function to import a CSV file and convert it into a terrain map.

    Parameters
    ----------
    path (str): The path to the CSV file.

    Returns
    -------
    list: A list of strings representing the terrain map.
    """
    
    terrain_map = []
    with open(path) as map:
        csv_reader = reader(map)
        for row in csv_reader:
            row = [' ' if cell == '-1' else 'X' if cell == '0' else 'C' if cell == '12' else 'N' if cell == '3' else cell for cell in row]
            terrain_map.append(''.join(row))
    return terrain_map


# Importing level maps from CSV files
level_map1 = import_csv_layout(r"src\graphics\backgrounds\outside_map.csv")
level_map2 = import_csv_layout(r"src\graphics\backgrounds\inside_map.csv")

# List of background images
bg_list = [r"src\graphics\backgrounds\outside_map.png", r"src\graphics\backgrounds\inside_map.png"]

# List of questions for the game
list_of_questions = [
    {'text': 'Calculate 77 + 33?', 'answers': ['100', '110', '120', 1]},
    {'text': 'What is the square root of 169?', 'answers': ['13', '17', '19', 0]},
    {'text': 'Evaluate 2(x+3)+5=-1', 'answers': ['-1!', '-2!', '-3!', 2]},
    {'text': 'Is zero a integer number?', 'answers': ['Yes', 'No', "Zero isn't a number", 0]},
    {'text': "What's the sum of the first 5 even numbers?", 'answers': ['10', '20', '22', 1]},
    {'text': 'Every square is a rectangle?', 'answers': ['Yes', 'No', 'Maybe', 0]},
    {'text': 'What is the graph of xy = 1?', 'answers': ['An Elipse', 'A Parabola', 'A Hyperbole', 2]},
    {'text': 'Limit as x -> 0 of sinx / x', 'answers': ['Infinity', '0', '1', 2]},
    {'text': "Sum of the inverse of the Natural Numbers", 'answers': ['Converges to 0', 'Converges to 1/2', 'Diverges', 2]},
    {'text': '(Piano Question)\nHow many movies are in The Twilight Saga?', 'answers': ['3', '4', '5', 2]}
]

# List of level maps
level_list = [level_map1, level_map2]

# Game constants
FPS = 60  # Frames per second
VERTICAL_TILE_NUMBER = 45  # Number of vertical tiles
TILE_SIZE = 16  # Size of each tile in pixels
SCREEN_WIDTH = 1280  # Width of the game screen in pixels
SCREEN_HEIGHT = len(level_map1) * TILE_SIZE  # Height of the game screen in pixels