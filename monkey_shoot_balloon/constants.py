import os
import pygame

# constants.py

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 120

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 128, 0)

# 初始狀態
INITIAL_MONEY = 300
INITIAL_LIVES = 3
MARGIN = 48 # 路徑邊界的距離

ENEMY_SPAWN_RATE = 0.5 # 每 0.5 秒生成一隻敵人

# UI path
UI_PATH = os.path.join("assets", "images", "UI")
DECOR_PATH = os.path.join("assets", "images", "decor")
PATH_END_IMAGE = os.path.join("assets", "images", "wood-cabin.png")


# 路徑座標
GRID_PATH = [
    [2,0],
    [2,4],
    [3,4],
    [3,5],
    [4,5],
    [7,5],
    [7,8],
    [5,8],
    [5,2],
    [9,2],
    [9,4],
    [15,4],
    [15,6],
    [9,6],
    [9,9],
    [8,9],
    [8,7],
    [12,7],
    [12,10],
]

STATIC_PATH = [[col * 64, row * 64] for (col, row) in GRID_PATH]



PATH_MODE = "static"   # "static" | "random"

TILE_PATH = os.path.join("assets", "images", "tiles")
TILE_SIZE = 64

UI_FONT = os.path.join("assets", "fonts", "font.otf")
BACKGROUND_IMAGE = os.path.join("assets", "images", "background.png")
