import math

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

def get_path_points():
    """ 回傳地圖的路徑座標點清單 """
    return MAP_PATH_POINTS


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