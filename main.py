"""This script works as prototype launcher"""

from Classes.Game.Game import Game
import os

if __name__ == "__main__":
    # get current directory for easy relative paths
    scripts_directory = os.path.dirname(os.path.abspath(__file__))
    Game(scripts_directory, False , False)