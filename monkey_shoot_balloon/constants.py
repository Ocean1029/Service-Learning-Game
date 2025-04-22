import os

# constants.py

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

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
# path end image
PATH_END_IMAGE = os.path.join("assets", "images", "wood-cabin.png")

STATIC_PATH = [
    [64, 0],     # 起點：最上方靠左一格
    [64, 128],   # 向下 2 格
    [256, 128],  # 向右 3 格
    [256, 192],  # 向下 1 格
    [128, 192],  # 向左 2 格
    [128, 320],  # 向下 2 格
    [384, 320],  # 向右 4 格
    [384, 128],  # 向上 3 格
    [512, 128],  # 向右 2 格
    [512, 384],  # 向下 4 格
    [704, 384],  # 向右 3 格
    [704, 512]   # 向下 2 格（終點）
]


PATH_MODE = "static"   # "static" | "random"

TILE_PATH = os.path.join("assets", "images", "tiles")