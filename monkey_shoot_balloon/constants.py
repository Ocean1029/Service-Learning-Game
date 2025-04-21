import os

# constants.py

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# 初始狀態
INITIAL_MONEY = 300
INITIAL_LIVES = 3
MARGIN = 30 # 路徑邊界的距離

ENEMY_SPAWN_RATE = 0.5 # 每 0.5 秒生成一隻敵人

# UI path
UI_PATH = os.path.join("assets", "images", "UI")
DECOR_PATH = os.path.join("assets", "images", "decor")
# path end image
PATH_END_IMAGE = os.path.join("assets", "images", "wood-cabin.png")

STATIC_PATH = [
    [50, 0],    # 起始：頂端靠左
    [50, 100],  # 往下
    [250, 100], # 向右延伸
    [250, 200], # 往下
    [150, 200], # 回左
    [150, 300], # 再往下
    [350, 300], # 向右大幅延伸
    [350, 150], # 往回上
    [500, 150], # 向右
    [500, 400], # 向下
    [700, 400], # 向右
    [700, 500]  # 末端：靠近螢幕下方
]

PATH_MODE = "static"   # "static" | "random"