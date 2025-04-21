import math
import random

# try

MAP_PATH_POINTS = [
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

# Store the generated path to reuse during a single game session
current_path = None

def generate_random_path():
    """Generate a random path for enemies to follow"""
    screen_width = 800
    screen_height = 600
    
    # Start position is always at the top of the screen
    start_x = random.randint(30, 150)
    path = [[start_x, 0]]
    
    # Number of waypoints (between 7 and 12)
    num_points = random.randint(7, 12)
    
    current_x, current_y = start_x, 0
    
    # Generate waypoints
    for i in range(num_points):
        # Decide direction: horizontal or vertical movement
        if i % 2 == 0:  # Even indices: move vertically
            # Don't go beyond the bottom of the screen
            max_y = min(current_y + 200, screen_height - 50)
            new_y = random.randint(current_y + 50, max_y)
            path.append([current_x, new_y])
            current_y = new_y
        else:  # Odd indices: move horizontally
            # Choose left or right movement, but ensure we stay within bounds
            if current_x < screen_width / 2:
                # More likely to move right if in left half
                direction = random.choices([-1, 1], weights=[30, 70])[0]
            else:
                # More likely to move left if in right half
                direction = random.choices([-1, 1], weights=[70, 30])[0]
            
            distance = random.randint(80, 250)
            
            # Make sure we stay within screen bounds
            if direction == 1:  # moving right
                new_x = min(current_x + distance, screen_width - 30)
            else:  # moving left
                new_x = max(current_x - distance, 30)
            
            path.append([new_x, current_y])
            current_x = new_x
    
    # Ensure the path ends at the bottom of the screen
    # If the last movement was horizontal, add a final vertical movement
    if path[-1][1] < screen_height - 50:
        path.append([path[-1][0], screen_height])
    
    return path

def get_path_points():
    """ Return path coordinates - randomly generated the first time it's called """
    global current_path
    
    # If no path has been generated yet or we want a new path each game
    if current_path is None:
        current_path = generate_random_path()
    
    return current_path

def reset_path():
    """Reset the current path to force generation of a new one"""
    global current_path
    current_path = None

def point_to_segment_distance(px, py, x1, y1, x2, y2):
    """
    計算點(px, py)到線段(x1, y1)-(x2, y2)的最短距離。
    若線段退化為單點(重疊)，直接回傳點到這個端點的距離。
    """
    # 線段向量
    seg_vx = x2 - x1
    seg_vy = y2 - y1
    seg_len_sq = seg_vx**2 + seg_vy**2

    # 若線段長度為 0，代表兩點重疊
    if seg_len_sq == 0:
        return math.hypot(px - x1, py - y1)

    # 向量 dp = P - A
    dp_vx = px - x1
    dp_vy = py - y1

    # 計算 (dp · seg) / |seg|^2 對應線段投影比例 t
    # t < 0 代表投影落在線段 A 延長之前
    # t > 1 代表投影落在線段 B 之後
    t = (dp_vx * seg_vx + dp_vy * seg_vy) / seg_len_sq

    if t < 0:
        # 最短距離是到A點
        return math.hypot(px - x1, py - y1)
    elif t > 1:
        # 最短距離是到B點
        return math.hypot(px - x2, py - y2)
    else:
        # 投影點在線段中間
        proj_x = x1 + t * seg_vx
        proj_y = y1 + t * seg_vy
        return math.hypot(px - proj_x, py - proj_y)

def is_point_near_path(px, py, path_points, margin=30):
    """
    檢查點(px, py)是否距離路徑(由多個相鄰座標構成)太近。
    只要有任何一段線段的距離 <= margin，即回傳 True。
    你可以在邏輯上：如果回傳 True，就禁止放置塔。
    """
    if len(path_points) < 2:
        return False  # 若路徑不足兩點，沒有線段可判斷

    for i in range(len(path_points) - 1):
        x1, y1 = path_points[i]
        x2, y2 = path_points[i+1]
        dist = point_to_segment_distance(px, py, x1, y1, x2, y2)
        if dist <= margin:
            return True
    return False