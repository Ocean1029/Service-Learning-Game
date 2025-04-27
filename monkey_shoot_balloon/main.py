# main.py
import patch_resources   # ← 一行就搞定全局 patch
from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
    
