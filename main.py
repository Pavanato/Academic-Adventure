import sys
import os

# Add the src directory to sys.path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

# Now you can import your module
from academic_adventure import Game

# Crie uma instância da classe Game
game_instance = Game()

game_instance.run()
